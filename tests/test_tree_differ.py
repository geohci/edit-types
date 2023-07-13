import copy
import json

from context import StructuredEditTypes, prev_wikitext


def check_change_counts(diff, expected_changes):
    diff = copy.deepcopy(diff)
    errors = []
    for (action, section, etype) in expected_changes:
        found = False
        for idx in range(len(diff[action])-1, -1, -1):
            chg = None
            if action == 'insert' or action == 'remove':
                chg = diff[action][idx]
            elif action == 'change' or action == 'move':
                chg = diff[action][idx]['prev']
            if chg['type'] == etype and chg['section'] == section:
                diff[action].pop(idx)
                found = True
                break
        if not found:
            errors.append(f'Missing {action}: {etype} in {section}')
    for action in ['remove', 'insert', 'change', 'move']:
        if diff[action]:
            errors.append(f'Additional {action}: {json.dumps(diff[action], indent=2)}')
    assert not errors


def test_insert_category():
    curr_wikitext = prev_wikitext.replace('[[Category:Artists from Olomouc]]\n',
                                          '[[Category:Artists from Olomouc]]\n[[Category:TEST CATEGORY]]',
                                          1)
    expected_changes = [('insert', '4: ==External links==', 'Category')]
    diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en')
    diff.get_diff()
    check_change_counts(diff.tree_diff, expected_changes)


def test_insert_link():
    curr_wikitext = prev_wikitext.replace('He was a pupil of the Olomouc painter',
                                          'He was a [[pupil]] of the Olomouc painter',
                                          1)
    expected_changes = [('insert', '1: ==Life==', 'Wikilink')]
    diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en')
    diff.get_diff()
    check_change_counts(diff.tree_diff, expected_changes)


def test_move_template():
    curr_wikitext = prev_wikitext.replace('{{Austria-painter-stub}}',
                                          '',
                                          1)
    curr_wikitext = '{{Austria-painter-stub}}' + curr_wikitext
    expected_changes = [('move', '4: ==External links==', 'Template')]
    diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en')
    diff.get_diff()
    check_change_counts(diff.tree_diff, expected_changes)


def test_change_heading():
    curr_wikitext = prev_wikitext.replace('===Works===',
                                          '===NotWorks===',
                                          1)
    expected_changes = [('change', '2: ===Works===', 'Heading')]
    diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en')
    diff.get_diff()
    check_change_counts(diff.tree_diff, expected_changes)


def test_remove_formatting():
    curr_wikitext = prev_wikitext.replace("'''Karl Josef Aigen'''",
                                          "Karl Josef Aigen",
                                          1)
    # two tf-spans removed; won't be reduced to a single block until the node differ
    expected_changes = [('remove', '0: Lede', 'Text Formatting'), ('remove', '0: Lede', 'Text Formatting')]
    diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en')
    diff.get_diff()
    check_change_counts(diff.tree_diff, expected_changes)


table = """{| border="1" cellspacing="0" cellpadding="5"
|- bgcolor="#cccccc"
! '''Year'''
! '''[[House of Representatives of the Netherlands|HoR]]'''
|-
|[[1897 Dutch general election|1897]]
|5
|-
|1898
|5
|-
|1899
|5
|-
|1900
|5
|-
|1901
|9
|-
|1902
|9
|}"""


def test_insert_table():
    curr_wikitext = prev_wikitext + '\n' + table
    # four tf-spans removed; won't be reduced to two blocks until the node differ
    expected_changes = [('insert', '4: ==External links==', 'Table'),
                        ('change', '4: ==External links==', 'Text'),
                        ('insert', '4: ==External links==', 'Wikilink'),
                        ('insert', '4: ==External links==', 'Wikilink'),
                        ('insert', '4: ==External links==', 'Text Formatting'),
                        ('insert', '4: ==External links==', 'Text Formatting'),
                        ('insert', '4: ==External links==', 'Text Formatting'),
                        ('insert', '4: ==External links==', 'Text Formatting')]
    diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en')
    diff.get_diff()
    check_change_counts(diff.tree_diff, expected_changes)


gallery = """<gallery widths="190px" heights="190px" perrow="4">
File:Lucas Cranach d.Ä. - Bildnis des Moritz Büchner.jpg|[[Lucas Cranach the Elder]], ''Portrait of Moritz'', 1518
</gallery>"""


def test_insert_gallery():
    curr_wikitext = prev_wikitext + '\n' + gallery
    # two tf-spans removed; won't be reduced to a single block until the node differ
    expected_changes = [('insert', '4: ==External links==', 'Gallery'),
                        ('change', '4: ==External links==', 'Text'),
                        ('insert', '4: ==External links==', 'Media'),
                        ('insert', '4: ==External links==', 'Wikilink'),
                        ('insert', '4: ==External links==', 'Text Formatting'),
                        ('insert', '4: ==External links==', 'Text Formatting')]
    diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en')
    diff.get_diff()
    check_change_counts(diff.tree_diff, expected_changes)


def test_table_change():
    curr_wikitext = table.replace('general election', 'gen elec', 1)
    expected_changes = [('change', '0: Lede', 'Wikilink'),
                        ('change', '0: Lede', 'Table')]
    diff = StructuredEditTypes(table, curr_wikitext, lang='en')
    diff.get_diff()
    check_change_counts(diff.tree_diff, expected_changes)
