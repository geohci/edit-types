import mwparserfromhell as mw
import re

def is_change_in_edit_type(prev_wikitext,curr_wikitext,node_type):
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
            prev_temp_dict = { temp.split('=',maxsplit=1)[0].strip():temp.split('=',maxsplit=1)[1] for temp in prev_parsed_text.filter_templates(recursive=False)[0].params}
            curr_temp_dict = { temp.split('=',maxsplit=1)[0].strip():temp.split('=',maxsplit=1)[1] for temp in curr_parsed_text.filter_templates(recursive=False)[0].params}

            #Get the difference between template parameters. If it is more than 0, then a change occured
            if len(set(curr_temp_dict.items()) ^ set(prev_temp_dict.items())) > 0:
                return True, 'Template'

        
        if node_type == 'Media':
            prev_media = prev_parsed_text.filter_wikilinks(recursive=False)
            curr_media = curr_parsed_text.filter_wikilinks(recursive=False)

            if len(prev_media) > 0 and len(curr_media) > 0:
                if prev_media[0].text != curr_media[0].text or \
                    prev_media[0].title != curr_media[0].title:
                    return True, 'Media'

        if node_type == 'Category':
            prev_cat = prev_parsed_text.filter_wikilinks(recursive=False)
            curr_cat = curr_parsed_text.filter_wikilinks(recursive=False)

            if len(prev_cat) > 0 and len(curr_cat) > 0:
                if prev_cat[0].text != curr_cat[0].text or \
                    prev_cat[0].title != curr_cat[0].title:
                    return True, 'Category'

        if node_type == 'Wikilink':
            prev_wikilink = prev_parsed_text.filter_wikilinks(recursive=False)
            curr_wikilink = curr_parsed_text.filter_wikilinks(recursive=False)

            if len(prev_wikilink) > 0 and len(curr_wikilink) > 0:
                if prev_wikilink[0].text != curr_wikilink[0].text or \
                    prev_wikilink[0].title != curr_wikilink[0].title:
                    return True, 'Wikilink'

        if node_type == 'Text':
            prev_filtered_text = prev_parsed_text.filter_text(recursive=False)[0]
            curr_filtered_text = curr_parsed_text.filter_text(recursive=False)[0]

            if prev_filtered_text.value != curr_filtered_text.value:
                return True, 'Text'

        if node_type == 'Tag':
            #Check if a reference changes
            prev_filtered_ref = prev_parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)
            curr_filtered_ref = curr_parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)
            if len(prev_filtered_ref) > 0 and len(curr_filtered_ref) > 0:
                if prev_filtered_ref[0].contents != curr_filtered_ref[0].contents:
                    return True, 'Reference'

            #Check if a table changes

            prev_filtered_table = prev_parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)
            curr_filtered_table = curr_parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)

            if len(prev_filtered_table) > 0 and len(curr_filtered_table) > 0:
                if prev_filtered_table[0].contents != curr_filtered_table[0].contents:
                    return True, 'Table'

            #Check if a text format changes
            prev_filtered_text_formatting = prev_parsed_text.filter_tags(recursive=False)

            curr_filtered_text_formatting = curr_parsed_text.filter_tags(recursive=False)

            if len(prev_filtered_text_formatting) > 0 and len(curr_filtered_text_formatting) > 0:
                prev_filtered_text_formatting = re.findall("'{2}.*''", str(prev_filtered_text_formatting[0]))
                curr_filtered_text_formatting = re.findall("'{2}.*''", str(curr_filtered_text_formatting[0]))

                if len(prev_filtered_text_formatting) > 0 and len(curr_filtered_text_formatting) > 0:

                    if prev_filtered_text_formatting[0] != curr_filtered_text_formatting[0]:
                        return True, 'Text Formatting'


            #Check if a list changes
            prev_filtered_list = prev_parsed_text.filter_tags(matches=lambda node: node.tag in ("li","dt","dd"),recursive=False)
            curr_filtered_list = curr_parsed_text.filter_tags(matches=lambda node: node.tag in ("li","dt","dd"),recursive=False)

            if len(prev_filtered_list) > 0  and len(curr_filtered_list) > 0:
                if prev_filtered_list[0].contents != curr_filtered_list[0].contents:
                    return True, 'List'

        if node_type == 'Heading':
            prev_filtered_section = prev_parsed_text.filter_headings(recursive=False)[0]
            curr_filtered_section = curr_parsed_text.filter_headings(recursive=False)[0]

            if prev_filtered_section.title != curr_filtered_section.title:
                return True, 'Heading'

        if node_type == 'Comment':
            prev_filtered_comments = prev_parsed_text.filter_comments(recursive=False)[0]
            curr_filtered_comments = curr_parsed_text.filter_comments(recursive=False)[0]

            if prev_filtered_comments.contents != curr_filtered_comments.contents:
                return True, 'Comment'

        if node_type == 'ExternalLink':
            prev_filtered_external_links = prev_parsed_text.filter_external_links(recursive=False)[0]
            curr_filtered_external_links = curr_parsed_text.filter_external_links(recursive=False)[0]

            if prev_filtered_external_links.title != curr_filtered_external_links.title or \
                prev_filtered_external_links.url != curr_filtered_external_links.url:
                return True, 'ExternalLink'
    except Exception:
        pass

    return False, None


def is_edit_type(wikitext, node_type):
    """ Checks if wikitext is an edit type

    Parameters
    ----------
    wikitext : str
        Wikitext
    node_type: str
        Node type
    Returns
    -------
    tuple
        Tuple containing the bool,wikitext and edit type
    """
    parsed_text = mw.parse(wikitext)
    # If type field is Text
    if node_type == 'Text':
        text = parsed_text.filter_text(recursive=False)
        if len(text) > 0:
            return True, text[0], 'Text'


    elif node_type == 'Tag':
        # Check if edit type is a reference
        ref = parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)
        if len(ref) > 0:
            return True, ref[0], 'Reference'
        # Check if edit type is a table
        table = parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)
        if len(table) > 0:
            return True, table[0], 'Table'

        # Check if edit type is a text formatting
        text_format = parsed_text.filter_tags(recursive=False)
        text_format = re.findall("'{2}.*''", str(text_format[0]))
        if len(text_format) > 0:
            return True, text_format[0], 'Text Formatting'

        list_type = parsed_text.filter_tags(matches=lambda node: node.tag in ("li","dt","dd"),recursive=False)
        if len(list_type) > 0:
            return True, list_type[0], 'List'


    elif node_type == 'Comment':
        comments = parsed_text.filter_comments(recursive=False)
        if len(comments) > 0:
            return True, comments[0], 'Comment'

    elif node_type == 'Template':
        templates = parsed_text.filter_templates(recursive=False)
        if len(templates) > 0:
            return True, templates[0], 'Template'

    elif node_type == 'Heading':
        section = parsed_text.filter_headings(recursive=False)
        if len(section) > 0:
            return True, section[0], 'Section'

    elif node_type == 'Wikilink':
        wikilink = parsed_text.filter_wikilinks(recursive=False)
        if len(wikilink) > 0:
            return True, wikilink[0], 'Wikilink'

    elif node_type == 'Media':
        media = parsed_text.filter_wikilinks(recursive=False)
        if len(media) > 0:
            return True, media[0], 'Media'

    elif node_type == 'Category':
        category = parsed_text.filter_wikilinks(recursive=False)
        if len(category) > 0:
            return True, category[0], 'Category'

    elif node_type == 'ExternalLink':
        external_link = parsed_text.filter_external_links(recursive=False)
        if len(external_link) > 0:
            return True, external_link[0], 'External Link'
    return False, None, None

def get_diff_count(result):
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
    for r in result['remove']:
        text = r['text']
        is_edit_type_found,wikitext,edit_type = is_edit_type(text,r['type'])
        if is_edit_type_found:
            if edit_types.get(edit_type,{}):
                edit_types[edit_type]['remove'] = edit_types[edit_type].get('remove', 0) + 1
            else:
                edit_types[edit_type] = {'remove':1}

    for i in result['insert']:
        text = i['text']
        is_edit_type_found,wikitext,edit_type = is_edit_type(text,i['type'])
        #check if edit_type in edit types dictionary
        if is_edit_type_found:
            if edit_types.get(edit_type,{}):
                edit_types[edit_type]['insert'] = edit_types[edit_type].get('insert', 0) + 1
            else:
                edit_types[edit_type] = {'insert':1}

    for c in result['change']:
        if c['prev']['type'] == c['curr']['type']:
            is_edit_type_found,edit_type = is_change_in_edit_type(c['prev']['text'],c['curr']['text'],c['prev']['type'])
            #check if edit_type in edit types dictionary
            if is_edit_type_found:
                if edit_types.get(edit_type,{}):
                    edit_types[edit_type]['change'] = edit_types[edit_type].get('change', 0) + 1
                else:
                    edit_types[edit_type] = {'change':1}

    for m in result['move']:
        text = m['text']        
        is_edit_type_found,edit_type = is_edit_type(text, m['type'])
                
        #check if edit_type in edit types dictionary
        if is_edit_type_found:
            if edit_types.get(edit_type,{}):
                edit_types[edit_type]['move'] = edit_types[edit_type].get('move', 0) + 1
            else:
                edit_types[edit_type] = {'move':1}

    return edit_types