import re  # not technically needed because part of edittypes.tokenizer but that's confusing

import mwparserfromhell as mw
from edittypes.tokenizer import *

NON_ENGLISH_UNICODE = '''[\u0609\u060a\u060c\u060d\u061b\u061e\u061f\u066a\u066b\u066c
\u070a\u070b\u070c\u070d\u07f7\u07f8\u07f9\u0830\u0831\u0832\u0833\u0834\u0835
\u0836\u0837\u0838\u0839\u083a\u083b\u083c\u083d\u083e\u085e\u0964
\u0965\u0970\u09fd\u0a76\u0af0\u0c77\u0c84\u0df4
\u0e4f\u0e5a\u0e5b\u0f04\u0f05\u0f06\u0f07\u0f08\u0f09\u0f0a\u0f0b
\u0f0c\u0f0d\u0f0e\u0f0f\u0f10\u0f11\u0f12\u0f14\u0f85\u0fd0\u0fd1
\u0fd2\u0fd3\u0fd4\u0fd9\u0fda\u104a\u104b\u104c\u104d\u104e\u104f
\u10fb\u1360\u1361\u1362\u1363\u1364\u1365\u1366\u1367\u1368\u166e
\u16eb\u16ec\u16ed\u1735\u1736\u17d4\u17d5\u17d6\u17d8\u17d9\u17da
\u1800\u1801\u1802\u1803\u1804\u1805\u1807\u1808\u1809\u180a\u1944
\u1945\u1a1e\u1a1f\u1aa0\u1aa1\u1aa2\u1aa3\u1aa4\u1aa5\u1aa6\u1aa8
\u1aa9\u1aaa\u1aab\u1aac\u1aad\u1b5a\u1b5b\u1b5c\u1b5d\u1b5e\u1b5f
\u1b60\u1bfc\u1bfd\u1bfe\u1bff\u1c3b\u1c3c\u1c3d\u1c3e\u1c3f\u1c7e
\u1c7f\u1cc0\u1cc1\u1cc2\u1cc3\u1cc4\u1cc5\u1cc6\u1cc7\u1cd3\u2016
\u2017\u2020\u2021\u2022\u2023\u2025\u2026\u2027\u2030\u2031
\u2032\u2033\u2034\u2035\u2036\u2037\u2038\u203b\u203c\u203d\u203e
\u2041\u2042\u2043\u2047\u2048\u2049\u204a\u204b\u204c\u204d\u204e
\u204f\u2050\u2051\u2053\u2055\u2056\u2057\u2058\u2059\u205a\u205b
\u205c\u205d\u205e\u2cf9\u2cfa\u2cfb\u2cfc\u2cfe\u2cff]'''
ENGLISH_UNICODE = '[\u00b7\u00bf]'

# Initialize tokenizer class
TOKENIZER = Tokenizer(ENGLISH_UNICODE, NON_ENGLISH_UNICODE)
    
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
            prev_temp_dict = dict(prev_temp_dict, **{'template_name':prev_parsed_text.filter_templates(recursive=False)[0].title})
            
            curr_temp_dict = { temp.split('=',maxsplit=1)[0].strip():temp.split('=',maxsplit=1)[1] for temp in curr_parsed_text.filter_templates(recursive=False)[0].params}
            curr_temp_dict = dict(curr_temp_dict, **{'template_name':prev_parsed_text.filter_templates(recursive=False)[0].title})
            
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

        if node_type == 'Reference':
            #Check if a reference changes
            prev_filtered_ref = prev_parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)
            curr_filtered_ref = curr_parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)
            if len(prev_filtered_ref) > 0 and len(curr_filtered_ref) > 0:
                if prev_filtered_ref[0].contents != curr_filtered_ref[0].contents:
                    return True, 'Reference'

        if node_type == 'Table':
            #Check if a table changes

            prev_filtered_table = prev_parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)
            curr_filtered_table = curr_parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)

            if len(prev_filtered_table) > 0 and len(curr_filtered_table) > 0:
                if prev_filtered_table[0].contents != curr_filtered_table[0].contents:
                    return True, 'Table'

        if node_type == 'Text Formatting':
            #Check if a text format changes
            prev_filtered_text_formatting = prev_parsed_text.filter_tags(matches=lambda node: node.tag in ('b', 'i', 's', 'u', 'del', 'ins','hr','pre', 'nowiki','small', 'big', 'sub', 'sup'),recursive=False)

            curr_filtered_text_formatting = curr_parsed_text.filter_tags(matches=lambda node: node.tag in ('b', 'i', 's', 'u', 'del', 'ins','hr','pre', 'nowiki','small', 'big', 'sub', 'sup'),recursive=False)

            if len(prev_filtered_text_formatting) > 0 and len(curr_filtered_text_formatting) > 0:
                if prev_filtered_text_formatting[0] != curr_filtered_text_formatting[0]:
                    return True, 'Text Formatting'

        if node_type == 'List':
            #Check if a list changes
            prev_filtered_list = prev_parsed_text.filter_tags(matches=lambda node: node.tag in ("li","dt","dd"),recursive=False)
            curr_filtered_list = curr_parsed_text.filter_tags(matches=lambda node: node.tag in ("li","dt","dd"),recursive=False)

            if len(prev_filtered_list) > 0  and len(curr_filtered_list) > 0:
                if prev_filtered_list[0].contents != curr_filtered_list[0].contents:
                    return True, 'List'

        if node_type == 'Table Element':
            #Check if a table element changes

            prev_filtered_table = prev_parsed_text.filter_tags(matches=lambda node: node.tag in ('th', 'tr', 'td'),recursive=False)
            curr_filtered_table = curr_parsed_text.filter_tags(matches=lambda node: node.tag in ('th', 'tr', 'td'),recursive=False)

            if len(prev_filtered_table) > 0 and len(curr_filtered_table) > 0:
                if prev_filtered_table[0].contents != curr_filtered_table[0].contents:
                    return True, 'Table'

        if node_type == 'Gallery':
            #Check if a list changes
            prev_filtered_gallery = prev_parsed_text.filter_tags(matches=lambda node: node.tag == 'Gallery',recursive=False)
            curr_filtered_gallery = curr_parsed_text.filter_tags(matches=lambda node: node.tag == 'Gallery',recursive=False)

            if len(prev_filtered_gallery) > 0  and len(curr_filtered_gallery) > 0:
                if prev_filtered_gallery[0].contents != curr_filtered_gallery[0].contents:
                    return True, 'Gallery'

        if 'Tag' in node_type:
            #Check if a tag changes
            prev_filtered_tag = prev_parsed_text.filter_tags(recursive=False)
            curr_filtered_tag = curr_parsed_text.filter_tags(recursive=False)

            if len(prev_filtered_tag) > 0  and len(curr_filtered_tag) > 0:
                if prev_filtered_tag[0].contents != curr_filtered_tag[0].contents:
                    return True, node_type

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
            return True, 'Text'

    elif node_type == 'Reference':
        # Check if edit type is a reference
        ref = parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)
        if len(ref) > 0:
            return True, 'Reference'

    elif node_type == 'List':
        list_type = parsed_text.filter_tags(matches=lambda node: node.tag in ("li","dt","dd"),recursive=False)
        if len(list_type) > 0:
            return True, 'List'

    elif node_type == 'Table':
        # Check if edit type is a table
        table = parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)
        if len(table) > 0:
            return True, 'Table'

    elif 'Tag' in node_type:
        tag = parsed_text.filter_tags(recursive=False)
        if len(tag) > 0:
            return True, node_type

    elif node_type == 'Text Formatting':
        text_format = parsed_text.filter_tags(matches=lambda node: node.tag in ('b', 'i', 's', 'u', 'del', 'ins','hr','pre', 'nowiki','small', 'big', 'sub', 'sup'),recursive=False)
        if len(text_format) > 0:
            return True, 'Text Formatting'

    elif node_type == 'Table Element':
        table_element = parsed_text.filter_tags(matches=lambda node: node.tag in ('th', 'tr', 'td'),recursive=False)
        if len(table_element) > 0:
            return True, 'Table Element'

    elif node_type == 'Gallery':
        gallery = parsed_text.filter_tags(matches=lambda node: node.tag == 'gallery',recursive=False)
        if len(gallery) > 0:
            return True, 'Gallery'
    elif node_type == 'Comment':
        comments = parsed_text.filter_comments(recursive=False)
        if len(comments) > 0:
            return True, 'Comment'

    elif node_type == 'Template':
        templates = parsed_text.filter_templates(recursive=False)
        if len(templates) > 0:
            return True, 'Template'

    elif node_type == 'Heading':
        section = parsed_text.filter_headings(recursive=False)
        if len(section) > 0:
            return True, 'Section'

    elif node_type == 'Wikilink':
        wikilink = parsed_text.filter_wikilinks(recursive=False)
        if len(wikilink) > 0:
            return True, 'Wikilink'

    elif node_type == 'Media':
        media = parsed_text.filter_wikilinks(recursive=False)
        if len(media) > 0:
            return True, 'Media'

    elif node_type == 'Category':
        category = parsed_text.filter_wikilinks(recursive=False)
        if len(category) > 0:
            return True, 'Category'

    elif node_type == 'ExternalLink':
        external_link = parsed_text.filter_external_links(recursive=False)
        if len(external_link) > 0:
            return True, 'External Link'
    return False, None


def parse_change_text(node_type, prev_wikitext='',curr_wikitext=''):
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
            prev_tokenizer = TOKENIZER.tokenize_and_get_occurence(prev_wikitext)
            curr_tokenizer = TOKENIZER.tokenize_and_get_occurence(curr_wikitext)

            #Gets the list of differences. Counts both added and removed whitespaces
            whitespace_items_diff_list = list(set(curr_tokenizer['whitespace_count'].items())  ^ set(prev_tokenizer['whitespace_count'].items()))
            punctuation_items_diff_list = list(set(curr_tokenizer['punctuation_count'].items())  ^ set(prev_tokenizer['punctuation_count'].items()))
            word_items_diff_list = list(set(curr_tokenizer['word_count'].items())  ^ set(prev_tokenizer['word_count'].items()))
            sentence_items_diff_list = list(set(curr_tokenizer['sentence_count'].items())  ^ set(prev_tokenizer['sentence_count'].items()))
            paragraphs_items_diff_list = list(set(curr_tokenizer['paragraph_count'].items())  ^ set(prev_tokenizer['paragraph_count'].items()))

            result = {}


            #Sort whitespaces
            for item in whitespace_items_diff_list:
                if item[0] not in prev_tokenizer['whitespace_count'].keys() and item[0] in curr_tokenizer['whitespace_count'].keys():
                    if item[1] > 1:
                        result['Whitespace'] = dict(result.get('Whitespace',{}),**{item[0]:item[1]})
                    else:
                        result['Whitespace'] = dict(result.get('Whitespace',{}), **{item[0]:1})
                elif item[0] in prev_tokenizer['whitespace_count'].keys() and item[0] in curr_tokenizer['whitespace_count'].keys():
                    diff = curr_tokenizer['whitespace_count'][item[0]] - prev_tokenizer['whitespace_count'][item[0]]
                    result['Whitespace'] = dict(result.get('Whitespace',{}).get('change'), **{item[0]:diff})
                else:
                    if item[1] > 1:
                       result['Whitespace'] = dict(result.get('Whitespace',{}),**{item[0]:-item[1]})
                    else:
                        result['Whitespace'] = dict(result.get('Whitespace',{}), **{item[0]:-1})

            #Sort punctuations
            for item in punctuation_items_diff_list:
                if item[0] not in prev_tokenizer['punctuation_count'].keys() and item[0] in curr_tokenizer['punctuation_count'].keys():
                    if item[1] > 1:
                       result['Punctuation'] = dict(result.get('Punctuation',{}),**{item[0]:item[1]})
                    else:
                        result['Punctuation'] = dict(result.get('Punctuation',{}), **{item[0]:1})

                elif item[0] in prev_tokenizer['punctuation_count'].keys() and item[0] in curr_tokenizer['punctuation_count'].keys():
                    diff = curr_tokenizer['punctuation_count'][item[0]] - prev_tokenizer['punctuation_count'][item[0]]
                    result['Punctuation'] = dict(result.get('Punctuation',{}), ** {item[0]:diff})
                else:
                    if item[1] > 1:
                       result['Punctuation'] = dict(result.get('Punctuation',{}),**{item[0]:-item[1]})
                    else:
                        result['Punctuation'] = dict(result.get('Punctuation',{}), **{item[0]:-1})
                    

            #Sort words
            for item in word_items_diff_list:
                if item[0] not in prev_tokenizer['word_count'].keys() and item[0] in curr_tokenizer['word_count'].keys():
                    if item[1] > 1:
                       result['Word'] = dict(result.get('Word',{}),**{item[0]:item[1]})
                    else:
                        result['Word'] = dict(result.get('Word',{}), **{item[0]:1})
                elif item[0] in prev_tokenizer['word_count'].keys() and item[0] in curr_tokenizer['word_count'].keys():
                    diff = curr_tokenizer['word_count'][item[0]] - prev_tokenizer['word_count'][item[0]]
                    result['Word'] = dict(result.get('Word',{}), **{item[0]:diff})
                else:
                    if item[1] > 1:
                       result['Word'] = dict(result.get('Word',{}),**{item[0]:-item[1]})
                    else:
                        result['Word'] = dict(result.get('Word',{}), **{item[0]:-1})
                    

            #Sort sentences
            for item in sentence_items_diff_list:
                if item[0] not in prev_tokenizer['sentence_count'].keys() and item[0] in curr_tokenizer['sentence_count'].keys():
                    if item[1] > 1:
                       result['Sentence'] = dict(result.get('Sentence',{}),**{item[0]:item[1]})
                    else:
                        result['Sentence'] = dict(result.get('Sentence',{}), **{item[0]:1})

                elif item[0] in prev_tokenizer['sentence_count'].keys() and item[0] in curr_tokenizer['sentence_count'].keys():
                    diff = curr_tokenizer['sentence_count'][item[0]] - prev_tokenizer['sentence_count'][item[0]]
                    result['Sentence'] = dict(result.get('Sentence',{}), **{item[0]:diff})
                else:
                    if item[1] > 1:
                       result['Sentence'] = dict(result.get('Sentence',{}),**{item[0]:-item[1]})
                    else:
                        result['Sentence'] = dict(result.get('Sentence',{}),** {item[0]:-1})


            #Sort paragraphs
            for item in paragraphs_items_diff_list:
                if item[0] not in prev_tokenizer['paragraph_count'].keys() and item[0] in curr_tokenizer['paragraph_count'].keys():
                    if item[1] > 1:
                       result['Paragraph'] = dict(result.get('Paragraph',{}),**{item[0]:item[1]})
                    else:
                        result['Paragraph'] = dict(result.get('Paragraph',{}) , **{item[0]:1})
                elif item[0] in prev_tokenizer['paragraph_count'].keys() and item[0] in curr_tokenizer['paragraph_count'].keys():
                    diff = curr_tokenizer['paragraph_count'][item[0]] - prev_tokenizer['paragraph_count'][item[0]]
                    result['Paragraph'] = dict(result.get('Paragraph',{}),**{item[0]:diff})
                else:
                    if item[1] > 1:
                       result['Paragraph'] = dict(result.get('Paragraph',{}),**{item[0]:-item[1]})
                    else:
                        result['Paragraph'] = dict(result.get('Paragraph',{}), **{item[0]:-1})

            #Get the maximum value between the sum of positives and sum of negatives
            if len(result.get('Whitespace',{})) > 0:
                whitespace_removals = sum(abs(item) for item in result['Whitespace'].values() if item < 0)
                whitespace_additions = sum(abs(item) for item in result['Whitespace'].values() if item > 0)
                whitespace_change = min(whitespace_removals, whitespace_additions)
                if whitespace_change > 0:
                    whitespace_change_diff = whitespace_removals - whitespace_additions
                    if whitespace_change_diff > 0:
                        result['Whitespace'] = {'remove':abs(whitespace_change_diff),'change':whitespace_change}
                    elif whitespace_change_diff == 0:
                        result['Whitespace'] = {'change':whitespace_change}
                    else:
                        result['Whitespace'] = {'insert':abs(whitespace_change_diff),'change':whitespace_change}

                else:
                    result['Whitespace'] = {edittype:max(whitespace_removals, whitespace_additions)}
            if len(result.get('Punctuation',{})) > 0:
                punctuation_removals = sum(abs(item) for item in result['Punctuation'].values() if item < 0)
                punctuation_additions = sum(abs(item) for item in result['Punctuation'].values() if item > 0)
                punctuation_change = min(punctuation_removals, punctuation_additions)
                if punctuation_change > 0:
                    punctuation_change_diff = punctuation_removals - punctuation_additions
                    if punctuation_change_diff > 0:
                        result['Punctuation'] = {'remove':abs(punctuation_change_diff),'change':punctuation_change}
                    elif punctuation_change_diff == 0:
                        result['Punctuation'] = {'change':punctuation_change}
                    else:
                        result['Punctuation'] = {'insert':abs(punctuation_change_diff),'change':punctuation_change}

                else:
                    result['Punctuation'] = {edittype:max(punctuation_removals, punctuation_additions)}
            if len(result.get('Word',{})) > 0:
                word_removals = sum(abs(item) for item in result['Word'].values() if item < 0)
                word_additions = sum(abs(item) for item in result['Word'].values() if item > 0)
                word_change = min(word_removals, word_additions)
                if word_change > 0:
                    word_change_diff = word_removals - word_additions
                    if word_change_diff > 0:
                        result['Word'] = {'remove':abs(word_change_diff),'change':word_change}
                    elif word_change_diff == 0:
                        result['Word'] = {'change':word_change}
                    else:
                        result['Word'] = {'insert':abs(word_change_diff), 'change':word_change}

                else:
                    result['Word'] = {edittype:max(word_removals, word_additions)}
            if len(result.get('Sentence',{})) > 0:
                sentence_removals = sum(abs(item) for item in result['Sentence'].values() if item < 0)
                sentence_additions = sum(abs(item) for item in result['Sentence'].values() if item > 0)
                sentence_change = min(sentence_removals, sentence_additions)
                if sentence_change > 0:
                    sentence_change_diff = sentence_removals - sentence_additions
                    if sentence_change_diff > 0:
                        result['Sentence'] = {'remove':abs(sentence_change_diff),'change':sentence_change}
                    elif sentence_change_diff == 0:
                        result['Sentence'] = {'change':sentence_change}             
                    else:
                        result['Sentence'] = {'insert':abs(sentence_change_diff),'change':sentence_change}

                else:
                    result['Sentence'] = {edittype:max(sentence_removals, sentence_additions)}

            if len(result.get('Paragraph',{})) > 0:
                paragraph_removals = sum(abs(item) for item in result['Paragraph'].values() if item < 0)
                paragraph_additions = sum(abs(item) for item in result['Paragraph'].values() if item > 0)
                paragraph_change = min(paragraph_removals, paragraph_additions)
                if paragraph_change > 0:
                    paragraph_change_diff = paragraph_removals - paragraph_additions
                    if paragraph_change_diff > 0:
                        result['Paragraph'] = {'remove':paragraph_removals,'change':paragraph_change}
                    elif paragraph_change_diff == 0:
                        result['Paragraph'] = {'change':paragraph_change}
                    else:
                        result['Paragraph'] = {'insert':paragraph_additions,'change':paragraph_change}

                else:
                    result['Paragraph'] = {edittype:max(paragraph_removals, paragraph_additions)}
            return result

        return None

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
        if r['type'] == 'Text':
            is_text_change_found = parse_change_text(r['type'], text,'')
            if is_text_change_found:
                for k,v in is_text_change_found.items():
                    for v_key, v_val in v.items():
                        if len(edit_types.get(k,{})) > 0:
                            edit_types[k] = dict(edit_types.get(k, {}),**{v_key:edit_types.get(k,{}).get(v_key,0)})
                        else:
                            edit_types[k] = dict(edit_types.get(k, {}), **v)
        else:
            is_edit_type_found,edit_type = is_edit_type(text,r['type'])
            if is_edit_type_found:
                if edit_types.get(edit_type,{}):
                    edit_types[edit_type]['remove'] = edit_types[edit_type].get('remove', 0) + 1
                else:
                    edit_types[edit_type] = {'remove':1}
        

    for i in result['insert']:
        text = i['text']
        if i['type'] == 'Text':
            is_text_change_found = parse_change_text(i['type'], text,'')
            if is_text_change_found:
                for k,v in is_text_change_found.items():
                    for v_key, v_val in v.items():
                        if len(edit_types.get(k,{})) > 0:
                                edit_types[k] = dict(edit_types.get(k, {}),**{v_key:edit_types.get(k,{}).get(v_key,0)})
                        else:
                            edit_types[k] = dict(edit_types.get(k, {}), **v)
        else:
            is_edit_type_found,edit_type = is_edit_type(text,i['type'])
            #check if edit_type in edit types dictionary
            if is_edit_type_found:
                if edit_types.get(edit_type,{}):
                    edit_types[edit_type]['insert'] = edit_types[edit_type].get('insert', 0) + 1
                else:
                    edit_types[edit_type] = {'insert':1}

    for c in result['change']:
        if c['prev']['type'] == c['curr']['type']:
            if c['prev']['type'] == 'Text':
                is_text_change_found = parse_change_text(c['prev']['type'], c['prev']['text'],c['curr']['text'])
                if is_text_change_found:
                    for k,v in is_text_change_found.items():
                        for v_key, v_val in v.items():
                            if len(edit_types.get(k,{})) > 0:
                                edit_types[k] = dict(edit_types.get(k, {}),**{v_key:edit_types.get(k,{}).get(v_key,0)})
                            else:
                                edit_types[k] = dict(edit_types.get(k, {}), **v)
            else:
                is_edit_type_found,edit_type = is_change_in_edit_type(c['prev']['text'],c['curr']['text'],c['prev']['type'])
                #check if edit_type in edit types dictionary
                if is_edit_type_found:
                    if edit_types.get(edit_type,{}):
                        edit_types[edit_type]['change'] = edit_types[edit_type].get('change', 0) + 1
                    else:
                        edit_types[edit_type] = {'change':1}

    for m in result['move']:
        text = m['prev']['text']       
        is_edit_type_found,edit_type = is_edit_type(text, m['prev']['type'])
        #check if edit_type in edit types dictionary
        if is_edit_type_found:
            if edit_types.get(edit_type,{}):
                edit_types[edit_type]['move'] = edit_types[edit_type].get('move', 0) + 1
            else:
                edit_types[edit_type] = {'move':1}

    return edit_types