# helper functions for handling mwparserfromhell / wikitext
import mwparserfromhell as mw

from mwedittypes.constants import *


def simple_node_class(mwnode, lang='en'):
    """e.g., "<class 'mwparserfromhell.nodes.heading.Heading'>" -> "Heading"."""
    if type(mwnode) == str:
        return 'Text'
    else:
        nc = str(type(mwnode)).split('.')[-1].split("'")[0]
        if nc == 'Wikilink':
            n_prefix = mwnode.title.split(':', maxsplit=1)[0].lower()
            if n_prefix in [m.lower() for m in MEDIA_PREFIXES + MEDIA_ALIASES.get(lang, [])]:
                nc = 'Media'
            elif n_prefix in [c.lower() for c in CAT_PREFIXES + CAT_ALIASES.get(lang, [])]:
                nc = 'Category'
        elif nc == 'Tag':
            tag_type = str(mwnode.tag)
            if tag_type in TEXT_FORMATTING_TAGS:
                return 'Text Formatting'
            elif tag_type in LIST_TAGS:
                return 'List'
            elif tag_type == 'table':
                return 'Table'
            elif tag_type in TABLE_ELEMENTS_TAGS:
                return 'Table Element'
            elif tag_type == 'gallery':
                return 'Gallery'
            elif tag_type == 'ref':
                return 'Reference'
            elif tag_type == 'noinclude':
                return 'Comment'
            # any others I missed -- e.g., div, meta, etc.
            else:
                return tag_type.capitalize() + ' Tag'
        return nc


def sec_to_name(mwsection, sidx):
    """Converts a section to an interpretible and unique name."""
    if sidx == 0:
        sectitle = 'Lede'
    else:
        try:
            sectitle = str(mwsection.nodes[0])
        except IndexError:
            sectitle = ''
    return f'{sidx}: {sectitle}'


def node_to_name(mwnode, lang='en'):
    """Converts a mwparserfromhell node to an interpretible name."""
    n_txt = mwnode.replace("\n", "\\n")
    if len(n_txt) > 13:
        return f'{simple_node_class(mwnode, lang)}: {n_txt[:10]}...'
    else:
        return f'{simple_node_class(mwnode, lang)}: {n_txt}'


def wikitext_to_plaintext(wt, lang='en'):
    """Helper function for converting wikitext to plaintext."""
    return ''.join([extract_text(n, lang) for n in mw.parse(wt).nodes])


def extract_text(mwnode, lang='en'):
    """Extract what text would be displayed from any node."""
    ntype = simple_node_class(mwnode, lang)
    if ntype == 'Text':
        return str(mwnode)
    elif ntype == 'HTMLEntity':
        return mwnode.normalize()
    elif ntype == 'Wikilink':
        if mwnode.text:
            return mwnode.text.strip_code()
        else:
            return mwnode.title.strip_code()
    elif ntype == 'ExternalLink' and mwnode.title:
        return mwnode.title.strip_code()
    # tables can have tons of nested references etc. so can't just go through standard strip_code
    elif ntype == 'Table':
        # don't collapse whitespace for tables because otherwise strip_code sometimes merges text across cells
        return mwnode.contents.strip_code(collapse=False)
    elif ntype == 'Text Formatting':
        return ''.join(extract_text(mwn) for mwn in mwnode.contents.nodes)
    # Heading, Template, Comment, Argument, Category, Media, References, URLs without display text
    # Tags not listed here (div, gallery, etc.) that almost never have true text content and can be super messy
    # Table elements (they duplicate the text if included)
    else:
        return ''


def find_nested_media(wikitext, is_gallery=False, max_link_length=240):
    """Case-insensitive search for media files (lacking brackets) in wikitext -- i.e. in Templates and Galleries.
    For setting max_link_length: https://commons.wikimedia.org/wiki/Commons:File_naming#Length

    In templates, image name is a parameter and all formatting/caption options are separate parameters
    but template-specific so there is no easy and consistent way to extract them. The best we can do
    is to extract the filename and detect when that has been edited.

    In galleries, each image is given its own line and formatting/caption options are evaluated just like
    they are for standard bracketed media links. Gallery images do not need a File: etc. prefix however.
    So for galleries, we also extract everything between filename and end-of-line as the media options.
    """
    lc_wt = wikitext.lower()
    media = []
    end = 0
    while True:
        m = EXTEN_PATTERN.search(lc_wt, pos=end)
        if m is None:
            break
        start, end = m.span()
        if end - start <= max_link_length:
            media_wikitext = wikitext[start:end]
            if is_gallery:
                end_of_line = wikitext.find('\n', end)
                if end_of_line == -1:  # no new-line at end of gallery
                    media_options = wikitext[end:]
                else:
                    media_options = wikitext[end:end_of_line]
                media_wikitext += media_options
            media.append(media_wikitext.strip())
    return media


def parse_image_options(img_options_wikitext, lang='en'):
    """Identify any formatting options and caption within media file syntax.

    There are a set of allowed keywords/parameters for media formatting that we have fully compiled a list of.
    Each parameter in a media file is checked against these formatting options and if it does not match,
    it is assumed to be the caption.

    For more info, see: https://www.mediawiki.org/wiki/Help:Images#Syntax
    """
    options = []
    caption = None
    if img_options_wikitext:
        lang_tags = {}
        for k in DEF_OPTION_TAGS:
            lang_tags[k] = DEF_OPTION_TAGS[k] + IMG_OPTION_ALIASES.get(lang, {}).get(k, [])
        for o in img_options_wikitext.split('|'):
            o = o.strip()
            if o in lang_tags['keywords']:
                options.append(o)
            elif o.split('=')[0] in lang_tags['params']:
                options.append(o)
            else:
                found = False
                for t in lang_tags['startswith']:
                    if o.startswith(t):
                        options.append(o)
                        found = True
                        break
                if not found:
                    for t in lang_tags['endswith']:
                        if o.endswith(t):
                            options.append(o)
                            found = True
                            break
                if not found:
                    caption = o

    return options, caption


def full_diff_to_simple(full_diff):
    """Extract simple edit type summary from full edit type response."""
    result = {}
    for ne in full_diff['node-edits']:
        if ne.type not in result:
            result[ne.type] = {}
        result[ne.type][ne.edittype] = result[ne.type].get(ne.edittype, 0) + 1
    te_types = set()
    for te in full_diff['text-edits']:
        if te.type not in result:
            result[te.type] = {}
            te_types.add(te.type)
        result[te.type][te.edittype] = result[te.type].get(te.edittype, 0) + te.count
    for tet in te_types:
        change = min(result[tet].get('insert', 0), result[tet].get('remove', 0))
        if change:
            result[tet]['change'] = change
            if 'insert' in result[tet]:
                if result[tet]['insert'] == change:
                    result[tet].pop('insert')
                else:
                    result[tet]['insert'] = result[tet]['insert'] - change
            if 'remove' in result[tet]:
                if result[tet]['remove'] == change:
                    result[tet].pop('remove')
                else:
                    result[tet]['remove'] = result[tet]['remove'] - change
    for ce in full_diff['context']:
        if ce.type not in result:
            result[ce.type] = {}
        result[ce.type][ce.edittype] = result[ce.type].get(ce.edittype, 0) + ce.count

    return result
