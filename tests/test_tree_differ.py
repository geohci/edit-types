import copy
import json

from context import td  # tree-differ

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

def check_change_counts(diff, expected_changes):
    diff = copy.deepcopy(diff)
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
        assert found, f'Missing {action}: {etype} in {section}'
    for action in ['remove', 'insert', 'change', 'move']:
        assert not diff[action], f'Additional {action}: {json.dumps(diff[action], indent=2)}'


def test_insert_category():
    curr_wikitext = prev_wikitext.replace('[[Category:Artists from Olomouc]]\n',
                                          '[[Category:Artists from Olomouc]]\n[[Category:TEST CATEGORY]]',
                                          1)
    expected_changes = [('insert', 'S#5: External links (L2)', 'Category')]
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    check_change_counts(diff, expected_changes)

def test_insert_link():
    curr_wikitext = prev_wikitext.replace('He was a pupil of the Olomouc painter',
                                          'He was a [[pupil]] of the Olomouc painter',
                                          1)
    expected_changes = [('insert', 'S#2: Life (L2)', 'Wikilink')]
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    check_change_counts(diff, expected_changes)

def test_move_template():
    curr_wikitext = prev_wikitext.replace('{{Austria-painter-stub}}',
                                          '',
                                          1)
    curr_wikitext = '{{Austria-painter-stub}}' + curr_wikitext
    expected_changes = [('move', 'S#5: External links (L2)', 'Template')]
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    check_change_counts(diff, expected_changes)

def test_change_heading():
    curr_wikitext = prev_wikitext.replace('===Works===',
                                          '===NotWorks===',
                                          1)
    expected_changes = [('change', 'S#3: Works (L3)', 'Heading')]
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    check_change_counts(diff, expected_changes)

def test_remove_formatting():
    curr_wikitext = prev_wikitext.replace("'''Karl Josef Aigen'''",
                                          "Karl Josef Aigen",
                                          1)
    expected_changes = [('remove', 'S#1: Lede (L2)', 'Tag')]
    diff = get_diff(prev_wikitext, curr_wikitext, lang='en')
    check_change_counts(diff, expected_changes)