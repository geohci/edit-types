from context import prev_wikitext, EditCategories, StructuredEditTypes, Tokenizer

enTokenizer = Tokenizer(lang='en')

# Text tests
def test_text_change():
    curr_wikitext = prev_wikitext.replace('Aigen was born in Olomouc on 8 October 1685, the son of a goldsmith.',
                                          'Aigen-Abe was born in Olomouc on 9 October 1685, the daughter of a goldsmith.',
                                          1)
    size, difficulty, text_change, edit_categories = EditCategories().get_edit_categories(prev_wikitext, curr_wikitext, lang='en', tokenizer=enTokenizer)
    expected_size = 'Small'
    expected_difficulty = 'Easy'
    expected_text_change = True
    expected_ec = ['Content Maintenance']
    assert size == expected_size
    assert difficulty == expected_difficulty
    assert text_change == expected_text_change
    assert sorted(list(edit_categories.keys())) == expected_ec


# validate text doubly nested within an object that contributes text (formatting) and one that doesn't (ref tag)
# is correctly handled -- i.e. the ref doesn't contribute any words.
def test_text_within_formatting():
    curr_wikitext = prev_wikitext.replace("the son of a goldsmith",
                                          "''the son of a goldsmith<ref>A reference: https://example.com/url-string</ref>''",
                                          1)
    size, difficulty, text_change, edit_categories = EditCategories().get_edit_categories(
        prev_wikitext, curr_wikitext, lang='en', tokenizer=enTokenizer)
    expected_size = 'Small'
    expected_difficulty = 'Hard'
    expected_text_change = False
    expected_ec = ['Content Annotation', 'Content Maintenance']
    assert size == expected_size
    assert difficulty == expected_difficulty
    assert text_change == expected_text_change
    assert sorted(list(edit_categories.keys())) == expected_ec


def test_large_unnested_change():
    curr_wikitext = prev_wikitext.replace("Aigen was born",
                                          "Aigen was born" + ' [[link]]' * 500,
                                          1)
    size, difficulty, text_change, edit_categories = EditCategories().get_edit_categories(
        prev_wikitext, curr_wikitext, lang='en', tokenizer=enTokenizer)
    expected_size = 'Large'
    expected_difficulty = 'Medium-Hard'
    expected_text_change = True
    expected_ec = ['Content Annotation', 'Content Maintenance']
    assert size == expected_size
    assert difficulty == expected_difficulty
    assert text_change == expected_text_change
    assert sorted(list(edit_categories.keys())) == expected_ec


# Non-text nodes test
def test_insert_category():
    curr_wikitext = prev_wikitext.replace('[[Category:Artists from Olomouc]]\n',
                                          '[[Category:Artists from Olomouc]]\n[[Category:TEST CATEGORY]]',
                                          1)
    size, difficulty, text_change, edit_categories = EditCategories().get_edit_categories(
        prev_wikitext, curr_wikitext, lang='en', tokenizer=enTokenizer)
    expected_size = 'Small'
    expected_difficulty = 'Medium-Hard'
    expected_text_change = False
    expected_ec = ['Content Annotation']
    assert size == expected_size
    assert difficulty == expected_difficulty
    assert text_change == expected_text_change
    assert sorted(list(edit_categories.keys())) == expected_ec


def test_change_template():
    curr_wikitext = prev_wikitext.replace('{{Use dmy dates|date=April 2017}}\n',
                                          '{{Use dmy dates|date=April 2018}}\n',
                                          1)
    size, difficulty, text_change, edit_categories = EditCategories().get_edit_categories(
        prev_wikitext, curr_wikitext, lang='en', tokenizer=enTokenizer)
    expected_size = 'Small'
    expected_difficulty = 'Hard'
    expected_text_change = False
    expected_ec = ['Content Maintenance']
    assert size == expected_size
    assert difficulty == expected_difficulty
    assert text_change == expected_text_change
    print(EditCategories().details_to_dict(StructuredEditTypes(prev_wikitext=prev_wikitext, curr_wikitext=curr_wikitext, lang='en').get_diff()))
    assert sorted(list(edit_categories.keys())) == expected_ec


def test_unbracketed_media():
    curr_wikitext = prev_wikitext.replace('===Works===\n',
                                          '===Works===\n<gallery>\nFile:Carl Aigen Fischmarkt.jpg|thumb|Caption\n</gallery>',
                                          1)
    size, difficulty, text_change, edit_categories = EditCategories().get_edit_categories(
        prev_wikitext, curr_wikitext, lang='en', tokenizer=enTokenizer)
    expected_size = 'Small'
    expected_difficulty = 'Hard'
    expected_text_change = False
    expected_ec = ['Content Generation']
    assert size == expected_size
    assert difficulty == expected_difficulty
    assert text_change == expected_text_change
    print(StructuredEditTypes(prev_wikitext=prev_wikitext, curr_wikitext=curr_wikitext, lang='en').get_diff())
    assert sorted(list(edit_categories.keys())) == expected_ec