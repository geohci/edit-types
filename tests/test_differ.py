from context import EditTypes, parse_change_text

# Basic wikitext to play with that has most of the things we're interested in (image, categories, templates, etc.)
# Source: https://en.wikipedia.org/wiki/Karl_Aigen
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
cjk_prev_wikitext ="""{{特筆性|date=2016年1月30日 (土) 01:03 (UTC)}}
『'''ティーンズねっとわーく'''』は、[[1994年]][[4月4日]]から[[1996年]][[3月11日]]まで[[NHK教育テレビジョン|NHK教育テレビ]]で放送されていた高校生向けの[[学校放送]]（教科：[[特別活動]]）である。放送時間は毎週月曜 12:30 - 13:00 （[[日本標準時]]）、1995年度のみ別の時間帯での[[再放送]]あり。

== 概要 ==
[[パソコン通信]]を活用した番組で、番組収録に協力してくれた高等学校46校との間に専用ネットワークを開設。このネットワークに寄せられた各回の議題（生活環境・家庭環境・社会情勢・世界情勢など）に対する意見や関連情報を、その学校に通う生徒たち自身がリポート・討論することで議題をさらに深く追求していた<ref>{{Cite web |url=http://nhk.jp/chronicle/?0001000000000000%40000000000000000000000012-63-0300000000000000000000&q=%E3%83%86%E3%82%A3%E3%83%BC%E3%83%B3%E3%82%BA%E3%81%AD%E3%81%A3%E3%81%A8%E3%82%8F%E3%83%BC%E3%81%8F |title=ティーンズねっとわーく 理想の学校とは &#124; 保存番組検索結果詳細 &#124; NHKクロニクル |publisher=[[日本放送協会]] |accessdate=2016-03-21}}</ref>。

番組は、パソコン通信の活用方法を紹介するミニコーナー「パソ通ミニ講座」を設けていた。番組終了間際の回においては、パソコン通信に代わって台頭しはじめていた[[日本のインターネット|インターネット]]を話題にしていた<ref>{{Cite web |url=http://nhk.jp/chronicle/?0001000000000000%4000000000000000000000001703-3C00000000000000000000&q=%E3%83%86%E3%82%A3%E3%83%BC%E3%83%B3%E3%82%BA%E3%81%AD%E3%81%A3%E3%81%A8%E3%82%8F%E3%83%BC%E3%81%8F&fy=&fm=&fd=&ty=&tm=&td=&np=10&cal_edit=&or=&o=31&hitCount=39 |title=ティーンズねっとわーく インターネットって何？ &#124; 保存番組検索結果詳細 &#124; NHKクロニクル |publisher=日本放送協会 |accessdate=2016-03-21}}</ref>。

== 出演者 ==
; 1994年度
: [[山根一眞]]、[[穴井夕子]]、[[石塚英彦]]（[[ホンジャマカ]]）、[[恵俊彰]]（ホンジャマカ）
; 1995年度
: [[向谷実]]、[[岩井由紀子]]、石塚英彦（ホンジャマカ）、恵俊彰（ホンジャマカ）

== 放送リスト ==
{| class="wikitable" style="font-size:small; float:left; margin-right:3px"
|-
!初回放送日!!サブタイトル
|-
|1994年4月4日||理想の学校とは
|-
|1994年4月18日||わたしたちにとっての「米」
|-
|1994年5月2日||モテる条件
|-
|1994年5月16日||生徒会を考える
|-
|1994年5月30日||障害者の暮らしやすい環境とは
|-
|1994年6月13日||わたしたちにとっての「米」パート2
|-
|1994年6月27日||パソコン通信とコミュニケーション
|-
|1994年8月29日||私たちにとっての地域社会
|-
|1994年9月12日||君は国際人になれるか？
|-
|1994年9月26日||ティーンズの一日
|-
|1994年10月17日||ティーンズ文化祭
|-
|1994年10月31日||燃えろ ごみ問題
|-
|1994年11月14日||いま、なぜ ボランティア？
|-
|1994年11月28日||目指せ！理想の部活
|-
|1994年12月12日||徹底分析 マスコミの中のティーンズ像
|-
|1995年1月9日||いじめはなくせるか
|-
|1995年1月23日||夢のかなえかた
|-
|1995年2月6日||わたしたちとエイズ
|-
|1995年2月20日||わたしたちにとっての「米」パート3 農業の魅力
|-
|1995年3月6日||ティーンズ卒業式
|}
{| class="wikitable" style="font-size:small; float:left"
|-
!初回放送日!!サブタイトル
|-
|1995年4月10日||学校生活に何を求めるか
|-
|1995年4月24日||
|-
|1995年5月15日||よその学校を知りたい
|-
|1995年5月29日||生徒会役員はつらいよ
|-
|1995年6月12日||パソ通なんてこわくない！
|-
|1995年6月26日||オトナになんてなりたくない？
|-
|1995年7月10日||勉強って何のため？
|-
|1995年8月28日||ティーンズかっぷる白書
|-
|1995年9月18日||かわいい子だから旅がしたい
|-
|1995年10月2日||今、コトバを見つめたい
|-
|1995年10月16日||制服でもおしゃれしたい！
|-
|1995年10月30日||どう考える体罰
|-
|1995年11月13日||ティーンズ文化祭
|-
|1995年11月27日||近くの友達 遠くの親友？
|-
|1995年12月11日||理科系vs文科系
|-
|1996年1月8日||日本はやさしい国ですか
|-
|1996年1月22日||金銭道・高校編
|-
|1996年2月5日||ふるさとを知っていますか？
|-
|1996年2月19日||インターネットって何？
|-
|1996年3月4日||ティーンズ旅立ち
|}
{{clear}}

== 脚注 ==
{{Reflist}}

== 参考文献 ==
{{参照方法|date=2016年1月30日 (土) 01:03 (UTC)|section=1}}
* [https://web.archive.org/web/20150309163502/http://www.nhk.or.jp/archives/dataroom/ アカイさん資料室（1994〜1995年）] {{どれ|date=2016年3月21日 (月) 13:36 (UTC)}}

== 外部リンク ==
* {{NHK放送史|D0009042550_00000|ティーンズねっとわーく}}
{{前後番組
| 放送局 = [[NHK教育テレビジョン|NHK教育テレビ]]
| 放送枠 = 月曜12:30枠
| 番組名 = ティーンズねっとわーく<br />（1994年4月4日 - 1996年3月25日）
| 前番組 = [[コンピューター未来館]]<br />（1993年4月5日 - 1994年3月14日）<br />※12:25 - 12:55<hr />[[数学ボックス]]（月曜）<br />（1993年4月5日 - 1994年3月14日）<br />※12:55 - 13:00
| 次番組 = [[ハイスクール電脳倶楽部]]<br />（1996年4月8日 - 1997年3月10日）
}}
{{Tv-stub}}
{{NHK高校講座}}
{{ホンジャマカ}}
{{デフォルトソート:ていいんすねつとわあく}}
[[Category:NHK教育テレビジョンの学校放送番組の歴史 (1990年代)]]
[[Category:1994年のテレビ番組 (日本)]]
[[Category:情報教育]]
"""
##Text test
    
def test_text_change():
    curr_wikitext = prev_wikitext.replace('Aigen was born in Olomouc on 8 October 1685, the son of a goldsmith.',
                                          'Aigen-Abe was born in Olomouc on 9 October 1685, the daughter of a goldsmith.',
                                          1)
    expected_changes = {'Paragraph':{'change':1}, 'Sentence':{'change':1}, 'Word':{'change':3},'Punctuation':{'insert':1}, 'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_hyphen_words():
    curr_wikitext = prev_wikitext.replace('Aigen was born in Olomouc on 8 October 1685, the son of a goldsmith.',
                                          "Aigen-Abes' daughter was born in Olomouc on 9 October 1685, the daughter of a goldsmith.",
                                          1)

    expected_changes = {'Word': {'change': 3, 'insert': 1}, 'Punctuation': {'insert': 2}, 'Whitespace': {'insert': 1},
                        'Sentence': {'change': 1}, 'Section': {'change': 1}, 'Paragraph': {'change': 1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_reorder_text():
    curr_wikitext = prev_wikitext.replace("He was a pupil of the Olomouc painter Dominik Maier.",
                                          "He the a pupil of was Olomouc painter Maier Dominik.",
                                          1)
    expected_changes = {'Sentence':{'change':1},'Paragraph':{'change':1}, 'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

# validate reference doesn't contribute text even though it's nested within text formatting
def test_text_from_formatting():
    curr_wikitext = prev_wikitext.replace("the son of a goldsmith",
                                          "''the son of a goldsmith<ref>A reference: https://example.com/url-string</ref>''",
                                          1)
    expected_changes = {'Text Formatting':{'insert':1}, 'Reference':{'insert':1}, 'ExternalLink':{'insert':1},
                        'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

# validate reference doesn't contribute text even though it's nested within text formatting
def test_text_from_link():
    curr_wikitext = prev_wikitext.replace("[[Vienna]]",
                                          "[[Vienna|same link different text]]",
                                          1)
    expected_changes = {'Wikilink':{'change':1}, 'Sentence':{'change':1}, 'Paragraph':{'change':1},
                        'Section':{'change':1}, 'Word':{'insert': 3, 'change':1}, 'Whitespace':{'insert':3}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_change_cjk_punctuations():
    cjk_curr_wikitext = cjk_prev_wikitext.replace('。','、',1)
    expected_changes = {'Section':{'change':1}, 'Punctuation':{'change':1},'Sentence':{'change':1,'remove':1},'Paragraph':{'change':1}}
    diff = EditTypes(cjk_prev_wikitext, cjk_curr_wikitext, lang='ja').get_diff()
    assert expected_changes == diff

def test_change_cjk_character():
    cjk_curr_wikitext = cjk_prev_wikitext.replace('番組は','年度',1)
    expected_changes = {'Section':{'change':1}, 'Character':{'change':2,'remove':1},'Sentence':{'change':1},'Paragraph':{'change':1}}
    diff = EditTypes(cjk_prev_wikitext, cjk_curr_wikitext, lang='ja').get_diff()
    assert expected_changes == diff

def test_remove_cjk_punctuations():
    cjk_curr_wikitext = cjk_prev_wikitext.replace('。','',1)
    expected_changes = {'Section':{'change':1}, 'Punctuation':{'remove':1},'Sentence':{'change':1,'remove':1},'Paragraph':{'change':1}}
    diff = EditTypes(cjk_prev_wikitext, cjk_curr_wikitext, lang='ja').get_diff()
    assert expected_changes == diff

##Size Test

def test_large_nested_change():
    curr_wikitext = prev_wikitext.replace("<ref>{{Bryan (3rd edition)",
                                          "<ref>{{Bryan (3rd edition)" + '[[link]]'*1000,
                                          1)
    # shouldn't be expanded so only change to reference detected
    expected_changes = {'Reference': {'change': 1}, 'Section': {'change': 1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_large_unnested_change():
    curr_wikitext = prev_wikitext.replace("Aigen was born",
                                          "Aigen was born" + '[[link]]'*1000,
                                          1)
    # too many nodes -- should just compare section hashes to find edits
    expected_changes = {'Section': {'change': 1}, 'Paragraph':{'change':1}, 'Sentence':{'change':1}, 'Word':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_empty_previous():
    curr_wikitext = 'Section with some text.'
    expected_changes = {'Word':{'insert':4},'Section':{'insert':1}, 'Punctuation':{'insert':1}, 'Sentence':{'insert':1},
                        'Paragraph':{'insert':1}, 'Whitespace':{'insert':3}}
    diff = EditTypes('', curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff




##Non-text nodes test
def test_insert_category():
    curr_wikitext = prev_wikitext.replace('[[Category:Artists from Olomouc]]\n',
                                          '[[Category:Artists from Olomouc]]\n[[Category:TEST CATEGORY]]',
                                          1)
    expected_changes = {'Category':{'insert':1}, 'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_change_category():
    curr_wikitext = prev_wikitext.replace('[[Category:Artists from Olomouc]]',
                                          '[[Category:Artists from somewhere else]]',
                                          1)
    expected_changes = {'Category':{'change':1}, 'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff


def test_remove_formatting():
    curr_wikitext = prev_wikitext.replace("'''Karl Josef Aigen'''",
                                          "Karl Josef Aigen",
                                          1)
    expected_changes = {'Text Formatting':{'remove':1},'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_change_formatting():
    curr_wikitext = prev_wikitext.replace("'''Karl Josef Aigen'''",
                                          "''Karl Josef Aigen''",
                                          1)
    expected_changes = {'Text Formatting':{'change':1},'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff


def test_insert_template():
    curr_wikitext = prev_wikitext.replace('{{Use dmy dates|date=April 2017}}\n',
                                          '{{Use dmy dates|date=April 2017}}\n{{Use dmy new dates|date=April 2017}}',
                                          1)
    expected_changes = {'Template':{'insert':1}, 'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff


def test_change_template():
    curr_wikitext = prev_wikitext.replace('{{Use dmy dates|date=April 2017}}\n',
                                          '{{Use dmy dates|date=April 2018}}\n',
                                          1)
    expected_changes = {'Template':{'change':1}, 'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff


def test_nested_nodes_ref_temp_link():
    curr_wikitext = prev_wikitext.replace("<ref>{{Bryan (3rd edition)|title=Aigen, Karl |volume=1}}</ref>",
                                          "<ref>{{Bryan (3rd edition)|title=[[Aigen, Karl]] |volume=1}}</ref>",
                                          1)
    expected_changes = {'Reference':{'change':1},'Wikilink':{'insert':1},'Template':{'change':1}, 'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_swap_templates():
    curr_wikitext = prev_wikitext.replace("{{commons category}}\n{{Authority control}}",
                                          "{{Authority control}}\n{{commons category}}",
                                          1)
    expected_changes = {'Template':{'move':2}, 'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_unbracketed_media():
    curr_wikitext = prev_wikitext.replace('===Works===\n',
                                          '===Works===\n<gallery>\nFile:Carl Aigen Fischmarkt.jpg|thumb|Caption\n</gallery>',
                                          1)
    expected_changes = {'Gallery': {'insert': 1}, 'Media':{'insert':1}, 'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_nested_nodes_media_format():
    curr_wikitext = prev_wikitext.replace("[[File:Carl Aigen Fischmarkt.jpg|thumb|''Fischmarkt'' by Karl Aigen]]",
                                          "[[File:Carl Aigen Fischmarkt.jpg|thumb|Fischmarkt by Karl Aigen<ref>A reference</ref>]]",
                                          1)
    expected_changes = {'Text Formatting':{'remove':1},'Media':{'change':1}, 'Reference':{'insert':1}, 'Section':{'change':1}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_complicated_sections():
    # break section into two (no text changes, just new heading)
    curr_wikitext = prev_wikitext.replace("\nHe died at Vienna",
                                          "===Death===\nHe died at Vienna",
                                          1)
    # category change in later section
    curr_wikitext = curr_wikitext.replace("[[Category:Artists from Olomouc]]",
                                          "[[Category:Artists in Olomouc]]",
                                          1)
    expected_changes = {'Heading':{'insert':1},'Category':{'change':1}, 'Section':{'insert':1, 'change':2}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff

def test_moved_section():
    # swap Works and References sections with no other changess
    curr_wikitext = prev_wikitext.replace("\n\n===Works===\nThe [[Österreichische Galerie Belvedere|Gallery of the Belvedere]] in Vienna has two works by him, both scenes with figures.<ref>{{Bryan (3rd edition)|title=Aigen, Karl |volume=1}}</ref>\n\n==References==\n{{reflist}}",
                                          "\n\n==References==\n{{reflist}}\n\n===Works===\nThe [[Österreichische Galerie Belvedere|Gallery of the Belvedere]] in Vienna has two works by him, both scenes with figures.<ref>{{Bryan (3rd edition)|title=Aigen, Karl |volume=1}}</ref>",
                                          1)
    expected_changes = {'Section':{'move':1, 'change':2}}
    diff = EditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    assert expected_changes == diff


##Unit test
def test_remove_text_count_english_punctuations():
    text = "Wait for it... awesome! More things to come. Why me?"
    expected_changes = {'Sentence':{'remove':3},'Word':{'remove':10},"Whitespace":{'remove':9},"Punctuation":{'remove':4},
                        'Paragraph':{'remove':1}
                       }
    
    get_text_structure = parse_change_text('Text',text,'')
    
    assert expected_changes == get_text_structure

def test_insert_text_count_english_punctuations():
    text = "Wait for it... awesome! More things to come. Why me?"
    expected_changes = {'Sentence':{'insert':3},'Word':{'insert':10},"Whitespace":{'insert':9},"Punctuation":{'insert':4},
                        'Paragraph':{'insert':1}
                       }
    
    get_text_structure = parse_change_text('Text','',text)
    
    assert expected_changes == get_text_structure


def test_change_text_count_english_punctuations():
    curr_text = "Wait for it... awesome! More things to come. Why me?"
    prev_text = "Waits for it... awesome!! More things to come. Why me?"
    expected_changes = {'Sentence':{'change':1},'Word':{'change':1},
                        "Punctuation":{'remove':1},
                        'Paragraph':{'change':1}
                        }
    get_text_structure = parse_change_text('Text', prev_text,curr_text)
    assert expected_changes == get_text_structure