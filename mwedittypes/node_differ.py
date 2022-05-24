import re  # not technically needed because part of mwedittypes.tokenizer but that's confusing

import mwparserfromhell as mw
from mwedittypes.tokenizer import *
from mwedittypes.constants import *

def is_change_in_edit_type(node_type,prev_wikitext='',curr_wikitext=''):
    """ Checks if a change occurs in wikitexts

    Parameters
    ----------
    prev_wikitext : str
        Previous Wikitext
    curr_wikitext : str
        Current Wikitext
    node_type: str
        Node type
    Returns
    -------
    tuple
        Tuple containing the bool and edit type
    """
    try:
        prev_parsed_text = mw.parse(prev_wikitext)
        curr_parsed_text = mw.parse(curr_wikitext) 

        if node_type == 'Template':
            if prev_wikitext != '' and curr_wikitext != '':
                prev_temp_dict = { str(temp.name):str(temp.value) for temp in prev_parsed_text.filter_templates(recursive=False)[0].params}
                prev_temp_dict = dict(prev_temp_dict, **{'template_name':str(prev_parsed_text.filter_templates(recursive=False)[0].name)})
                
                curr_temp_dict = { str(temp.name):str(temp.value) for temp in curr_parsed_text.filter_templates(recursive=False)[0].params}
                curr_temp_dict = dict(curr_temp_dict, **{'template_name':str(curr_parsed_text.filter_templates(recursive=False)[0].name)})
                
                #Get the difference between template parameters. If it is more than 0, then a change occured
                if len(set(curr_temp_dict.items()) ^ set(prev_temp_dict.items())) > 0:
                    return True, 'Template'
            elif prev_wikitext != '' and curr_wikitext=='':
                templates = prev_parsed_text.filter_templates(recursive=False)
                if len(templates) > 0:
                    return True, 'Template'

            elif prev_wikitext == '' and curr_wikitext != '':
                templates = curr_parsed_text.filter_templates(recursive=False)
                if len(templates) > 0:
                    return True, 'Template'
            
        elif node_type == 'Media':
            if prev_wikitext != '' and curr_wikitext != '':
                if len(prev_parsed_text) > 0 and len(curr_parsed_text) > 0:
                    return True, 'Media'
            elif prev_wikitext != '' and curr_wikitext=='':
                if len(prev_parsed_text) > 0:
                    return True, 'Media'
            elif prev_wikitext == '' and curr_wikitext != '':
                if len(curr_parsed_text) > 0:
                    return True, 'Media'
        
        elif node_type == 'Category':
            if prev_wikitext != '' and curr_wikitext != '':
                prev_cat = prev_parsed_text.filter_wikilinks(recursive=False)
                curr_cat = curr_parsed_text.filter_wikilinks(recursive=False)
                if len(prev_cat) > 0 and len(curr_cat) > 0:
                    if prev_cat[0].text != curr_cat[0].text or \
                        prev_cat[0].title != curr_cat[0].title:
                        return True, 'Category'
                        
            elif prev_wikitext != '' and curr_wikitext=='':
                category = prev_parsed_text.filter_wikilinks(recursive=False)
                if len(category) > 0:
                    return True, 'Category'
            elif prev_wikitext == '' and curr_wikitext != '':
                category = curr_parsed_text.filter_wikilinks(recursive=False)
                if len(category) > 0:
                    return True, 'Category'

        elif node_type == 'Wikilink':
            if prev_wikitext != '' and curr_wikitext != '':
                prev_wikilink = prev_parsed_text.filter_wikilinks(recursive=False)
                curr_wikilink = curr_parsed_text.filter_wikilinks(recursive=False)

                if len(prev_wikilink) > 0 and len(curr_wikilink) > 0:
                    if prev_wikilink[0].text != curr_wikilink[0].text or \
                        prev_wikilink[0].title != curr_wikilink[0].title:
                        return True, 'Wikilink'
            elif prev_wikitext != '' and curr_wikitext=='':
                wikilinks = prev_parsed_text.filter_wikilinks(recursive=False)
                if len(wikilinks) > 0:
                    return True, 'Wikilink' 
            elif prev_wikitext == '' and curr_wikitext != '':
                wikilinks = curr_parsed_text.filter_wikilinks(recursive=False)
                if len(wikilinks) > 0:
                    return True, 'Wikilink'
        
        elif node_type == 'Reference':
            #Check if a reference changes
            if prev_wikitext != '' and curr_wikitext != '':
                prev_filtered_ref = prev_parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)
                curr_filtered_ref = curr_parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)
                if len(prev_filtered_ref) > 0 and len(curr_filtered_ref) > 0:
                    if prev_filtered_ref[0] != curr_filtered_ref[0]:
                        return True, 'Reference'
            elif prev_wikitext != '' and curr_wikitext=='':
                ref = prev_parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)
                if len(ref) > 0:
                    return True, 'Reference'

            elif prev_wikitext == '' and curr_wikitext != '':
                ref = curr_parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)
                if len(ref) > 0:
                    return True, 'Reference'

        elif node_type == 'Table':
            if prev_wikitext != '' and curr_wikitext != '':
                #Check if a table changes
                prev_filtered_table = prev_parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)
                curr_filtered_table = curr_parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)

                if len(prev_filtered_table) > 0 and len(curr_filtered_table) > 0:
                    if prev_filtered_table[0].contents != curr_filtered_table[0].contents:
                        return True, 'Table'

            elif prev_wikitext != '' and curr_wikitext=='':
                tables = prev_parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)
                if len(tables) > 0:
                    return True, 'Table'

            elif prev_wikitext == '' and curr_wikitext != '':
                tables = curr_parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)
                if len(tables) > 0:
                    return True, 'Table'

        elif node_type == 'Text Formatting':
            #Check if a text format changes
            if prev_wikitext != '' and curr_wikitext != '':
                prev_filtered_text_formatting = prev_parsed_text.filter_tags(matches=lambda node: node.tag in TEXT_FORMATTING_TAGS,recursive=False)
                curr_filtered_text_formatting = curr_parsed_text.filter_tags(matches=lambda node: node.tag in TEXT_FORMATTING_TAGS,recursive=False)

                if len(prev_filtered_text_formatting) > 0 and len(curr_filtered_text_formatting) > 0:
                    if prev_filtered_text_formatting[0].tag != curr_filtered_text_formatting[0].tag:
                        return True, 'Text Formatting'
            elif prev_wikitext != '' and curr_wikitext=='':
                text_format = prev_parsed_text.filter_tags(matches=lambda node: node.tag in TEXT_FORMATTING_TAGS,recursive=False)
                if len(text_format) > 0:
                    return True, 'Text Formatting'
            elif prev_wikitext == '' and curr_wikitext != '':
                text_format = curr_parsed_text.filter_tags(matches=lambda node: node.tag in TEXT_FORMATTING_TAGS,recursive=False)
                if len(text_format) > 0:
                    return True, 'Text Formatting'

        elif node_type == 'List':
            if prev_wikitext != '' and curr_wikitext != '':
                #Check if a list changes
                prev_filtered_list = prev_parsed_text.filter_tags(matches=lambda node: node.tag in LIST_TAGS,recursive=False)
                curr_filtered_list = curr_parsed_text.filter_tags(matches=lambda node: node.tag in LIST_TAGS,recursive=False)

                if len(prev_filtered_list) > 0  and len(curr_filtered_list) > 0:
                    if prev_filtered_list[0].contents != curr_filtered_list[0].contents:
                        return True, 'List'

            elif prev_wikitext != '' and curr_wikitext=='':
                lists = prev_parsed_text.filter_tags(matches=lambda node: node.tag in LIST_TAGS,recursive=False)
                if len(lists) > 0:
                    return True, 'List'

            elif prev_wikitext == '' and curr_wikitext != '':
                lists = curr_parsed_text.filter_tags(matches=lambda node: node.tag in LIST_TAGS,recursive=False)
                if len(lists) > 0:
                    return True, 'List'


        elif node_type == 'Table Element':
            if prev_wikitext != '' and curr_wikitext != '':
                #Check if a table element changes
                prev_filtered_table = prev_parsed_text.filter_tags(matches=lambda node: node.tag in TABLE_ELEMENTS_TAGS,recursive=False)
                curr_filtered_table = curr_parsed_text.filter_tags(matches=lambda node: node.tag in TABLE_ELEMENTS_TAGS,recursive=False)

                if len(prev_filtered_table) > 0 and len(curr_filtered_table) > 0:
                    if prev_filtered_table[0].contents != curr_filtered_table[0].contents:
                        return True, 'Table Element'

            elif prev_wikitext != '' and curr_wikitext=='':
                table_elems = prev_parsed_text.filter_tags(matches=lambda node: node.tag in TABLE_ELEMENTS_TAGS,recursive=False)
                if len(table_elems) > 0:
                    return True, 'Table Element'

            elif prev_wikitext == '' and curr_wikitext != '':
                table_elems = curr_parsed_text.filter_tags(matches=lambda node: node.tag in TABLE_ELEMENTS_TAGS,recursive=False)
                if len(table_elems) > 0:
                    return True, 'Table Element'

        elif node_type == 'Gallery':
            #Check if a gallery changes
            if prev_wikitext != '' and curr_wikitext != '':
                prev_filtered_gallery = prev_parsed_text.filter_tags(matches=lambda node: node.tag == 'gallery',recursive=False)
                curr_filtered_gallery = curr_parsed_text.filter_tags(matches=lambda node: node.tag == 'gallery',recursive=False)

                if len(prev_filtered_gallery) > 0  and len(curr_filtered_gallery) > 0:
                    if prev_filtered_gallery[0].contents != curr_filtered_gallery[0].contents:
                        return True, 'Gallery'

            elif prev_wikitext != '' and curr_wikitext=='':
                gallery = prev_parsed_text.filter_tags(matches=lambda node: node.tag == 'gallery',recursive=False)
                if len(gallery) > 0:
                    return True, 'Gallery'

            elif prev_wikitext == '' and curr_wikitext != '':
                gallery = curr_parsed_text.filter_tags(matches=lambda node: node.tag == 'gallery',recursive=False)
                if len(gallery) > 0:
                    return True, 'Gallery'
            
        elif 'Tag' in node_type:
            #Check if a tag changes
            if prev_wikitext != '' and curr_wikitext != '':
                prev_filtered_tag = prev_parsed_text.filter_tags(recursive=False)
                curr_filtered_tag = curr_parsed_text.filter_tags(recursive=False)

                if len(prev_filtered_tag) > 0  and len(curr_filtered_tag) > 0:
                    if prev_filtered_tag[0].contents != curr_filtered_tag[0].contents:
                        return True, node_type

            elif prev_wikitext != '' and curr_wikitext=='':
                tags = prev_parsed_text.filter_tags(recursive=False)
                if len(tags) > 0:
                    return True, node_type

            elif prev_wikitext == '' and curr_wikitext != '':
                tags = curr_parsed_text.filter_tags(recursive=False)
                if len(tags) > 0:
                    return True, node_type

        elif node_type == 'Heading':
            if prev_wikitext != '' and curr_wikitext != '':
                prev_filtered_section = prev_parsed_text.filter_headings(recursive=False)[0]
                curr_filtered_section = curr_parsed_text.filter_headings(recursive=False)[0]

                if prev_filtered_section.title != curr_filtered_section.title:
                    return True, 'Heading'
            elif prev_wikitext != '' and curr_wikitext=='':
                section = prev_parsed_text.filter_headings(recursive=False)
                if len(section) > 0:
                    return True, 'Heading'
            elif prev_wikitext == '' and curr_wikitext != '':
                section = curr_parsed_text.filter_headings(recursive=False)
                if len(section) > 0:
                    return True, 'Heading'

        elif node_type == 'Comment':
            if prev_wikitext != '' and curr_wikitext != '':
                prev_filtered_comments = prev_parsed_text.filter_comments(recursive=False)[0]
                curr_filtered_comments = curr_parsed_text.filter_comments(recursive=False)[0]

                if prev_filtered_comments.contents != curr_filtered_comments.contents:
                    return True, 'Comment'

            elif prev_wikitext != '' and curr_wikitext=='':
                comments = prev_parsed_text.filter_comments(recursive=False)
                if len(comments) > 0:
                    return True, 'Comment'

            elif prev_wikitext == '' and curr_wikitext != '':
                comments = curr_parsed_text.filter_comments(recursive=False)
                if len(comments) > 0:
                    return True, 'Comment'

        elif node_type == 'External Link':
            if prev_wikitext != '' and curr_wikitext != '':
                prev_filtered_external_links = prev_parsed_text.filter_external_links(recursive=False)[0]
                curr_filtered_external_links = curr_parsed_text.filter_external_links(recursive=False)[0]

                if prev_filtered_external_links.title != curr_filtered_external_links.title or \
                    prev_filtered_external_links.url != curr_filtered_external_links.url:
                    return True, 'External Link'
            elif prev_wikitext != '' and curr_wikitext=='':
                external_links = prev_parsed_text.filter_external_links(recursive=False)
                if len(external_links) > 0:
                    return True, 'External Link'

            elif prev_wikitext == '' and curr_wikitext != '':
                external_links = curr_parsed_text.filter_external_links(recursive=False)
                if len(external_links) > 0:
                    return True, 'External Link'
        else:
            return True, node_type
    except Exception:
        pass
    return False, None


def parse_change_text(node_type, prev_wikitext='',curr_wikitext='', lang='en'):
    # Initialize tokenizer class
    tokenizer = Tokenizer(ENGLISH_UNICODE, NON_ENGLISH_UNICODE, lang=lang)

    if node_type == 'Text':
        if prev_wikitext == '' and curr_wikitext != '':
            edittype = 'insert'
        elif prev_wikitext != '' and curr_wikitext == '':
            edittype = 'remove'
        elif prev_wikitext != '' and curr_wikitext != '':
            edittype = 'change'
        else:
            edittype = None

        
        if edittype:
            prev_tokenizer = tokenizer.tokenize_and_get_occurence(prev_wikitext)
            curr_tokenizer = tokenizer.tokenize_and_get_occurence(curr_wikitext)

            result = {}
            for text_category in curr_tokenizer.keys():
                items_diff_list = list(set(curr_tokenizer[text_category].items())  ^ set(prev_tokenizer[text_category].items()))
                for item in items_diff_list:
                    diff = curr_tokenizer[text_category].get(item[0], 0) - prev_tokenizer[text_category].get(item[0],0)
                    result[text_category] = dict(result.get(text_category,{}), **{item[0]:diff})

            #Get the maximum value between the sum of positives and sum of negatives
                if len(result.get(text_category,{})) > 0: 
                    removals = sum(abs(item) for item in result[text_category].values() if item < 0)
                    additions = sum(abs(item) for item in result[text_category].values() if item > 0)
                    change = min(removals, additions)
                    result[text_category] = {}
                    removals -= change
                    additions -= change

                    if removals > 0:
                        result[text_category]['remove'] = removals
                    
                    if additions > 0:
                        result[text_category]['insert'] = additions

                    if change > 0:
                        result[text_category]['change'] = change
            return result

        return None

def get_diff_count(result, lang='en'):
    """ Gets the edit type count of a diff

    Parameters
    ----------
    result : dict
        The diff API response containing inserts,removes and changes made in a Wikipedia revision.
    Returns
    -------
    dict
        a dict containing a count of edit type occurence
    """

    edit_types = {}
    section_titles = set()
    prev_text = []
    curr_text = []
    # loop through all removed nodes
    for r in result['remove']:
        text = r['text']  # wikitext of the node
        # if node is text, just check whether there's anything and retain for later
        # because all the text is processed at once at the end
        if r['type'] == 'Text' and text:
            prev_text.append(text)
            section_titles.add(r['section'])
        # non-text node: verify/fine-tune the edit type and add to results dictionary
        else:
            is_edit_type_found,edit_type = is_change_in_edit_type(r['type'],text,'')
            if is_edit_type_found:
                section_titles.add(r['section'])
                if edit_types.get(edit_type,{}):
                    edit_types[edit_type]['remove'] = edit_types[edit_type].get('remove', 0) + 1
                else:
                    edit_types[edit_type] = {'remove':1}

    for i in result['insert']:
        text = i['text']
        if i['type'] == 'Text' and text:
            curr_text.append(text)
            section_titles.add(i['section'])
        else:
            is_edit_type_found,edit_type = is_change_in_edit_type(i['type'],'',text)
            #check if edit_type in edit types dictionary
            if is_edit_type_found:
                section_titles.add(i['section'])
                if edit_types.get(edit_type,{}):
                    edit_types[edit_type]['insert'] = edit_types[edit_type].get('insert', 0) + 1
                else:
                    edit_types[edit_type] = {'insert':1}

    for c in result['change']:
        if c['prev']['type'] == c['curr']['type']:
            if c['prev']['type'] == 'Text' and c['prev']['text'] != c['curr']['text']:
                prev_text.append(c['prev']['text'])
                curr_text.append(c['curr']['text'])
                section_titles.add(c['curr']['section'])
                section_titles.add(c['prev']['section'])
            else:
                is_edit_type_found,edit_type = is_change_in_edit_type(c['prev']['type'],c['prev']['text'],c['curr']['text'])
                #check if edit_type in edit types dictionary
                if is_edit_type_found:
                    section_titles.add(c['curr']['section'])
                    section_titles.add(c['prev']['section'])
                    if edit_types.get(edit_type,{}):
                        edit_types[edit_type]['change'] = edit_types[edit_type].get('change', 0) + 1
                    else:
                        edit_types[edit_type] = {'change':1}

    for m in result['move']:
        text = m['prev']['text']
        is_edit_type_found,edit_type = is_change_in_edit_type(m['prev']['type'],text,'')
        #check if edit_type in edit types dictionary
        if is_edit_type_found:
            section_titles.add(m['curr']['section'])
            section_titles.add(m['prev']['section'])
            if edit_types.get(edit_type,{}):
                edit_types[edit_type]['move'] = edit_types[edit_type].get('move', 0) + 1
            else:
                edit_types[edit_type] = {'move':1}

    # join together all the changed section text and process
    if prev_text or curr_text:
        is_text_change_found = parse_change_text('Text', ''.join(prev_text), ''.join(curr_text), lang=lang)
        if is_text_change_found:
            for text_subcat,text_et in is_text_change_found.items():
                edit_types[text_subcat] = {}
                for et, et_count in text_et.items():
                    edit_types[text_subcat][et] = edit_types[text_subcat].get(et, 0) + et_count
    
    if section_titles:
        if 'Section' not in edit_types:
            edit_types['Section'] = {}
        sec_remove = edit_types.get('Heading', {}).get('remove', 0)
        sec_insert = edit_types.get('Heading', {}).get('insert', 0)
        sec_change = len(section_titles) - sec_remove - sec_insert
        if sec_remove:
            edit_types['Section']['remove'] = sec_remove
        if sec_insert:
            edit_types['Section']['insert'] = sec_insert
        if sec_change:
            edit_types['Section']['change'] = sec_change
    return edit_types