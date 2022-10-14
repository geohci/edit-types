from context import StructuredEditTypes, prev_wikitext

# NOTE: these tests focus specifically on the additional node details and assume that the edittypes_summary tests
# do the heavy work to ensure that text/context changes are correctly processed.

def test_text_from_link():
    curr_wikitext = prev_wikitext.replace("[[Vienna]]",
                                          "[[Vienna|same link different text]]",
                                          1)
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    expected_node_edits = 1
    assert len(full_diff['node-edits']) == expected_node_edits, full_diff
    wikilink = full_diff['node-edits'][0]
    assert wikilink.type == 'Wikilink', wikilink
    assert wikilink.edittype == 'change', wikilink
    assert wikilink.name == "Vienna", wikilink
    assert len(wikilink.changes) == 1, wikilink
    assert wikilink.changes[0][0] == 'text', wikilink
    assert wikilink.changes[0][1] is None and wikilink.changes[0][2] == 'same link different text', wikilink

def test_change_template():
    curr_wikitext = prev_wikitext.replace('{{Use dmy dates|date=April 2017}}\n',
                                          '{{Use dmy dates|date=April 2018}}\n',
                                          1)
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    expected_node_edits = 1
    assert len(full_diff['node-edits']) == expected_node_edits, full_diff
    tmplt = full_diff['node-edits'][0]
    assert tmplt.type == 'Template', tmplt
    assert tmplt.edittype == 'change', tmplt
    assert tmplt.name == "Use dmy dates", tmplt
    assert len(tmplt.changes) == 1, tmplt
    assert tmplt.changes[0][0] == 'parameter', tmplt
    assert tmplt.changes[0][1] == ('date', 'April 2017') and tmplt.changes[0][2] == ('date', 'April 2018'), tmplt


def test_unbracketed_media():
    curr_wikitext = prev_wikitext.replace('===Works===\n',
                                          '===Works===\n<gallery>\nFile:Carl Aigen Fischmarkt.jpg|thumb|Caption\n</gallery>',
                                          1)
    full_diff = StructuredEditTypes(prev_wikitext, curr_wikitext, lang='en').get_diff()
    expected_node_edits = 2
    assert len(full_diff['node-edits']) == expected_node_edits, full_diff
    # NOTE: the order of the node edits is actually arbitrary so if it changes, that's fine and should be updated
    media = full_diff['node-edits'][0]
    assert media.type == 'Media', media
    assert media.edittype == 'insert', media
    assert media.name == "Carl Aigen Fischmarkt.jpg", media
    assert len(media.changes) == 3, media
    mc = media.changes
    assert mc[0][0] == 'filename', media
    assert mc[0][1] is None and mc[0][2] == "Carl Aigen Fischmarkt.jpg", media
    assert mc[1][0] == 'caption', media
    assert mc[1][1] is None and mc[1][2] == "Caption", media
    assert mc[2][0] == 'option', media
    assert mc[2][1] is None and mc[2][2] == "thumb", media
    gallery = full_diff['node-edits'][1]
    assert gallery.type == 'Gallery', gallery
    assert gallery.edittype == 'insert', gallery
    assert gallery.name is None, gallery
    assert len(gallery.changes) == 0, gallery
