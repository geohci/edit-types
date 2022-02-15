from context import nd
from context import td

# Basic wikitext to play with that has most of the things we're interested in (image, categories, templates, etc.)
# Source: https://en.wikipedia.org/wiki/Karl_Aigen
# NOTE: I add the "==Lede==" section at the top as a useful preprocessing step
prev_wikitext = """{{Short description|Austrian painter}}
'''Karl Josef Aigen''' (8 October 1684 – 22 October 1762) was a landscape painter, born at [[Olomouc]].

==Life==
[[File:Carl Aigen Fischmarkt.jpg|thumb|''Fischmarkt'' by Karl Aigen]]
Aigen was born in Olomouc on 8 October 1685, the son of a goldsmith.

He was a pupil of the Olomouc painter Dominik Maier. He lived in [[Vienna]] from about 1720, where he was professor of painting at the [[Academy of Fine Arts Vienna|Academy]] from 1751 until his death. His work consists of landscapes with figures, genre paintings and altarpieces. His style shows the influence of artists from France and the Low Countries.<ref name=belv>{{cite web|title=Karl Josef Aigen|url=http://digital.belvedere.at/emuseum/view/people/asitem/items$0040null:13/0?t:state:flow=85945fe1-2502-4798-a332-087cc860da49|publisher=Belvedere Wien|accessdate=27 March 2014}}</ref>

He died at Vienna on 21 October 1762.<ref name=belv/>

===Works===
The [[Österreichische Galerie Belvedere|Gallery of the Belvedere]] in Vienna has two works by him, both scenes with figures.<ref>{{Bryan (3rd edition)|title=Aigen, Karl |volume=1}}</ref>

==References==
{{reflist}}

==External links==
{{cite web|title=Works in the [[Belveddere Gallery]]|url=http://digital.belvedere.at/emuseum/view/objects/asimages/search$0040?t:state:flow=3a74c35b-1547-43a3-a2b8-5bc257d26adb|publisher=Digitales Belvedere}}

{{commons category}}
{{Authority control}}

{{Use dmy dates|date=April 2017}}

{{DEFAULTSORT:Aigen, Karl}}
[[Category:1684 births]]
[[Category:1762 deaths]]
[[Category:17th-century Austrian painters]]
[[Category:18th-century Austrian painters]]
[[Category:Academy of Fine Arts Vienna alumni]]
[[Category:Academy of Fine Arts Vienna faculty]]
[[Category:Austrian male painters]]
[[Category:Moravian-German people]]
[[Category:People from the Margraviate of Moravia]]
[[Category:Artists from Olomouc]]

{{Austria-painter-stub}}
"""

def get_diff(prev_wt, curr_wt, lang):
    prev_wt = "==Lede==" + prev_wt
    curr_wt = "==Lede==" + curr_wt
    return td.get_diff(prev_wt, curr_wt, lang)

def test_insert_category():
    curr_wikitext = prev_wikitext.replace('[[Category:Artists from Olomouc]]\n',
                                          '[[Category:Artists from Olomouc]]\n[[Category:TEST CATEGORY]]',
                                          1)
    expected_changes = {'Category':{'insert':1}}
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    assert expected_changes == nd.get_diff_count(diff)

def test_change_category():
    curr_wikitext = prev_wikitext.replace('[[Category:Artists from Olomouc]]',
                                          '[[Category:Artists from somewhere else]]',
                                          1)
    expected_changes = {'Category':{'change':1}}
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    assert expected_changes == nd.get_diff_count(diff)


def test_remove_formatting():
    curr_wikitext = prev_wikitext.replace("'''Karl Josef Aigen'''",
                                          "Karl Josef Aigen",
                                          1)
    expected_changes = {'Text Formatting':{'remove':1}}
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    assert expected_changes == nd.get_diff_count(diff)

def test_change_formatting():
    curr_wikitext = prev_wikitext.replace("'''Karl Josef Aigen'''",
                                          "''Karl Josef Aigen''",
                                          1)
    expected_changes = {'Text Formatting':{'change':1}}
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    assert expected_changes == nd.get_diff_count(diff)


def test_insert_template():
    curr_wikitext = prev_wikitext.replace('{{Use dmy dates|date=April 2017}}\n',
                                          '{{Use dmy dates|date=April 2017}}\n{{Use dmy new dates|date=April 2017}}',
                                          1)
    expected_changes = {'Template':{'insert':1}}
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    assert expected_changes == nd.get_diff_count(diff)

def test_change_template():
    curr_wikitext = prev_wikitext.replace('{{Use dmy dates|date=April 2017}}\n',
                                          '{{Use dmy dates|date=April 2018}}\n',
                                          1)
    expected_changes = {'Template':{'change':1}}
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    assert expected_changes == nd.get_diff_count(diff)
def test_nested_nodes_ref_temp_link():
    curr_wikitext = prev_wikitext.replace("<ref>{{Bryan (3rd edition)|title=Aigen, Karl |volume=1}}</ref>",
                                          "<ref>{{Bryan (3rd edition)|title=[[Aigen, Karl]] |volume=1}}</ref>",
                                          1)
    expected_changes = {'Reference':{'change':1},'Wikilink':{'insert':1},'Template':{'change':1}}
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    assert expected_changes == nd.get_diff_count(diff)

def test_swap_templates():
    curr_wikitext = prev_wikitext.replace("{{commons category}}\n{{Authority control}}",
                                          "{{Authority control}}\n{{commons category}}",
                                          1)
    expected_changes = {'Template':{'move':2}}
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    assert expected_changes == nd.get_diff_count(diff)


def test_remove_text_count_english_punctuations():
    text = "Wait for it... awesome! More things to come. Why me?"
    expected_changes = {'Sentence':{'remove':3},'Word':{'remove':10},"Whitespace":{'remove':9},"Punctuation":{'remove':4},
                        'Paragraph':{'remove':1}
                       }
    
    get_text_structure = nd.parse_change_text('Text',text,'')
    
    assert expected_changes == get_text_structure

def test_insert_text_count_english_punctuations():
    text = "Wait for it... awesome! More things to come. Why me?"
    expected_changes = {'Sentence':{'insert':3},'Word':{'insert':10},"Whitespace":{'insert':9},"Punctuation":{'insert':4},
                        'Paragraph':{'insert':1}
                       }
    
    get_text_structure = nd.parse_change_text('Text','',text)
    
    assert expected_changes == get_text_structure


def test_change_text_count_english_punctuations():
    curr_text = "Wait for it... awesome! More things to come. Why me?"
    prev_text = "Waits for it... awesome!! More things to come. Why me?"
    expected_changes = {'Sentence':{'change':1},'Word':{'change':1},
                        "Whitespace":{},"Punctuation":{'change':1},
                        'Paragraph':{'change':1}
                        }
    get_text_structure = nd.parse_change_text('Text', prev_text,curr_text)
    assert expected_changes == get_text_structure


    
# def test_text_insert():
#     curr_wikitext = prev_wikitext.replace('Aigen',
#                                           'Aigen Abe',
#                                           1)
#     expected_changes = {'Word':{'change':1}}
#     diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
#     assert expected_changes == nd.get_diff_count(diff)
    
# def test_unbracketed_media():
#     curr_wikitext = prev_wikitext.replace('===Works===\n',
#                                           '===Works===\n<gallery>\nFile:Carl Aigen Fischmarkt.jpg|thumb|Caption\n</gallery>',
#                                           1)
#     expected_changes = {'Tag': {'insert': 1}, 'Media':{'insert':1}}
#     diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
#     assert expected_changes == nd.get_diff_count(diff)

# def test_move_template():
#     curr_wikitext = prev_wikitext.replace('\n{{Use dmy dates|date=April 2017}}',
#                                           '{{Use dmy dates|date=April 2017}}\n',
#                                           1)
#     expected_changes = {'Template':{'move':1}}
#     diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
#     assert expected_changes == nd.get_diff_count(diff)

# def test_nested_nodes_media_format():
#     # Known that this test fails right now -- see https://github.com/geohci/edit-types/issues/13
#     curr_wikitext = prev_wikitext.replace("[[File:Carl Aigen Fischmarkt.jpg|thumb|''Fischmarkt'' by Karl Aigen]]",
#                                           "[[File:Carl Aigen Fischmarkt.jpg|thumb|Fischmarkt by Karl Aigen<ref>A reference</ref>]]",
#                                           1)
#     expected_changes = {'Text Formatting':{'remove':1},'Media':{'change':1}, 'Reference':{'insert':1}}
#     diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
#     print(diff)
#     assert expected_changes == nd.get_diff_count(diff)