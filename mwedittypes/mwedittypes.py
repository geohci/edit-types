from mwedittypes.node_differ import get_diff_count
from mwedittypes.simple_differ import get_diff as simple_get_diff
from mwedittypes.tree_differ import get_diff


class StructuredEditTypes:

    def __init__(self, prev_wikitext='', curr_wikitext='', lang='en', timeout=False, debug=False):
        self.prev_wikitext = prev_wikitext
        self.curr_wikitext = curr_wikitext
        self.lang = lang
        self.timeout = timeout
        self.debug = debug
        self.tree_diff = None
        self.actions = None

    def get_diff(self):
        self.tree_diff = get_diff(self.prev_wikitext, self.curr_wikitext, lang=self.lang,
                                  timeout=self.timeout, debug=self.debug)
        self.actions = get_diff_count(self.tree_diff, lang=self.lang)
        return self.actions


class SimpleEditTypes:

    def __init__(self, prev_wikitext='', curr_wikitext='', lang='en'):
        self.prev_wikitext = prev_wikitext
        self.curr_wikitext = curr_wikitext
        self.lang = lang
        self.actions = None

    def get_diff(self):
        self.actions = simple_get_diff(self.prev_wikitext, self.curr_wikitext, lang=self.lang)
        return self.actions

class EditCategories:

    def __init__(self):
        self.COMPLEX_EDIT_TYPES = ['Template', 'Media', 'Table']
        self.CONTEXT_TYPES = ['Section', 'Sentence', 'Paragraph']
        self.ANNOTATION_TYPES = ['Category', 'Wikilink', 'ExternalLink']
        # Word is a content type and handled explicitly in the function
        # also not included explicitly here are any generic Tags -- i.e. adding HTML tags to wikitext
        self.MAINTENANCE_TYPES = ['List',  # this is just the syntax -- e.g., adding a `*` to the start of a line
                                  'Text Formatting', 'Punctuation',  # text changes that don't really impact meaning
                                  'Heading',  # structuring existing content
                                  'Reference',  # very important but not actual content
                                  'Comment']  # no impact on content

        self.CON_GEN = 'Content Generation'
        self.CON_MAI = 'Content Maintenance'
        self.CON_ANN = 'Content Annotation'

        self.EASY_TYPES = ['Whitespace', 'Punctuation', 'Word', 'Character', 'Sentence', 'Paragraph', 'Section']
        self.MEDIUM_TYPES = ['Comment', 'List', 'Category', 'Wikilink', 'ExternalLink', 'Text Formatting', 'Heading']
        self.HARD_TYPES = ['Other Tag', 'Reference', 'Media', 'Table', 'Template']

    def details_to_dict(self, details):
        if details is not None:
            expanded = {'context': details['context'],
                        'node-edits': details['node-edits'],
                        'text-edits': details['text-edits']}
            for n in expanded['node-edits']:
                for i in range(0, len(n.changes)):
                    c = n.changes[i]
                    n.changes[i] = {'change-type': c[0], 'prev': c[1], 'curr': c[2]}
            return expanded

    def get_edit_categories(self, prev_wikitext='', curr_wikitext='', lang='en', gen_categories=True):
        """
        Map a revision's atomic edit types to a higher-level taxonomy of edit categories:
        * Content Generation (gen): adding new information
        * Content Annotation (ann): adding new metadata
        * Content Maintenance (mai): cleaning existing content

        NOTE: If this can be done with simple edittypes, those are used (far faster).
              For certain more complex edit types, the structured ediittypes are run and
              edit categories are determined based on the additional details.
        """
        simple_et = SimpleEditTypes(prev_wikitext=prev_wikitext, curr_wikitext=curr_wikitext, lang=lang).get_diff()
        edit_categories = self.simple_et_to_higher_level(simple_et)
        if self.needs_structured(simple_et):
            full_et = StructuredEditTypes(prev_wikitext=prev_wikitext, curr_wikitext=curr_wikitext, lang=lang).get_diff()
            expanded_full_et = self.details_to_dict(full_et)
            for cat, cnt in self.full_et_to_higher_level(expanded_full_et).items():
                edit_categories[cat] = edit_categories.get(cat, 0) + cnt

        difficulty = self.simple_et_to_difficulty(simple_et)
        size = self.simple_et_to_size(simple_et)
        text_change = self.text_changed(simple_et)

        return size, difficulty, text_change, edit_categories

    def needs_structured(self, edit_types_summary):
        """Determine if structured edit types need to be computed to make assessment."""
        for et in self.COMPLEX_EDIT_TYPES:
            if et in edit_types_summary:
                return True
        return False

    def full_et_to_higher_level(self, edit_types):
        """Same as simple_et_to_higher_level but for more complex edit types."""
        types = {}
        for et in edit_types.get('node-edits', []):
            if et.type in self.COMPLEX_EDIT_TYPES:
                if et.type == 'Template':
                    # Insert template w/o parameters: annotation (probably metadata but either
                    # way the editor is connecting content not creating new content)
                    if et.edittype == 'insert':
                        con_ann = True
                        for chg in et.changes:
                            if chg['change-type'] == 'parameter':
                                con_ann = False
                                types[self.CON_GEN] = types.get(self.CON_GEN, 0) + 1
                                break
                        if con_ann:
                            types[self.CON_ANN] = types.get(self.CON_ANN, 0) + 1
                    # Move/remove template = maintenance
                    elif et.edittype in ['move', 'remove']:
                        types[self.CON_MAI] = types.get(self.CON_MAI, 0) + 1
                    # Change template by adding a new parameter = content creation;
                    # otherwise content maintenance of existing content
                    else:
                        print(et)
                        params_removed = 0
                        params_inserted = 0
                        for chg in et.changes:
                            if chg['change-type'] == 'parameter':
                                if chg['prev'] is None or not chg['prev'][1]:
                                    params_inserted += 1
                                elif chg['curr'] is None or not chg['curr'][1]:
                                    params_removed += 1
                        if params_inserted > params_removed:
                            types[self.CON_GEN] = types.get(self.CON_GEN, 0) + 1
                        else:
                            types[self.CON_MAI] = types.get(self.CON_MAI, 0) + 1
                elif et.type == 'Media':
                    # Insert media: content generation
                    if et.edittype == 'insert':
                        types[self.CON_GEN] = types.get(self.CON_GEN, 0) + 1
                    # Move/remove media = maintenance
                    elif et.edittype in ['move', 'remove']:
                        types[self.CON_MAI] = types.get(self.CON_MAI, 0) + 1
                    # Change media by adding a caption/alt text = content generation;
                    # otherwise content maintenance
                    else:
                        con_main = False
                        for chg in et.changes:
                            if chg['change-type'] == 'caption' and chg['prev'] is None:
                                types[self.CON_GEN] = types.get(self.CON_GEN, 0) + 1
                            elif chg['change-type'] == 'option':
                                if chg['prev'] is None and chg['curr'].split('=', maxsplit=1)[
                                    0].strip().lower() == 'alt':
                                    types[self.CON_GEN] = types.get(self.CON_GEN, 0) + 1
                            else:
                                con_main = True
                        if con_main:
                            types[self.CON_MAI] = types.get(self.CON_MAI, 0) + 1
                elif et.type == 'Table':
                    # Insert = content creation
                    if et.edittype == 'insert':
                        types[self.CON_GEN] = types.get(self.CON_GEN, 0) + 1
                    # Move/remove = content maintenance
                    elif et.edittype in ['move', 'remove']:
                        types[self.CON_MAI] = types.get(self.CON_MAI, 0) + 1
                    # Change = creation if adding cells; otherwise maintenance
                    else:
                        con_gen = False
                        con_mai = False
                        for chg in et.changes:
                            if chg['change-type'] == 'caption' and chg['prev'] is None:
                                con_gen = True
                            elif chg['change-type'] == 'cells':
                                if chg['prev'] == 'insert':
                                    con_gen = True
                                else:
                                    con_mai = True
                            else:
                                con_mai = True
                        if con_gen:
                            types[self.CON_GEN] = types.get(self.CON_GEN, 0) + 1
                        if con_mai:
                            types[self.CON_MAI] = types.get(self.CON_MAI, 0) + 1
        return types

    def simple_et_to_size(self, summary):
        changes = 0
        for et in summary:
            if et not in self.CONTEXT_TYPES:
                for chgtype in summary[et]:
                    changes += summary[et][chgtype]

        size = 'Small'
        if changes > 20:
            size = 'Large'
        elif changes > 10:
            size = 'Medium-Large'
        elif changes > 5:
            size = 'Small-Medium'
        return size

    def simple_et_to_difficulty(self, summary):
        difficulty_level = 'Easy'
        for et in summary:
            if et in self.MEDIUM_TYPES and difficulty_level.startswith('Easy'):
                if 'insert' in summary[et]:
                    difficulty_level = 'Medium-Hard'
                else:
                    difficulty_level = 'Easy-Medium'
            elif et in self.HARD_TYPES:
                difficulty_level = 'Hard'
                break
        return difficulty_level

    def text_changed(self, summary):
        for et in summary:
            if et in ['Word', 'Character']:
                return True
        return False

    def simple_et_to_higher_level(self, summary):
        types = {}
        # If just whitespace and optionally section/paragraph/sentence -> whitespace only
        if 'Whitespace' in summary and len(summary) <= 4:
            whitespace_only = True
            for et in summary:
                if et not in self.CONTEXT_TYPES and et != 'Whitespace':
                    whitespace_only = False
                    break
            if whitespace_only:
                return {self.CON_MAI: 1}

        for et in summary:
            # contextual information: not relevant
            # complex nodes handled in other function
            if et in self.CONTEXT_TYPES or et in self.COMPLEX_EDIT_TYPES:
                continue
            # punctuation w/o words = content maintenance; otherwise ignore punctuation component
            elif et == 'Punctuation' and ('Word' not in summary and 'Character' not in summary):
                types[self.CON_MAI] = types.get(self.CON_MAI, 0) + 1
            elif et in self.ANNOTATION_TYPES:
                ann_ets = summary[et]
                if 'change' in ann_ets or 'remove' in ann_ets or 'move' in ann_ets:
                    types[self.CON_MAI] = types.get(self.CON_MAI, 0) + 1
                if 'insert' in ann_ets:
                    types[self.CON_ANN] = types.get(self.CON_ANN, 0) + 1
            elif et in self.MAINTENANCE_TYPES:
                types[self.CON_MAI] = types.get(self.CON_MAI, 0) + 1
            elif et == 'Word' or et == 'Character':
                sent_ets = summary.get('Sentence', {})
                new_sentences = sent_ets.get('insert', 0)
                if new_sentences:
                    types[self.CON_GEN] = types.get(self.CON_GEN, 0) + new_sentences
                if 'change' in sent_ets or 'remove' in sent_ets or 'move' in sent_ets:
                    types[self.CON_MAI] = types.get(self.CON_MAI, 0) + 1
            elif et == 'Other Tag':
                types[self.CON_MAI] = types.get(self.CON_MAI, 0) + 1

        return types
