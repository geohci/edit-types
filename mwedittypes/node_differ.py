from collections import namedtuple
import mwparserfromhell as mw

from mwedittypes.tokenizer import parse_change_text
from mwedittypes.utils import parse_image_options

NodeEdit = namedtuple('NodeEdit', ['type', 'edittype', 'section', 'name', 'changes'])
TextEdit = namedtuple('TextEdit', ['type', 'edittype', 'text', 'count'])
Context = namedtuple('Context', ['type', 'edittype', 'count'])


def get_node_diff(node_type, prev_wikitext='', curr_wikitext='', lang='en'):
    """Identify fine-grained changes between two wikitext nodes.

    Parameters
    ----------
    node_type: str
        Node type -- e.g., Template, Category
    prev_wikitext : str
        Previous wikitext for node
    curr_wikitext : str
        Current wikitext for node
    lang : str
        Language code for Wikipedia -- e.g., 'en' = English

    Returns
    -------
    changes
        List with specific differences between previous and current nodes. Most whitespace changes are ignored.
    """
    name = None
    changes = []
    try:
        prev_wc = mw.parse(prev_wikitext).nodes[0] if prev_wikitext else None
        curr_wc = mw.parse(curr_wikitext).nodes[0] if curr_wikitext else None

        if node_type == 'Template':
            # separate between name changes and parameter changes
            pt_name = prev_wc.name.strip() if prev_wc else None
            ct_name = curr_wc.name.strip() if curr_wc else None
            name = pt_name if pt_name else ct_name
            pt_params = {str(p.name).strip(): str(p.value).strip() for p in prev_wc.params} if prev_wc else {}
            ct_params = {str(p.name).strip(): str(p.value).strip() for p in curr_wc.params} if curr_wc else {}
            if pt_name != ct_name:
                changes.append(('name', pt_name, ct_name))
            params = set(pt_params).union(set(ct_params))
            for p in params:
                if pt_params.get(p) != ct_params.get(p):
                    changes.append(('parameter',
                                    (p, pt_params[p]) if p in pt_params else None,
                                    (p, ct_params[p]) if p in ct_params else None))

        elif node_type == 'Media':
            # Media can be in three different formats:
            # Brackets: [[File:filename.ext|formatting options|caption]]
            # Template: File:filename.ext
            # Gallery: filename.ext|formatting options|caption
            # If template or gallery, we add the brackets and re-parse so the title/options can be consistently handled
            if prev_wikitext and not prev_wikitext.startswith('[['):
                prev_wc = mw.parse(f'[[{prev_wikitext}]]').nodes[0]
            if curr_wikitext and not curr_wikitext.startswith('[['):
                curr_wc = mw.parse(f'[[{curr_wikitext}]]').nodes[0]

            pm_title = prev_wc.title.strip() if prev_wc else None
            cm_title = curr_wc.title.strip() if curr_wc else None
            name = pm_title if pm_title else cm_title
            if pm_title != cm_title:
                changes.append(('filename', pm_title, cm_title))

            pm_options, pm_caption = parse_image_options(prev_wc.text.strip() if prev_wc else '', lang=lang)
            cm_options, cm_caption = parse_image_options(curr_wc.text.strip() if curr_wc else '', lang=lang)

            if pm_caption != cm_caption:
                changes.append(('caption', pm_caption, cm_caption))

            options = set(pm_options).union(set(cm_options))
            for o in options:
                if o not in pm_options:
                    changes.append(('option', None, o))
                elif o not in cm_options:
                    changes.append(('option', o, None))

        elif node_type == 'Category':
            # identify if category name changes in likely meaningful way
            prev_cat = prev_wc.title.split(':', maxsplit=1)[1].replace('_', ' ') if prev_wc else None
            curr_cat = curr_wc.title.split(':', maxsplit=1)[1].replace('_', ' ') if curr_wc else None
            name = prev_cat if prev_cat else curr_cat
            if prev_cat != curr_cat:
                changes.append(('title', prev_cat, curr_cat))

        elif node_type == 'Wikilink':
            # separate between title (destination) and text (display) changes
            pl_title = prev_wc.title.strip() if prev_wc and prev_wc.title else None
            cl_title = curr_wc.title.strip() if curr_wc and curr_wc.title else None
            name = pl_title if pl_title else cl_title
            if pl_title != cl_title:
                changes.append(('title', pl_title, cl_title))

            pl_text = prev_wc.text.strip() if prev_wc and prev_wc.text else None
            cl_text = curr_wc.text.strip() if curr_wc and curr_wc.text else None
            if pl_text != cl_text:
                changes.append(('text', pl_text, cl_text))

        elif node_type == 'Reference':
            # Separate between attributes and contents changes
            pr_name = None
            for a in prev_wc.attributes:
                if a.name == 'name':
                    pr_name = a.value
            cr_name = None
            for a in curr_wc.attributes:
                if a.name == 'name':
                    cr_name = a.value
            if pr_name != cr_name:
                changes.append(('name', pr_name, cr_name))

            # ref text -- ignoring templates etc.
            pr_text = prev_wc.contents.strip_code().strip() if prev_wc else None
            cr_text = curr_wc.contents.strip_code().strip() if curr_wc else None
            if pr_text != cr_text:
                changes.append(('text', pr_text, cr_text))

            if pr_name:
                name = pr_name
            elif cr_name:
                name = cr_name

            # heuristic -- check first template too
            try:
                pr_temp = str(prev_wc.contents.filter_templates(recursive=False)[0])
            except Exception:
                pr_temp = ''
            try:
                cr_temp = str(curr_wc.contents.filter_templates(recursive=False)[0])
            except Exception:
                cr_temp = ''

            if pr_temp != cr_temp:
                changes.append(('ref-template', pr_temp, cr_temp))

        elif node_type == 'Table':
            # check for attribute changes, header changes, cell changes
            pt_attrs = {str(a.name).strip(): str(a.value).strip() for a in prev_wc.attributes} if prev_wc else {}
            ct_attrs = {str(a.name).strip(): str(a.value).strip() for a in curr_wc.attributes} if curr_wc else {}
            attrs = set(pt_attrs).union(set(ct_attrs))
            for a in attrs:
                if pt_attrs.get(a) != ct_attrs.get(a):
                    changes.append(('attribute',
                                    (a, pt_attrs[a]) if a in pt_attrs else None,
                                    (a, ct_attrs[a]) if a in ct_attrs else None))

            pt_caption = None
            pt_cells = {}
            if prev_wc:
                for te in mw.parse(prev_wikitext).filter_tags():
                    if te.tag == 'td' or te.tag == 'th':
                        if '+' in [a.name for a in te.attributes] or te.contents.startswith('+'):
                            pt_caption = te.contents.lstrip('+')
                        else:
                            cell = hash(te.contents.strip())
                            pt_cells[cell] = pt_cells.get(cell, 0) + 1

            ct_caption = None
            ct_cells = {}
            if curr_wc:
                for te in mw.parse(curr_wikitext).filter_tags():
                    if te.tag == 'td' or te.tag == 'th':
                        if '+' in [a.name for a in te.attributes] or te.contents.startswith('+'):
                            ct_caption = te.contents.lstrip('+')
                        else:
                            cell = hash(te.contents.strip())
                            ct_cells[cell] = ct_cells.get(cell, 0) + 1

            if pt_caption != ct_caption:
                changes.append(('caption', pt_caption, ct_caption))

            allcells = set(pt_cells.keys()).union(set(ct_cells.keys()))
            changed = 0
            inserted = max(0, sum(ct_cells.values()) - sum(pt_cells.values()))
            removed = max(0, sum(pt_cells.values()) - sum(ct_cells.values()))
            for c in allcells:
                changed += abs(pt_cells.get(c, 0) - ct_cells.get(c, 0))
            changed -= (inserted + removed)
            changed = changed / 2  # each change results in two no-longer-matching cell values
            if inserted:
                changes.append(('cells', 'insert', inserted))
            if removed:
                changes.append(('cells', 'remove', removed))
            if changed:
                changes.append(('cells', 'change', changed))

        elif node_type == 'Text Formatting':
            # check if format type changed
            # Note this will skip '''text''' -> <b>text</b> which are both `b` tags (same for italics)
            prev_tag = str(prev_wc.tag) if prev_wc else None
            curr_tag = str(curr_wc.tag) if curr_wc else None
            if prev_tag != curr_tag:
                changes.append(('format tag', prev_tag, curr_tag))

        elif node_type == 'List':
            # check if list type changed
            prev_tag = str(prev_wc.tag) if prev_wc else None
            curr_tag = str(curr_wc.tag) if curr_wc else None
            if prev_tag != curr_tag:
                changes.append(('list item', prev_tag, curr_tag))

        elif node_type == 'Gallery':
            # Ignore contents changes as they should be captured my media changes
            pr_attrs = {str(a.name).strip(): str(a.value).strip() for a in prev_wc.attributes} if prev_wc else {}
            cr_attrs = {str(a.name).strip(): str(a.value).strip() for a in curr_wc.attributes} if curr_wc else {}
            attrs = set(pr_attrs).union(set(cr_attrs))
            for a in attrs:
                if pr_attrs.get(a) != cr_attrs.get(a):
                    changes.append(('attribute',
                                    (a, pr_attrs[a]) if a in pr_attrs else None,
                                    (a, cr_attrs[a]) if a in cr_attrs else None))

        elif node_type == 'Heading':
            # separate between level and title changes
            ph_level = prev_wc.level if prev_wc else None
            ch_level = curr_wc.level if curr_wc else None
            if ph_level != ch_level:
                changes.append(('level', ph_level, ch_level))
            ph_title = prev_wc.title.strip() if prev_wc else None
            ch_title = curr_wc.title.strip() if curr_wc else None
            name = ph_title if ph_title else ch_title
            if ph_title != ch_title:
                changes.append(('title', ph_title, ch_title))

        elif node_type == 'Comment':
            # check if comment contents changed
            pc_contents = prev_wc.contents.strip() if prev_wc else None
            cc_contents = curr_wc.contents.strip() if curr_wc else None
            if pc_contents != cc_contents:
                changes.append(('comment', pc_contents, cc_contents))

        elif node_type == 'External Link':
            # separate between url and text (display) changes
            pe_url = prev_wc.url if prev_wc else None
            ce_url = curr_wc.url if curr_wc else None
            name = pe_url if pe_url else ce_url
            if pe_url != ce_url:
                changes.append(('url', pe_url, ce_url))

            pl_display = prev_wc.title.strip() if prev_wc else None
            cl_display = curr_wc.title.strip() if curr_wc else None
            if pl_display != cl_display:
                changes.append(('text', pl_display, cl_display))
    except Exception:
        pass
    return name, changes


def get_diff_count(result, lang='en'):
    """Prepares more complete edit type summary based on tree diff result.

    Parameters
    ----------
    result : dict
        The tree diff result containing inserts, removes, changes, and moves made in a Wikipedia revision.
    lang : string
        The language edition associated with the diff. Necessary for parsing text changes correctly.
    Returns
    -------
    dict
        a dict containing each occurrence of a change
    """

    node_edits = []
    text_edits = []
    context = []
    section_titles = set()
    prev_text = []
    curr_text = []

    # go through each type of action (insert, remove, change, move) and compute edit types
    for r in result['remove']:
        text = r['text']  # wikitext of the node
        et = r['type']
        section_titles.add(r['section'])
        # if node is text, just check whether there's anything and retain for later
        # because all the text is processed at once at the end
        if et == 'Text' and text:
            prev_text.append(text)
        # non-text node: verify/fine-tune the edit type and add to results dictionary
        else:
            name, changes = get_node_diff(node_type=et, prev_wikitext=text, curr_wikitext='', lang=lang)
            node_edits.append(NodeEdit(et, 'remove', r['section'], name, changes))
    for i in result['insert']:
        text = i['text']
        et = i['type']
        section_titles.add(i['section'])
        if et == 'Text' and text:
            curr_text.append(text)
        else:
            name, changes = get_node_diff(node_type=et, prev_wikitext='', curr_wikitext=text, lang=lang)
            node_edits.append(NodeEdit(et, 'insert', i['section'], name, changes))
    for c in result['change']:
        et = c['prev']['type']
        ptext = c['prev']['text']
        ctext = c['curr']['text']
        section_titles.add(c['curr']['section'])
        section_titles.add(c['prev']['section'])
        if et == 'Text' and ptext != ctext:
            prev_text.append(ptext)
            curr_text.append(ctext)
        else:
            # edge-case where text formatting changes might just be the inner text
            # but we're only interested in counting it if the formatting tags themselves changed
            # e.g., '''Text''' -> ''Text'' but not '''Text''' -> '''Different text'''
            if et == 'Text Formatting':
                if mw.parse(ptext).nodes[0].tag == mw.parse(ctext).nodes[0].tag:
                    continue
            name, changes = get_node_diff(node_type=et, prev_wikitext=ptext, curr_wikitext=ctext, lang=lang)
            node_edits.append(NodeEdit(et, 'change', c['prev']['section'], name, changes))
    for m in result['move']:
        et = m['prev']['type']
        ptext = m['prev']['text']
        ctext = m['curr']['text']
        section_titles.add(m['curr']['section'])
        section_titles.add(m['prev']['section'])
        name, changes = get_node_diff(node_type=et, prev_wikitext=ptext, curr_wikitext=ctext, lang=lang)
        node_edits.append(NodeEdit(et, 'move', m['prev']['section'], name, changes))

    # give raw insert/remove counts
    # changes can be assumed to be overlap between insert+remove -- e.g., 5 insert and 3 remove -> 3 change, 2 insert
    # but would require more work to align well enough to know where words were likely changed vs. inserted/removed
    if prev_text or curr_text:
        is_text_change_found = parse_change_text(''.join(prev_text), ''.join(curr_text), lang=lang, summarize=False)
        if is_text_change_found:
            for text_subcat, text_et in is_text_change_found.items():
                for txt, et_count in text_et.items():
                    if et_count > 0:
                        text_edits.append(TextEdit(text_subcat, 'insert', txt, et_count))
                    elif et_count < 0:
                        text_edits.append(TextEdit(text_subcat, 'remove', txt, abs(et_count)))

    # identify how many sections have been edited based on a few heuristics
    if section_titles:
        sec_remove = sum([1 for n in node_edits if n.type == 'Heading' and n.edittype == 'remove']) + int('curr-no-content' in result)
        sec_insert = sum([1 for n in node_edits if n.type == 'Heading' and n.edittype == 'insert']) + int('prev-no-content' in result)
        sec_change = len(section_titles) - sec_remove - sec_insert
        if sec_remove:
            context.append(Context('Section', 'remove', sec_remove))
        if sec_insert:
            context.append(Context('Section', 'insert', sec_insert))
        if sec_change:
            context.append(Context('Section', 'change', sec_change))

    return {'node-edits': node_edits, 'text-edits': text_edits, 'context': context}
