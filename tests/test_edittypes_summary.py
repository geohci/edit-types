import pytest

from context import cjk_prev_wikitext, StructuredEditTypes, full_diff_to_simple, prev_wikitext, SimpleEditTypes

# Text tests
def test_text_change():
    curr_wikitext = prev_wikitext.replace('Aigen was born in Olomouc on 8 October 1685, the son of a goldsmith.',
                                          'Aigen-Abe was born in Olomouc on 9 October 1685, the daughter of a goldsmith.',
                                          1)
    expected_changes = {'Paragraph': {'change': 1}, 'Sentence': {'change': 1}, 'Word': {'change': 3},
                        'Punctuation': {'insert': 1}, 'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_hyphen_words():
    curr_wikitext = prev_wikitext.replace('Aigen was born in Olomouc on 8 October 1685, the son of a goldsmith.',
                                          "Aigen-Abes' daughter was born in Olomouc on 9 October 1685, the daughter of a goldsmith.",
                                          1)

    expected_changes = {'Word': {'change': 3, 'insert': 1}, 'Punctuation': {'insert': 2}, 'Whitespace': {'insert': 1},
                        'Sentence': {'change': 1}, 'Section': {'change': 1}, 'Paragraph': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_reorder_text():
    curr_wikitext = prev_wikitext.replace("He was a pupil of the Olomouc painter Dominik Maier.",
                                          "He the a pupil of was Olomouc painter Maier Dominik.",
                                          1)
    expected_changes = {'Sentence': {'change': 1}, 'Paragraph': {'change': 1}, 'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


# validate text formatting changes both when type and inner content changes
# note ''Fischmarkt'' is part of an image, which is why this isn't recorded as a word change too.
def test_text_from_formatting():
    curr_wikitext = prev_wikitext.replace("''Fischmarkt''",
                                          "''Fleischmarkt''",
                                          1)
    curr_wikitext = curr_wikitext.replace("'''Karl Josef Aigen'''",
                                          "''Karl Josef Aigen''",
                                          1)
    expected_changes = {'Text Formatting': {'change': 1},
                        'Section': {'change': 2}, 'Media': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


# validate text doubly nested within an object that contributes text (formatting) and one that doesn't (ref tag)
# is correctly handled -- i.e. the ref doesn't contribute any words.
def test_text_within_formatting():
    curr_wikitext = prev_wikitext.replace("the son of a goldsmith",
                                          "''the son of a goldsmith<ref>A reference: https://example.com/url-string</ref>''",
                                          1)
    expected_changes = {'Text Formatting': {'insert': 1}, 'Reference': {'insert': 1}, 'ExternalLink': {'insert': 1},
                        'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes

@pytest.mark.xfail(reason="Tree Differ can't currently detect simple shifts in text formatting start-stops.")
def test_change_formatting_length():
    curr_wikitext = prev_wikitext.replace("'''Karl Josef Aigen''' (8 October 1684 – 22 October 1762) was a landscape painter, born at",
                                          "'''Karl Josef Aigen (8 October 1684 – 22 October 1762) was a landscape painter, born at'''",
                                          1)
    expected_changes = {'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en')
    diff = full_diff.get_diff()
    assert full_diff_to_simple(diff) == expected_changes


def test_text_from_link():
    curr_wikitext = prev_wikitext.replace("[[Vienna]]",
                                          "[[Vienna|same link different text]]",
                                          1)
    expected_changes = {'Wikilink': {'change': 1}, 'Sentence': {'change': 1}, 'Paragraph': {'change': 1},
                        'Section': {'change': 1}, 'Word': {'insert': 3, 'change': 1}, 'Whitespace': {'insert': 3}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_empty_previous():
    curr_wikitext = 'Section with some text.'
    expected_changes = {'Word': {'insert': 4}, 'Section': {'insert': 1}, 'Punctuation': {'insert': 1},
                        'Sentence': {'insert': 1}, 'Paragraph': {'insert': 1}, 'Whitespace': {'insert': 3}}
    diff = SimpleEditTypes('', curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes('', curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_change_cjk_punctuations():
    cjk_curr_wikitext = cjk_prev_wikitext.replace('。', '、', 1)
    expected_changes = {'Section': {'change': 1}, 'Punctuation': {'change': 1}, 'Sentence': {'change': 1, 'remove': 1},
                        'Paragraph': {'change': 1}}
    diff = SimpleEditTypes(cjk_prev_wikitext, cjk_curr_wikitext, lang='ja').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(cjk_prev_wikitext, cjk_curr_wikitext, lang='ja').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_change_cjk_character():
    cjk_curr_wikitext = cjk_prev_wikitext.replace('番組は', '年度', 1)
    expected_changes = {'Section': {'change': 1}, 'Character': {'change': 2, 'remove': 1}, 'Sentence': {'change': 1},
                        'Paragraph': {'change': 1}}
    diff = SimpleEditTypes(cjk_prev_wikitext, cjk_curr_wikitext, lang='ja').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(cjk_prev_wikitext, cjk_curr_wikitext, lang='ja').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_remove_cjk_punctuations():
    cjk_curr_wikitext = cjk_prev_wikitext.replace('。', '', 1)
    expected_changes = {'Section': {'change': 1}, 'Punctuation': {'remove': 1}, 'Sentence': {'change': 1, 'remove': 1},
                        'Paragraph': {'change': 1}}
    diff = SimpleEditTypes(cjk_prev_wikitext, cjk_curr_wikitext, lang='ja').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(cjk_prev_wikitext, cjk_curr_wikitext, lang='ja').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


# Size Test

def test_large_nested_change():
    curr_wikitext = prev_wikitext.replace("<ref>{{Bryan (3rd edition)|title=Aigen, Karl",
                                          "<ref>{{Bryan (3rd edition)|title=Aigen, Karl" + '[[link]]' * 1000,
                                          1)
    simple_expected_changes = {'Reference': {'change': 1}, 'Section': {'change': 1}, 'Wikilink': {'insert': 1000},
                               'Template': {'change': 1}}
    full_expected_changes = {'Reference': {'change': 1}, 'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == simple_expected_changes
    # with 1000 links, we hit a RecursionError while manipulating the node trees if we don't cap with timeout
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en', timeout=True).get_diff()
    assert full_diff_to_simple(full_diff) == full_expected_changes


def test_large_unnested_change():
    curr_wikitext = prev_wikitext.replace("Aigen was born",
                                          "Aigen was born" + '[[link]]' * 1000,
                                          1)
    expected_changes = {'Section': {'change': 1},
                        'Wikilink': {'insert': 1000},
                        'Paragraph': {'change': 1},
                        'Sentence': {'change': 1},
                        'Word': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


# Non-text nodes test
def test_insert_category():
    curr_wikitext = prev_wikitext.replace('[[Category:Artists from Olomouc]]\n',
                                          '[[Category:Artists from Olomouc]]\n[[Category:TEST CATEGORY]]',
                                          1)
    expected_changes = {'Category': {'insert': 1}, 'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_change_category():
    curr_wikitext = prev_wikitext.replace('[[Category:Artists from Olomouc]]',
                                          '[[Category:Artists from somewhere else]]',
                                          1)
    expected_changes = {'Category': {'change': 1}, 'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_remove_formatting():
    curr_wikitext = prev_wikitext.replace("'''Karl Josef Aigen'''",
                                          "Karl Josef Aigen",
                                          1)
    expected_changes = {'Text Formatting': {'remove': 1}, 'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_link_within_formatting():
    curr_wikitext = prev_wikitext.replace("'''Karl Josef Aigen'''",
                                          "'''[[Karl Josef Aigen]]'''",
                                          1)
    expected_changes = {'Wikilink': {'insert': 1}, 'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_change_formatting():
    curr_wikitext = prev_wikitext.replace("'''Karl Josef Aigen'''",
                                          "''Karl Josef Aigen''",
                                          1)
    expected_changes = {'Text Formatting': {'change': 1}, 'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_insert_template():
    curr_wikitext = prev_wikitext.replace('{{Use dmy dates|date=April 2017}}\n',
                                          '{{Use dmy dates|date=April 2017}}\n{{Use dmy new dates|date=April 2017}}',
                                          1)
    expected_changes = {'Template': {'insert': 1}, 'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_change_template():
    curr_wikitext = prev_wikitext.replace('{{Use dmy dates|date=April 2017}}\n',
                                          '{{Use dmy dates|date=April 2018}}\n',
                                          1)
    expected_changes = {'Template': {'change': 1}, 'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_nested_nodes_ref_temp_link():
    curr_wikitext = prev_wikitext.replace("<ref>{{Bryan (3rd edition)|title=Aigen, Karl |volume=1}}</ref>",
                                          "<ref>{{Bryan (3rd edition)|title=[[Aigen, Karl]] |volume=1}}</ref>",
                                          1)
    expected_changes = {'Reference': {'change': 1}, 'Wikilink': {'insert': 1}, 'Template': {'change': 1},
                        'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_swap_templates():
    curr_wikitext = prev_wikitext.replace("{{commons category}}\n{{Authority control}}",
                                          "{{Authority control}}\n{{commons category}}",
                                          1)
    simple_expected_changes = {'Section': {'change': 1}}
    full_expected_changes = {'Template':{'move':2}, 'Section':{'change':1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == simple_expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == full_expected_changes


def test_unbracketed_media():
    curr_wikitext = prev_wikitext.replace('===Works===\n',
                                          '===Works===\n<gallery>\nFile:Carl Aigen Fischmarkt.jpg|thumb|Caption\n</gallery>',
                                          1)
    expected_changes = {'Gallery': {'insert': 1}, 'Media': {'insert': 1}, 'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_nested_nodes_media_format():
    curr_wikitext = prev_wikitext.replace("[[File:Carl Aigen Fischmarkt.jpg|thumb|''Fischmarkt'' by Karl Aigen]]",
                                          "[[File:Carl Aigen Fischmarkt.jpg|thumb|Fischmarkt by Karl Aigen<ref>A reference</ref>]]",
                                          1)
    expected_changes = {'Text Formatting': {'remove': 1}, 'Media': {'change': 1}, 'Reference': {'insert': 1},
                        'Section': {'change': 1}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_complicated_sections():
    # break section into two (no text changes, just new heading)
    curr_wikitext = prev_wikitext.replace("\nHe died at Vienna",
                                          "===Death===\nHe died at Vienna",
                                          1)
    # category change in later section
    curr_wikitext = curr_wikitext.replace("[[Category:Artists from Olomouc]]",
                                          "[[Category:Artists in Olomouc]]",
                                          1)
    expected_changes = {'Heading': {'insert': 1}, 'Category': {'change': 1}, 'Section': {'insert': 1, 'change': 2}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == expected_changes


def test_moved_section():
    # swap Works and References sections with no other changess
    curr_wikitext = prev_wikitext.replace(
        "\n\n===Works===\nThe [[Österreichische Galerie Belvedere|Gallery of the Belvedere]] in Vienna has two works by him, both scenes with figures.<ref>{{Bryan (3rd edition)|title=Aigen, Karl |volume=1}}</ref>\n\n==References==\n{{reflist}}",
        "\n\n==References==\n{{reflist}}\n\n===Works===\nThe [[Österreichische Galerie Belvedere|Gallery of the Belvedere]] in Vienna has two works by him, both scenes with figures.<ref>{{Bryan (3rd edition)|title=Aigen, Karl |volume=1}}</ref>",
        1)
    simple_expected_changes = {}
    full_expected_changes = {'Section':{'move':1, 'change':2}}
    diff = SimpleEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert diff == simple_expected_changes
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert full_diff_to_simple(full_diff) == full_expected_changes
