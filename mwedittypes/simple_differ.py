import re

import mwparserfromhell as mw

from mwedittypes.tokenizer import parse_change_text
from mwedittypes.utils import (
    find_nested_media,
    node_to_name,
    sec_to_name,
    simple_node_class,
    wikitext_to_plaintext,
)


# equivalent of main function
def get_diff(prev_wikitext, curr_wikitext, lang="en"):
    """Run through full process of getting diff between two wikitext revisions."""
    prev_tree = WikitextBag(wikitext=prev_wikitext, lang=lang)
    curr_tree = WikitextBag(wikitext=curr_wikitext, lang=lang)
    d = Differ(prev_tree, curr_tree)
    result = d.count_actions()
    return result


class Node:
    """
    Basic object for wrapping mwparserfromhell wikitext nodes
    """

    def __init__(self, name, ntype="Text", mwnode=None, section=None):
        self.name = name  # For debugging purposes
        self.ntype = ntype  # Type of node for result
        self.mwnode = mwnode
        self.text = str(mwnode)  # Text that is needed if unnesting the node
        # Content hash is used for quickly computing equality for most nodes.
        # Generally this just a simple hash of self.text (wikitext associated with a node) but
        # the text hash for sections is based on all the content within the section
        # so it can be used for pruning while self.text is just the text that creates the section
        # e.g., "==Section==\nThis is a section." would have as text "==Section==" but hash the full.
        # so the Differ doesn't identify a section as changing when content within it is changed
        self.content_hash = hash(self.text)
        self.section = section  # section that the node is a part of -- useful for formatting final diff

    def unnest(self, lang="en"):
        """Expand a node to also include all of its subnodes.
        This approach starts with a single wikitext node -- e.g., a single Tag node with nested link nodes etc.:
        <ref>{{cite web|title=[[Gallery]]|url=http://digital.belvedere.at|publisher=Digitales Belvedere}}</ref>
        and splits it into its component parts (ref, template, wikilink, externallink) to find fine-grained changes.
        """
        nodes = []
        # Using string mixin methods such as wt.find(x) for subnodes in the for
        # loop below means doing str(wt) everytime, which is expensive because
        # it recursively converts each node to str. Better to create a string using
        # the node's text and use built-in string methods instead.
        if self.ntype == "Gallery":
            # strip leading / trailing gallery tags so parser correctly parses everything in between
            # otherwise links, formatting, etc. is treated as text
            gallery_start = self.text.find(">")
            gallery_end = self.text.rfind("<")
            try:
                # the <br> is a hack; it'll be skipped in the ifilter loop; otherwise first image skipped
                wt = mw.parse(
                    "<br>" + self.text[gallery_start + 1 : gallery_end],
                    skip_style_tags=True,
                )
            except Exception:  # fallback
                wt = mw.parse(self.mwnode)
        else:
            wt = mw.parse(self.mwnode)
        for idx, nn in enumerate(wt.ifilter(recursive=True)):
            if idx == 0:
                continue  # skip root node -- already set
            ntype = simple_node_class(nn, lang)
            if ntype == "Text":
                # media w/o bracket will be IDed as text by mwparserfromhell
                # templates / galleries are where we find this nested media
                if self.ntype == "Template" or self.ntype == "Gallery":
                    for m in find_nested_media(
                        str(nn), is_gallery=(self.ntype == "Gallery")
                    ):
                        nn_node = Node(
                            f"Media: {m[:10]}...",
                            ntype="Media",
                            mwnode=m,
                            section=self.section,
                        )
                        nodes.append(nn_node)
            # tables are very highly-structured and produce a ton of nodes (each cell and more)
            # so we just extract links, formatting, etc. that appears in the table and skip the cells
            # because changes to those will generally be caught in the overall table changes and text changes
            # this leads to much faster parsing in exchange for not knowing how many table cells were edited
            elif ntype == "Table Element":
                pass
            else:
                nn_node = Node(
                    node_to_name(nn, lang=lang),
                    ntype=ntype,
                    mwnode=nn,
                    section=self.section,
                )
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
        wt = mw.parse(wikitext, skip_style_tags=True)
        for sidx, s in enumerate(wt.get_sections(flat=True)):
            if s:
                sec_id = sec_to_name(s, sidx)
                s_node = Node(sec_id, ntype="Section", mwnode=s, section=sec_id)
                self.secname_to_text[sec_id] = s_node.text
                self.nodes[s_node.content_hash] = self.nodes.get(
                    s_node.content_hash, []
                ) + [s_node]
                for (
                    n
                ) in (
                    s.nodes
                ):  # this is just top-level of nodes so e.g., table but not all the table rows etc.
                    ntype = simple_node_class(n, self.lang)
                    if ntype != "Text":
                        n_node = Node(
                            node_to_name(n, self.lang),
                            ntype=ntype,
                            mwnode=n,
                            section=s_node.name,
                        )
                        self.nodes[n_node.content_hash] = self.nodes.get(
                            n_node.content_hash, []
                        ) + [n_node]
                if "''" in s_node.text:
                    for line in s_node.text.split("\n"):
                        if "''" in line:
                            line, bt_found = re.subn("'{5}", "", line)
                            for _ in range(bt_found // 2):
                                tfn = Node(
                                    "Bold-Italic",
                                    ntype="Text Formatting",
                                    mwnode="'''''",
                                    section=s_node.name,
                                )
                                self.nodes[tfn.content_hash] = self.nodes.get(
                                    tfn.content_hash, []
                                ) + [tfn]
                            line, b_found = re.subn("'{3}", "", line)
                            for _ in range(b_found // 2):
                                tfn = Node(
                                    "Bold",
                                    ntype="Text Formatting",
                                    mwnode="'''",
                                    section=s_node.name,
                                )
                                self.nodes[tfn.content_hash] = self.nodes.get(
                                    tfn.content_hash, []
                                ) + [tfn]
                            line, t_found = re.subn("'{2}", "", line)
                            for _ in range(t_found // 2):
                                tfn = Node(
                                    "Italic",
                                    ntype="Text Formatting",
                                    mwnode="''",
                                    section=s_node.name,
                                )
                                self.nodes[tfn.content_hash] = self.nodes.get(
                                    tfn.content_hash, []
                                ) + [tfn]

    def expand_nested(self):
        """Expand nested nodes in tree -- e.g., Ref tags with templates/links contained in them."""
        to_add = {}
        for n_hash in self.nodes:
            for n in self.nodes[n_hash]:
                if n.ntype not in (
                    "Section",
                    "Heading",
                    "Text",
                ):  # leaves tag, link, etc.
                    for nn in n.unnest(self.lang):
                        to_add[nn.content_hash] = to_add.get(nn.content_hash, []) + [nn]

        for n_hash in to_add:
            for n in to_add[n_hash]:
                self.nodes[n_hash] = self.nodes.get(n_hash, []) + [n]


class Differ:
    """
    Find structural differences between two WikitextBags
    """

    def __init__(self, t1, t2, expand_nodes=True):
        self.t1 = t1
        self.t2 = t2
        self.diff(expand_nodes=expand_nodes)

    def diff(self, expand_nodes=True):
        # first pass on high-level nodes to prune down to just the ones that changed
        self.sym_diff()
        if expand_nodes:
            # expand out changed nodes and re-diff
            self.t1.expand_nested()
            self.t2.expand_nested()
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
                    t2n[n_hash] = t2n[n_hash][: abs(diff)]
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
                if n.ntype == "Section":
                    prev_text_sections.add(n.section)
        curr_ntypes = {}
        for n_hash in self.t2.nodes:
            for n in self.t2.nodes[n_hash]:
                curr_ntypes[n.ntype] = curr_ntypes.get(n.ntype, 0) + 1
                if n.ntype == "Section":
                    curr_text_sections.add(n.section)

        all_ntypes = set(prev_ntypes.keys()).union(set(curr_ntypes.keys()))
        for n_type in all_ntypes:
            # change is overlap in nodes; removal are extras in previous; insert are extras in current
            chg = min(prev_ntypes.get(n_type, 0), curr_ntypes.get(n_type, 0))
            rem = prev_ntypes.get(n_type, 0) - chg
            ins = curr_ntypes.get(n_type, 0) - chg
            edit_types[n_type] = {}
            if chg > 0:
                edit_types[n_type]["change"] = chg
            if rem > 0:
                edit_types[n_type]["remove"] = rem
            if ins > 0:
                edit_types[n_type]["insert"] = ins

        lang = self.t1.lang
        prev_text = ""
        for s in prev_text_sections:
            prev_text += wikitext_to_plaintext(self.t1.secname_to_text[s], lang=lang)
        curr_text = ""
        for s in curr_text_sections:
            curr_text += wikitext_to_plaintext(self.t2.secname_to_text[s], lang=lang)

        text_changes = parse_change_text(prev_text, curr_text, lang=lang)
        edit_types.update(text_changes)

        return edit_types
