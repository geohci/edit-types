import time

import mwparserfromhell as mw

from mwsimpleedittypes.constants import *
from mwsimpleedittypes.tokenizer import *


# equivalent of main function
def get_diff(prev_wikitext, curr_wikitext, lang='en', timeout=2):
    """Run through full process of getting diff between two wikitext revisions."""
    prev_tree = WikitextBag(wikitext=prev_wikitext, lang=lang)
    curr_tree = WikitextBag(wikitext=curr_wikitext, lang=lang)
    d = Differ(prev_tree, curr_tree, timeout=timeout)
    result = d.count_actions()
    return result


# helper functions for handling mwparserfromhell / wikitext
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
    """Converts a section to a unique name."""
    if sidx == 0:
        sectitle = 'Lede'
    else:
        sectitle = str(mwsection.nodes[0])
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


class Node():
    """
    Basic object for wrapping mwparserfromhell wikitext nodes
    """

    def __init__(self, name, ntype='Text', text_hash=None, text='', section=None):
        self.name = name  # For debugging purposes
        self.ntype = ntype  # Type of node for result
        self.text = str(text)  # Text that is needed if unnesting the node
        # Used for quickly computing equality for most nodes.
        # Generally this just a simple hash of self.text (wikitext associated with a node) but
        # the text hash for sections and paragraphs is based on all the content within the section/paragraph
        # so it can be used for pruning while self.text is just the text that creates the section/paragraph
        # e.g., "==Section==\nThis is a section." would have as text "==Section==" but hash the full.
        # so the Differ doesn't identify a section/paragraph as changing when content within it is changed
        if text_hash is None:
            self.text_hash = hash(self.text)
        else:
            self.text_hash = hash(str(text_hash))
        self.section = section  # section that the node is a part of -- useful for formatting final diff

    def unnest(self, lang='en'):
        """Expand a node to also include all of its subnodes.

        This approach starts with a single wikitext node -- e.g., a single Tag node with nested link nodes etc.:
        <ref>{{cite web|title=[[Gallery]]|url=http://digital.belvedere.at|publisher=Digitales Belvedere}}</ref>
        and splits it into its component parts (ref, template, wikilink, externallink) to identify fine-grained changes.
        """
        nodes = []
        # Using string mixin methods such as wt.find(x) for subnodes in the for
        # loop below means doing str(wt) everytime, which is expensive because
        # it recursively converts each node to str. Better to create a string using
        # the node's text and use built-in string methods instead.
        node_str = self.text
        if self.ntype == 'Gallery':
            # strip leading / trailing gallery tags so parser correctly parses everything in between
            # otherwise links, formatting, etc. is treated as text
            gallery_start = self.text.find('>')
            gallery_end = self.text.rfind('<')
            try:
                # the <br> is a hack; it'll be skipped in the ifilter loop; otherwise first image skipped
                node_str = '<br>' + self.text[gallery_start+1:gallery_end]
                wt = mw.parse(node_str)
            except Exception:  # fallback
                node_str = self.text
                wt = mw.parse(node_str)
        else:
            wt = mw.parse(node_str)
        for idx, nn in enumerate(wt.ifilter(recursive=True)):
            if idx == 0:
                continue  # skip root node -- already set
            ntype = simple_node_class(nn, lang)
            if ntype == 'Text':
                # media w/o bracket will be IDed as text by mwparserfromhell
                # templates / galleries are where we find this nested media
                if self.ntype == 'Template' or self.ntype == 'Gallery':
                    media = find_nested_media(str(nn))
                    for m in media:
                        nn_node = Node(f'Media: {m[:10]}...',
                                       ntype='Media',
                                       text=m,
                                       section=self.section)
                        nodes.append(nn_node)
            # tables are very highly-structured and produce a ton of nodes (each cell and more)
            # so we just extract links, formatting, etc. that appears in the table and skip the cells
            # because changes to those will generally be caught in the overall table changes and text changes
            # this leads to much faster parsing in exchange for not knowing how many table cells were edited
            elif ntype == 'Table Element':
                pass
            else:
                nn_node = Node(node_to_name(nn, lang=lang), ntype=ntype, text=nn, section=self.section)
                nodes.append(nn_node)
        return nodes


class WikitextBag:
    """
    Structure for extracting and holding an unordered collection of wikitext nodes based on mwparserfromhell
    """

    def __init__(self, wikitext, lang="en"):
        self.lang = lang
        self.secname_to_text = {}
        self.nodes = {}
        self.wikitext_to_bagofnodes(wikitext)

    def wikitext_to_bagofnodes(self, wikitext):
        """Build bag of document nodes from Wikipedia article.

        Includes special Section nodes that will cover any changes made to that section.
        Excludes text, which will be processed later (and is captured by the Section nodes).
        """
        wt = mw.parse(wikitext)
        for sidx, s in enumerate(wt.get_sections(flat=True)):
            if s:
                sec_hash = sec_to_name(s, sidx)
                sec_text = ''.join([str(n) for n in s.nodes])
                self.secname_to_text[sec_hash] = sec_text
                s_node = Node(sec_hash, ntype="Section", text=sec_text, section=sec_hash)
                self.nodes[s_node.text_hash] = self.nodes.get(s_node.text_hash, []) + [s_node]
                for n in s.nodes:  # this is just top-level of nodes so e.g., table but not all the table rows etc.
                    ntype = simple_node_class(n, self.lang)
                    if ntype != 'Text':
                        n_node = Node(node_to_name(n, self.lang), ntype=ntype, text=n, section=s_node.name)
                        self.nodes[n_node.text_hash] = self.nodes.get(n_node.text_hash, []) + [n_node]

    def expand_nested(self):
        """Expand nested nodes in tree -- e.g., Ref tags with templates/links contained in them."""
        to_add = {}
        for n_hash in self.nodes:
            for n in self.nodes[n_hash]:
                if n.ntype not in ('Section', 'Heading', 'Text'):  # leaves tag, link, etc.
                    for nn in n.unnest(self.lang):
                        to_add[nn.text_hash] = to_add.get(nn.text_hash, []) + [nn]

        for n_hash in to_add:
            for n in to_add[n_hash]:
                self.nodes[n_hash] = self.nodes.get(n_hash, []) + [n]


class Differ:
    """
    Find structural differences between two WikitextBags
    """

    def __init__(self, t1, t2, timeout=2, expand_nodes=True):
        self.timeout = time.time() + timeout
        self.t1 = t1
        self.t2 = t2
        self.diff(expand_nodes=expand_nodes)

    def diff(self, expand_nodes=True):
        # first pass on high-level nodes to prune down to just the ones that changed
        self.sym_diff()
        if expand_nodes and time.time() < self.timeout:
            # expand out changed nodes and re-diff
            self.t1.expand_nested()
            self.t2.expand_nested()
            # for second pass, we change text formatting to be hashes of the formatting type and not the text within
            # if we do this from the start, we'll miss nested changes but at this point we only want to keep the
            # text formatting changes if e.g., it goes from bold -> italics but content within the formatting
            # are now represented by their own nodes
            to_move = []
            for n_hash in self.t1.nodes:
                for nidx in range(len(self.t1.nodes[n_hash])-1, -1, -1):
                    n = self.t1.nodes[n_hash][nidx]
                    if n.ntype == 'Text Formatting':
                        n.text_hash = hash(str(mw.parse(n.text).nodes[0].tag))
                        to_move.append(self.t1.nodes[n_hash].pop(nidx))
            for n in to_move:
                self.t1.nodes[n.text_hash] = self.t1.nodes.get(n.text_hash, []) + [n]
            to_move = []
            for n_hash in self.t2.nodes:
                for nidx in range(len(self.t2.nodes[n_hash])-1, -1, -1):
                    n = self.t2.nodes[n_hash][nidx]
                    if n.ntype == 'Text Formatting':
                        n.text_hash = hash(str(mw.parse(n.text).nodes[0].tag))
                        to_move.append(self.t2.nodes[n_hash].pop(nidx))
            for n in to_move:
                self.t2.nodes[n.text_hash] = self.t2.nodes.get(n.text_hash, []) + [n]
            self.sym_diff()

    def sym_diff(self):
        # prune down node dictionaries to just unmatched nodes
        t1n = self.t1.nodes
        t2n = self.t2.nodes
        t1n_hashes = list(t1n.keys())
        for n_hash in t1n_hashes:
            # if this doesn't match, can leave t1n dictionary unchanged because all nodes should be kept for this hash
            if n_hash in t2n:
                diff = len(t1n[n_hash]) - len(t2n[n_hash])
                # fully-matched: remove from both sides
                if diff == 0:
                    t1n.pop(n_hash)
                    t2n.pop(n_hash)
                # extras in t1: remove from t2 and keep just extras in t1
                elif diff > 0:
                    t2n.pop(n_hash)
                    t1n[n_hash] = t1n[n_hash][:diff]
                # extras in t2: remove from t1 and keep just extras in t2
                elif diff < 0:
                    t1n.pop(n_hash)
                    t2n[n_hash] = t2n[n_hash][:abs(diff)]
        # no need to loop through t2n because what's left in it doesn't have any matches

    def count_actions(self):
        """Explain differences."""
        edit_types = {}
        prev_text_sections = set()
        curr_text_sections = set()

        # aggregate by node type to identify non-matching nodes
        prev_ntypes = {}
        for n_hash in self.t1.nodes:
            for n in self.t1.nodes[n_hash]:
                prev_ntypes[n.ntype] = prev_ntypes.get(n.ntype, 0) + 1
                if n.ntype == 'Section':
                    prev_text_sections.add(n.section)
        curr_ntypes = {}
        for n_hash in self.t2.nodes:
            for n in self.t2.nodes[n_hash]:
                curr_ntypes[n.ntype] = curr_ntypes.get(n.ntype, 0) + 1
                if n.ntype == 'Section':
                    curr_text_sections.add(n.section)

        all_ntypes = set(prev_ntypes.keys()).union(set(curr_ntypes.keys()))
        for n_type in all_ntypes:
            # change is overlap in nodes; removal are extras in previous; insert are extras in current
            chg = min(prev_ntypes.get(n_type, 0), curr_ntypes.get(n_type, 0))
            rem = prev_ntypes.get(n_type, 0) - chg
            ins = curr_ntypes.get(n_type, 0) - chg
            edit_types[n_type] = {}
            if chg > 0:
                edit_types[n_type]['change'] = chg
            if rem > 0:
                edit_types[n_type]['remove'] = rem
            if ins > 0:
                edit_types[n_type]['insert'] = ins

        prev_text = ''
        for s in prev_text_sections:
            prev_text += ''.join([extract_text(n, self.t1.lang) for n in mw.parse(self.t1.secname_to_text[s]).nodes])
        curr_text = ''
        for s in curr_text_sections:
            curr_text += ''.join([extract_text(n, self.t2.lang) for n in mw.parse(self.t2.secname_to_text[s]).nodes])

        text_changes = parse_change_text(prev_text, curr_text, self.t1.lang)
        edit_types.update(text_changes)

        return edit_types


def parse_change_text(prev_wikitext='', curr_wikitext='', lang='en'):
    # Initialize tokenizer class
    tokenizer = Tokenizer(ENGLISH_UNICODE, NON_ENGLISH_UNICODE, lang=lang)
    result = {}

    prev_tokenizer = tokenizer.tokenize_and_get_occurence(prev_wikitext)
    curr_tokenizer = tokenizer.tokenize_and_get_occurence(curr_wikitext)

    for text_category in curr_tokenizer.keys():
        items_diff_list = list(
            set(curr_tokenizer[text_category].items()) ^ set(prev_tokenizer[text_category].items()))
        for item in items_diff_list:
            diff = curr_tokenizer[text_category].get(item[0], 0) - prev_tokenizer[text_category].get(item[0], 0)
            result[text_category] = dict(result.get(text_category, {}), **{item[0]: diff})

        # Get the maximum value between the sum of positives and sum of negatives
        if len(result.get(text_category, {})) > 0:
            removals = sum(abs(item) for item in result[text_category].values() if item < 0)
            additions = sum(abs(item) for item in result[text_category].values() if item > 0)
            change = min(removals, additions)
            result[text_category] = {}
            removals -= change
            additions -= change

            if removals > 0:
                result[text_category]['remove'] = removals

            if additions > 0:
                result[text_category]['insert'] = additions

            if change > 0:
                result[text_category]['change'] = change

    return result
