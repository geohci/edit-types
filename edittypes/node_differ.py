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
            prev_filtered_ref = prev_parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)[0]
            curr_filtered_ref = curr_parsed_text.filter_tags(matches=lambda node: node.tag == "ref",recursive=False)[0]

            if prev_filtered_ref.contents != curr_filtered_ref.contents:
                return True, 'Reference'

            #Check if a table changes
            prev_filtered_table = prev_parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)[0]
            curr_filtered_table = curr_parsed_text.filter_tags(matches=lambda node: node.tag == "table",recursive=False)[0]

            if prev_filtered_table.contents != curr_filtered_table.contents:
                return True, 'Table'

            #Check if a text format chnages
            prev_filtered_text_formatting = prev_parsed_text.filter_tags(recursive=False)[0]
            prev_filtered_text_formatting = re.findall("'{2}.*''", str(prev_filtered_text_formatting[0]))[0]

            curr_filtered_text_formatting = curr_parsed_text.filter_tags(recursive=False)[0]
            curr_filtered_text_formatting = re.findall("'{2}.*''", str(curr_filtered_text_formatting[0]))[0]

            if prev_filtered_text_formatting != curr_filtered_text_formatting:
                return True, 'Text Formatting'


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

def is_nested_node_in_change(prev_wikitext,curr_wikitext, node_type):
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
        Tuple containing the bool and list containing tuple of edit types and edit actions e.g (True,[('remove','Template')]
    """
    node_type_list = []
    try:
        if node_type == 'Template':
            node_compare_list = []
            #Pass in filter statements
            prev_temp_dict = { temp.split('=',maxsplit=1)[0].strip():temp.split('=',maxsplit=1)[1] for temp in prev_parsed_text.filter_templates(recursive=False)[0].params}
            curr_temp_dict = { temp.split('=',maxsplit=1)[0].strip():temp.split('=',maxsplit=1)[1] for temp in curr_parsed_text.filter_templates(recursive=False)[0].params}
            
            #Check If there is a symmetric difference between the previous and current parameters of a template
            diff_dict = set(curr_temp_dict.items()) ^ set(prev_temp_dict.items())
            
            if len(diff_dict) > 0:
                #Convert set of diffrences into list
                diff_list = list(diff_dict)
                for item in diff_list:
                    #if previous template parameter changed, this means a removal occured
                    if prev_temp_dict.get(item[0],{}) == item[1]:
                        #Checks if there is an identical parameter in diff list
                        for item_copy in diff_list:
                            if item != item_copy and item[0] == item_copy[0]: 
                                node_compare_list.append(('remove',item))

                                templates = item[1].filter_templates()
                                if len(templates) > 0:
                                    node_type_list.append(('remove','Template'))

                                refs = item[1].filter_tags(matches=lambda node: node.tag == "ref")
                                if len(refs) > 0:
                                    node_type_list.append(('remove','Reference'))

                                table = item[1].filter_tags(matches=lambda node: node.tag == "table")
                                if len(table) > 0:
                                    node_type_list.append(('remove','Table'))
                                
                                #Find the solution for this. Apply regex maybe
                                formatting = item[1].filter_tags()
                                if len(formatting) > 0:
                                    node_type_list.append(('remove','Text Formatting'))
                                
                                wikilinks = item[1].filter_wikilinks()
                                if len(wikilinks) > 0:
                                    node_type_list.append(('remove','Wikilink'))

                                comments = item[1].filter_comments()
                                if len(comments) > 0:
                                    node_type_list.append(('remove','Comments'))

                                external_links = item[1].filter_external_links()
                                if len(external_links) > 0:
                                    node_type_list.append(('remove','ExternalLink'))


                        if ('remove',item) not in node_compare_list:
                            node_compare_list.append(('remove',item))  
                            
                            templates = item[1].filter_templates()
                            if len(templates) > 0:
                                node_type_list.append(('remove','Template'))

                            refs = item[1].filter_tags(matches=lambda node: node.tag == "ref")
                            if len(refs) > 0:
                                node_type_list.append(('remove','Reference'))

                            table = item[1].filter_tags(matches=lambda node: node.tag == "table")
                            if len(table) > 0:
                                node_type_list.append(('remove','Table'))
                            
                            #Find the solution for this. Apply regex maybe
                            formatting = item[1].filter_tags()
                            if len(formatting) > 0:
                                node_type_list.append(('remove','Text Formatting'))
                            
                            wikilinks = item[1].filter_wikilinks()
                            if len(wikilinks) > 0:
                                node_type_list.append(('remove','Wikilink'))

                            comments = item[1].filter_comments()
                            if len(comments) > 0:
                                node_type_list.append(('remove','Comments'))

                            external_links = item[1].filter_external_links()
                            if len(external_links) > 0:
                                node_type_list.append(('remove','ExternalLink'))

            
                    if curr_temp_dict.get(item[0],{}) == item[1]:
                        for item_copy in diff_list:
                            if item != item_copy and item[0] == item_copy[0]:
                                node_list.append(('insert',item))
                                
                                templates = item[1].filter_templates()
                                if len(templates) > 0:
                                    node_type_list.append(('remove','Template'))

                                refs = item[1].filter_tags(matches=lambda node: node.tag == "ref")
                                if len(refs) > 0:
                                    node_type_list.append(('remove','Reference'))

                                table = item[1].filter_tags(matches=lambda node: node.tag == "table")
                                if len(table) > 0:
                                    node_type_list.append(('remove','Table'))
                                
                                #Find the solution for this. Apply regex maybe
                                formatting = item[1].filter_tags()
                                if len(formatting) > 0:
                                    node_type_list.append(('remove','Text Formatting'))
                                
                                wikilinks = item[1].filter_wikilinks()
                                if len(wikilinks) > 0:
                                    node_type_list.append(('remove','Wikilink'))

                                comments = item[1].filter_comments()
                                if len(comments) > 0:
                                    node_type_list.append(('remove','Comments'))

                                external_links = item[1].filter_external_links()
                                if len(external_links) > 0:
                                    node_type_list.append(('remove','ExternalLink'))

                            if ('insert',item) not in node_list:
                                node_list.append(('insert',item))
                                
                                templates = item[1].filter_templates()
                                if len(templates) > 0:
                                    node_type_list.append(('remove','Template'))

                                refs = item[1].filter_tags(matches=lambda node: node.tag == "ref")
                                if len(refs) > 0:
                                    node_type_list.append(('remove','Reference'))

                                table = item[1].filter_tags(matches=lambda node: node.tag == "table")
                                if len(table) > 0:
                                    node_type_list.append(('remove','Table'))
                                
                                #Find the solution for this. Apply regex maybe
                                formatting = item[1].filter_tags()
                                if len(formatting) > 0:
                                    node_type_list.append(('remove','Text Formatting'))
                                
                                wikilinks = item[1].filter_wikilinks()
                                if len(wikilinks) > 0:
                                    node_type_list.append(('remove','Wikilink'))

                                comments = item[1].filter_comments()
                                if len(comments) > 0:
                                    node_type_list.append(('remove','Comments'))

                                external_links = item[1].filter_external_links()
                                if len(external_links) > 0:
                                    node_type_list.append(('remove','ExternalLink'))
        
        if node_type == 'Tag':
            node_compare_list = []
            prev_parsed_text = mw.parse(prev_wikitext).filter_tags(recursive=False)[0].contents
            curr_parsed_text = mw.parse(curr_wikitext).filter_tags(recursive=False)[0].contents

            #Compare prev filtered templates with current
            prev_templates = [ str(template) for template in prev_parsed_text.filter_templates()]
            curr_templates = [str(template) for template in curr_parsed_text.filter_templates()]

            diff_list = list(set(prev_templates) ^ set(curr_templates))

            for item in diff_list:
                #If the template changes, it means parameters got changed and template name remains same
                r = re.compile(f".*{item.split('|')[0].split(' ')[0]}")
                if len(list(filter(r.match, node_compare_list))) == 0:
                    if len(list(filter(r.match, prev_templates))) > 0 and  len(list(filter(r.match, curr_templates))) > 0:
                        node_type_list.append(('change', 'Template'))
                        node_compare_list.append(item)
                    else:
                        if item in prev_templates and item not in curr_templates:
                            node_type_list.append(('remove', 'Template'))
                            node_compare_list.append(item)
                        if item not in prev_templates and item in curr_templates:
                            node_type_list.append(('insert', 'Template'))
                            node_compare_list.append(item)
                

            #Compare prev filtered refs with current
            prev_refs = [ str(refs) for refs in prev_parsed_text.filter_tags(matches=lambda node: node.tag == "ref")]
            curr_refs = [ str(refs) for refs in curr_parsed_text.filter_tags(matches=lambda node: node.tag == "ref")]

            diff_list = list(set(prev_refs) ^ set(curr_refs))

            for item in diff_list:
                if item in prev_refs and item not in curr_refs:
                    node_type_list.append(('remove', 'Reference'))
                if item not in prev_refs and item in curr_refs:
                    node_type_list.append(('insert', 'Reference'))

            #Find the solution for this. Apply regex maybe
            prev_formatting = [ str(text_form) for text_form in prev_parsed_text.filter_tags() ]
            curr_formatting = [str(text_form) for text_form in curr_parsed_text.filter_tags() ]

            diff_list = list(set(prev_formatting) ^ set(curr_formatting))

            for item in diff_list:
                if item in prev_formatting and item not in curr_formatting:
                    node_type_list.append(('remove', 'Text Formatting'))
                if item not in prev_formatting and item in curr_formatting:
                    node_type_list.append(('insert', 'Text Formatting'))

            prev_wikilinks = [ str(wikilink) for wikilink in prev_parsed_text.filter_wikilinks()]
            curr_wikilinks = [ str(wikilink) for wikilink in curr_parsed_text.filter_wikilinks()]

            diff_list = list(set(prev_wikilinks) ^ set(curr_wikilinks))
            for item in diff_list:
                if item in prev_wikilinks and item not in curr_wikilinks:
                    node_type_list.append(('remove', 'Wikilink'))
                if item not in prev_wikilinks and item in curr_wikilinks:
                    node_type_list.append(('insert', 'Wikilink'))


            prev_comments = [ str(comment) for comment in prev_parsed_text.filter_comments()]
            curr_comments = [str(comment) for comment in curr_parsed_text.filter_comments()]

            diff_list = list(set(prev_comments) ^ set(curr_comments))

            for item in diff_list:
                if item in prev_comments and item not in curr_comments:
                    node_type_list.append(('remove', 'Comments'))
                if item not in prev_comments and item in curr_comments:
                    node_type_list.append(('insert', 'Comments'))

            prev_external_links = [ str(external) for external in prev_parsed_text.filter_external_links()]
            curr_external_links = [ str(external) for external in curr_parsed_text.filter_external_links()]

            diff_list = list(set(prev_external_links) ^ set(curr_external_links))

            for item in diff_list:
                if item in prev_external_links and item not in curr_external_links:
                    node_type_list.append(('remove', 'ExternalLink'))
                if item not in prev_external_links and item in curr_external_links:
                    node_type_list.append(('insert', 'ExternalLink'))
        if len(node_type_list) > 0:
            return True, node_type_list

    except Exception as e:
        return False, e        
    

    return False, node_type_list

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
    sections_affected = set()
    for r in result['remove']:
        sections_affected.add(r["section"])
    for i in result['insert']:
        sections_affected.add(i["section"])
    for c in result['change']:
        sections_affected.add(c['prev']["section"])

    edit_types = {}
    for s in sections_affected:
        for r in result['remove']:
            if r["section"] == s:
                text = r['text']
                is_edit_type_found,wikitext,edit_type = is_edit_type(text,r['type'])
                if is_edit_type_found:
                    if edit_types.get(edit_type,{}):
                        edit_types[edit_type]['remove'] = edit_types[edit_type].get('remove', 0) + 1
                    else:
                        edit_types[edit_type] = {'remove':1}

        for i in result['insert']:
            if i["section"] == s:
                text = i['text']
                is_edit_type_found,wikitext,edit_type = is_edit_type(text,i['type'])
                #check if edit_type in edit types dictionary
                if is_edit_type_found:
                    if edit_types.get(edit_type,{}):
                        edit_types[edit_type]['insert'] = edit_types[edit_type].get('insert', 0) + 1
                    else:
                        edit_types[edit_type] = {'insert':1}

        for c in result['change']:
            
            if c["prev"]["section"] == s:
                if c['prev']['type'] == c['curr']['type']:
                    text = c['curr']['text']
                    is_edit_type_found,edit_type = is_change_in_edit_type(c['prev']['text'],c['curr']['text'],c['prev']['type'])
                    is_nested_node_found, nested_nodes = is_nested_node_in_change(c['prev']['text'],c['curr']['text'],c['prev']['type'])
                    #check if edit_type in edit types dictionary
                    if is_edit_type_found:
                        if edit_types.get(edit_type,{}):
                            edit_types[edit_type]['change'] = edit_types[edit_type].get('change', 0) + 1
                        else:
                            edit_types[edit_type] = {'change':1}
                            
                    if is_nested_node_found:
                        for node in nested_nodes:
                            if edit_types.get(node[1],{}):
                                edit_types[node[1]][node[0]] = edit_types[node[1]].get(node[0], 0) + 1
                            else:
                                edit_types[node[1]] = {node[0]:1}

    return edit_types