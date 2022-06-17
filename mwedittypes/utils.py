# helper functions for handling mwparserfromhell / wikitext
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


def find_nested_media(wikitext, max_link_length=240):
    """Case-insensitive search for media files (lacking brackets) in wikitext -- i.e. in Templates and Galleries.
    For setting max_link_length: https://commons.wikimedia.org/wiki/Commons:File_naming#Length
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
            media.append(wikitext[start:end].strip())
    return media
