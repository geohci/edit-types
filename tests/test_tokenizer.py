from context import parse_change_text


def test_remove_text_count_english_punctuations():
    text = "Wait for it... awesome! More things to come. Why me?"
    expected_changes = {'Sentence': {'remove': 3}, 'Word': {'remove': 10}, "Whitespace": {'remove': 9},
                        "Punctuation": {'remove': 4}, 'Paragraph': {'remove': 1}}

    get_text_structure = parse_change_text(text, '')

    assert expected_changes == get_text_structure


def test_insert_text_count_english_punctuations():
    text = "Wait for it... awesome! More things to come. Why me?"
    expected_changes = {'Sentence': {'insert': 3}, 'Word': {'insert': 10}, 'Whitespace': {'insert': 9},
                        'Punctuation': {'insert': 4}, 'Paragraph': {'insert': 1}}

    get_text_structure = parse_change_text('', text)

    assert expected_changes == get_text_structure


def test_change_text_count_english_punctuations():
    curr_text = "Wait for it... awesome! More things to come. Why me?"
    prev_text = "Waits for it... awesome!! More things to come. Why me?"
    expected_changes = {'Sentence': {'change': 1}, 'Word': {'change': 1},
                        'Punctuation': {'remove': 1},
                        'Paragraph': {'change': 1}
                        }
    get_text_structure = parse_change_text(prev_text, curr_text)
    assert expected_changes == get_text_structure
