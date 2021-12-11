import time

from anytree import Node, RenderTree, PostOrderIter, PreOrderIter, NodeMixin
from anytree.util import leftsibling
import mwparserfromhell


class OrderedNode(NodeMixin):  # Add Node feature
    def __init__(self, name, ntype='Text', text_hash=None, idx=-1, text='', char_offset=-1, parent=None, children=None):
        super(OrderedNode, self).__init__()
        self.name = name  # For debugging purposes
        self.ntype = ntype  # Different node types can be treated differently when computing equality
        self.text = str(text)  # Text that can then be passed to a diffing library
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
        self.idx = idx  # Used by Differ -- Post order on tree from 0...# nodes - 1
        self.char_offset = char_offset  # make it easy to find node in section text
        self.parent = parent
        if children:
            self.children = children

    def leftmost(self):
        return self.idx if self.is_leaf else self.children[0].leftmost()


def simple_node_class(node):
    """e.g., "<class 'mwparserfromhell.nodes.heading.Heading'>" -> "Heading"."""
    if type(node) == str:
        return 'Text'
    else:
        return str(type(node)).split('.')[-1].split("'")[0]

def sec_to_name(s, idx):
    """Converts a section to an interpretible name."""
    return f'S#{idx}: {s.nodes[0].title} (L{s.nodes[0].level})'


def node_to_name(n):
    """Converts a mwparserfromhell node to an interpretible name."""
    n_txt = n.replace("\n", "\\n")
    if len(n_txt) > 13:
        return f'{simple_node_class(n)}: {n_txt[:10]}...'
    else:
        return f'{simple_node_class(n)}: {n_txt}'

def extract_text(node):
    """Extract what text would be displayed from any node."""
    ntype = simple_node_class(node)
    if ntype == 'Text' or ntype == 'HTMLEntity':
        return str(node)
    elif ntype == 'Wikilink':
        if node.text:
            return str(node.text)
        else:
            return str(node.title)
    elif ntype == 'ExternalLink' and node.title:
        return str(node.title)
    elif ntype == 'Tag' and node.tag != 'ref':
        return str(node.contents)
    else:  # Heading, Table, Template, HTMLEntity, Comment, Argument
        return ''

def sec_node_tree(wt):
    """Build tree of document nodes from Wikipedia article.

    This approach builds a tree with an artificial 'root' node on the 1st level,
    all of the article sections on the 2nd level (including an artificial Lede section),
    and all of the text, link, template, etc. nodes nested under their respective sections.
    """
    root = OrderedNode('root', ntype="Article")
    secname_to_text = {}
    for sidx, s in enumerate(wt.get_sections()):
        if s:
            sec_hash = sec_to_name(s, sidx)
            sec_text = str(s.nodes[0])
            for n in s.nodes[1:]:
                if simple_node_class(n) == 'Heading':
                    break
                sec_text += str(n)
            secname_to_text[sec_hash] = sec_text
            s_node = OrderedNode(sec_hash, ntype="Heading", text=s.nodes[0], text_hash=sec_text, char_offset=0, parent=root)
            char_offset = len(s_node.text)
            for n in s.nodes[1:]:
                if simple_node_class(n) == 'Heading':
                    break
                n_node = OrderedNode(node_to_name(n), ntype=simple_node_class(n), text=n, char_offset=char_offset, parent=s_node)
                char_offset += len(str(n))
    return root, secname_to_text

def format_diff(node):
    """Convert OrderedNode object into simple dictionary."""
    result = {'name':node.name,
              'type':node.ntype,
              'text':node.text,
              'offset':node.char_offset}
    if node.ntype == 'Heading':
        result['section'] = node.name
    else:
        result['section'] = node.parent.name
    return result


def format_result(diff, sections1, sections2):
    result = {'remove':[], 'insert':[], 'change':[], 'move':[], 'sections-prev':{}, 'sections-curr':{}}
    for n in diff['remove']:
        n_res = format_diff(n)
        result['remove'].append(n_res)
        result['sections-prev'][n_res['section']] = sections1[n_res['section']]
    for n in diff['insert']:
        n_res = format_diff(n)
        result['insert'].append(n_res)
        result['sections-curr'][n_res['section']] = sections2[n_res['section']]
    for pn, cn in diff['change']:
        pn_res = format_diff(pn)
        cn_res = format_diff(cn)
        result['change'].append({'prev':pn_res, 'curr':cn_res})
        result['sections-prev'][pn_res['section']] = sections1[pn_res['section']]
        result['sections-curr'][cn_res['section']] = sections2[cn_res['section']]
    for pn, cn in diff['move']:
        pn_res = format_diff(pn)
        cn_res = format_diff(cn)
        result['move'].append({'prev':pn_res, 'curr':cn_res})
        result['sections-prev'][pn_res['section']] = sections1[pn_res['section']]
        result['sections-curr'][cn_res['section']] = sections2[cn_res['section']]
    return result

def detect_moves(diff):
    """Detect when nodes were moved (as opposed to removed + inserted)."""
    prev_moved = []
    curr_moved = []
    for i,pn in enumerate(diff['remove']):
        for j,cn in enumerate(diff['insert']):
            if pn.ntype == cn.ntype and pn.text_hash == cn.text_hash:
                prev_moved.append(i)
                curr_moved.append(j)
                break
    diff['move'] = []
    if prev_moved:
        for i in range(len(prev_moved)):
            pn = diff['remove'][prev_moved[i]]
            cn = diff['insert'][curr_moved[i]]
            diff['move'].append((pn, cn))
        prev_moved = sorted(prev_moved, reverse=True)
        for i in prev_moved:
            diff['remove'].pop(i)
        curr_moved = sorted(curr_moved, reverse=True)
        for i in curr_moved:
            diff['insert'].pop(i)


def section_mapping(result, s1, s2):
    """Build mapping of sections between previous and current versions of article."""
    prev = list(s1.keys())
    curr = list(s2.keys())
    p_to_c = {}
    c_to_p = {}
    removed = []
    for n in result['remove']:
        if n['type'] == 'Heading':
            for i, s in enumerate(prev):
                if s == n['name']:
                    removed.append(i)
                    break
    for idx in sorted(removed, reverse=True):
        p_to_c[prev[idx]] = None
        prev.pop(idx)
    inserted = []
    for n in result['insert']:
        if n['type'] == 'Heading':
            for i, s in enumerate(curr):
                if s == n['name']:
                    inserted.append(i)
                    break
    for idx in sorted(inserted, reverse=True):
        c_to_p[curr[idx]] = None
        curr.pop(idx)

    # changes happen in place so don't effect structure of doc and can be ignored

    for c in result['move']:
        pn = c['prev']
        cn = c['curr']
        if pn['type'] == 'Heading':
            prev_idx = None
            curr_idx = None
            for i, s in enumerate(prev):
                if s == pn['name']:
                    prev_idx = i
                    break
            for i, s in enumerate(curr):
                if s == cn['name']:
                    curr_idx = i
                    break
            if prev_idx is not None and curr_idx is not None:
                s = curr.pop(curr_idx)
                curr.insert(prev_idx, s)

    for i in range(len(prev)):
        p_to_c[prev[i]] = curr[i]
        c_to_p[curr[i]] = prev[i]

    return p_to_c, c_to_p


def merge_text_changes(result, s1, s2):
    """Replace isolated text changes with section-level text changes."""
    p_to_c, c_to_p = section_mapping(result, s1, s2)
    changes = []
    prev_secs_checked = set()
    curr_secs_checked = set()
    for idx in range(len(result['remove']) - 1, -1, -1):
        r = result['remove'][idx]
        if r['type'] == 'Text':
            prev_sec = r['section']
            if prev_sec not in prev_secs_checked:
                prev_secs_checked.add(prev_sec)
                prev_text = ''.join([extract_text(n) for n in mwparserfromhell.parse(s1[prev_sec]).nodes])
                curr_sec = p_to_c[prev_sec]
                curr_secs_checked.add(curr_sec)
                if curr_sec is None:
                    changes.append({'prev': {'name': node_to_name(prev_text), 'type': 'Text', 'text': prev_text,
                                             'section': prev_sec, 'offset': 0}})
                else:
                    curr_text = ''.join([extract_text(n) for n in mwparserfromhell.parse(s2[curr_sec]).nodes])
                    if prev_text != curr_text:
                        changes.append({'prev': {'name': node_to_name(prev_text), 'type': 'Text', 'text': prev_text,
                                                 'section': prev_sec, 'offset': 0},
                                        'curr': {'name': node_to_name(curr_text), 'type': 'Text', 'text': curr_text,
                                                 'section': curr_sec, 'offset': 0}})
            result['remove'].pop(idx)
    for idx in range(len(result['insert']) - 1, -1, -1):
        i = result['insert'][idx]
        if i['type'] == 'Text':
            curr_sec = i['section']
            if curr_sec not in curr_secs_checked:
                curr_secs_checked.add(curr_sec)
                curr_text = ''.join([extract_text(n) for n in mwparserfromhell.parse(s2[curr_sec]).nodes])
                prev_sec = c_to_p[curr_sec]
                prev_secs_checked.add(prev_sec)
                if prev_sec is None:
                    changes.append({'curr': {'name': node_to_name(curr_text), 'type': 'Text', 'text': curr_text,
                                             'section': curr_sec, 'offset': 0}})
                else:
                    prev_text = ''.join([extract_text(n) for n in mwparserfromhell.parse(s1[prev_sec]).nodes])
                    if prev_text != curr_text:
                        changes.append({'prev': {'name': node_to_name(prev_text), 'type': 'Text', 'text': prev_text,
                                                 'section': prev_sec, 'offset': 0},
                                        'curr': {'name': node_to_name(curr_text), 'type': 'Text', 'text': curr_text,
                                                 'section': curr_sec, 'offset': 0}})
            result['insert'].pop(idx)
    for idx in range(len(result['change']) - 1, -1, -1):
        pn = result['change'][idx]['prev']
        cn = result['change'][idx]['curr']
        if pn['type'] == 'Text':
            prev_sec = pn['section']
            if prev_sec not in prev_secs_checked:
                prev_secs_checked.add(prev_sec)
                prev_text = ''.join([extract_text(n) for n in mwparserfromhell.parse(s1[prev_sec]).nodes])
                curr_sec = cn['section']
                curr_text = ''.join([extract_text(n) for n in mwparserfromhell.parse(s2[curr_sec]).nodes])
                if prev_text != curr_text:
                    changes.append({'prev': {'name': node_to_name(prev_text), 'type': 'Text', 'text': prev_text,
                                             'section': prev_sec, 'offset': 0},
                                    'curr': {'name': node_to_name(curr_text), 'type': 'Text', 'text': curr_text,
                                             'section': curr_sec, 'offset': 0}})
            result['change'].pop(idx)

    for c in changes:
        if 'prev' in c and 'curr' in c:
            result['change'].append(c)
        elif 'prev' in c:
            result['remove'].append(c['prev'])
        elif 'curr' in c:
            result['insert'].append(c['curr'])


class Differ:

    def __init__(self, t1, t2, timeout=2):
        self.t1 = [n for n in PostOrderIter(t1)]
        self.t2 = [n for n in PostOrderIter(t2)]
        self.prune_trees()
        for i, n in enumerate(self.t1):
            n.idx = i
        for i, n in enumerate(self.t2):
            n.idx = i
        self.timeout = time.time() + timeout
        self.ins_cost = 1
        self.rem_cost = 1
        self.chg_cost = 1
        self.nodetype_chg_cost = 10  # arbitrarily high to encourage remove+insert when node types change

        # Permanent store of transactions such that transactions[x][y] is the minimum
        # transactions to get from the sub-tree rooted at node x (in tree1) to the sub-tree
        # rooted at node y (in tree2).
        self.transactions = {None: {}}
        # Indices for each transaction, to avoid high performance cost of creating the
        # transactions multiple times
        self.transaction_to_idx = {None: {None: 0}}
        # All possible transactions
        self.idx_to_transaction = [(None, None)]

        idx_transaction = 1  # starts with nulls inserted

        transactions = {None: {None: []}}

        # Populate transaction stores
        for i in range(0, len(self.t1)):
            transactions[i] = {None: []}
            self.transaction_to_idx[i] = {None: idx_transaction}
            idx_transaction += 1
            self.idx_to_transaction.append((i, None))
            for j in range(0, len(self.t2)):
                transactions[None][j] = []
                transactions[i][j] = []
                self.transaction_to_idx[None][j] = idx_transaction
                idx_transaction += 1
                self.idx_to_transaction.append((None, j))
                self.transaction_to_idx[i][j] = idx_transaction
                idx_transaction += 1
                self.idx_to_transaction.append((i, j))
            self.transactions[i] = {}
        self.populate_transactions(transactions)

    def prune_trees(self):
        """Quick heuristic preprocessing to reduce tree differ time.

        Prune nodes from any sections that align across revisions to reduce tree size while maintaining structure.
        """
        t1_sections = [n for n in self.t1 if n.ntype == "Heading"]
        t2_sections = [n for n in self.t2 if n.ntype == "Heading"]
        prune = []
        for secnode1 in t1_sections:
            for sn2_idx in range(len(t2_sections)):
                secnode2 = t2_sections[sn2_idx]
                if secnode1.text_hash == secnode2.text_hash:
                    prune.append(secnode1)
                    prune.append(secnode2)
                    t2_sections.pop(sn2_idx)  # only match once
                    break
        for n in prune:
            # only keep section children and remove all other nodes
            n.children = [c for c in n.children if c.ntype == "Heading"]

        # remove nodes from t1/t2 structures
        for i in range(len(self.t1) - 1, -1, -1):
            if not self.t1[i].name == 'root' and self.t1[i].parent is None:
                self.t1.pop(i)
        for i in range(len(self.t2) - 1, -1, -1):
            if not self.t2[i].name == 'root' and self.t2[i].parent is None:
                self.t2.pop(i)

    def get_key_roots(self, tree):
        """Get keyroots (node has a left sibling or is the root) of a tree"""
        for on in tree:
            if on.is_root or leftsibling(on) is not None:
                yield on

    def populate_transactions(self, transactions):
        """Populate self.transactions with minimum transactions between all possible trees"""
        for kr1 in self.get_key_roots(self.t1):
            # Make transactions for tree -> null
            i_nulls = []
            for ii in range(kr1.leftmost(), kr1.idx + 1):
                i_nulls.append(self.transaction_to_idx[ii][None])
                transactions[ii][None] = i_nulls.copy()
            for kr2 in self.get_key_roots(self.t2):
                # Make transactions of null -> tree
                j_nulls = []
                for jj in range(kr2.leftmost(), kr2.idx + 1):
                    j_nulls.append(self.transaction_to_idx[None][jj])
                    transactions[None][jj] = j_nulls.copy()

                # get the diff
                self.find_minimum_transactions(kr1, kr2, transactions)
                if time.time() > self.timeout:
                    self.transactions = None
                    return

        for i in range(0, len(self.t1)):
            for j in range(0, len(self.t2)):
                if self.transactions.get(i, {}).get(j) and len(self.transactions[i][j]) > 0:
                    self.transactions[i][j] = tuple([self.idx_to_transaction[idx] for idx in self.transactions[i][j]])

    def get_node_distance(self, n1, n2):
        """
        Get the cost of:
        * removing a node from the first tree,
        * inserting a node into the second tree,
        * or relabelling a node from the first tree to a node from the second tree.
        """
        if n1 is None and n2 is None:
            return 0
        elif n1 is None:
            return self.ins_cost
        elif n2 is None:
            return self.rem_cost
        # Inserts/Removes are easy. Changes are more complicated and should only be within same node type.
        # Use arbitrarily high-value for nodetype changes to effectively ban.
        elif n1.ntype != n2.ntype:
            return self.nodetype_chg_cost
        # next two functions check if both nodes are the same (criteria varies by nodetype)
        elif n1.ntype in ['Heading', "Paragraph"]:
            if n1.text == n2.text:
                return 0
            else:
                return self.chg_cost
        elif n1.text_hash == n2.text_hash:
            return 0
        # otherwise, same node types and not the same, then change cost
        else:
            return self.chg_cost

    def get_lowest_cost(self, rc, ic, cc):
        min_cost = rc
        index = 0
        if ic < min_cost:
            index = 1
            min_cost = ic
        if cc < min_cost:
            index = 2
        return index

    def find_minimum_transactions(self, kr1, kr2, transactions):
        """Find the minimum transactions to get from the first tree to the second tree."""
        for i in range(kr1.leftmost(), kr1.idx + 1):
            if i == kr1.leftmost():
                i_minus_1 = None
            else:
                i_minus_1 = i - 1
            n1 = self.t1[i]
            for j in range(kr2.leftmost(), kr2.idx + 1):
                if j == kr2.leftmost():
                    j_minus_1 = None
                else:
                    j_minus_1 = j - 1
                n2 = self.t2[j]

                if n1.leftmost() == kr1.leftmost() and n2.leftmost() == kr2.leftmost():
                    rem = transactions[i_minus_1][j]
                    ins = transactions[i][j_minus_1]
                    chg = transactions[i_minus_1][j_minus_1]
                    node_distance = self.get_node_distance(n1, n2)
                    # cost of each transaction
                    transaction = self.get_lowest_cost(len(rem) + self.rem_cost,
                                                       len(ins) + self.ins_cost,
                                                       len(chg) + node_distance)
                    if transaction == 0:
                        # record a remove
                        rc = rem.copy()
                        rc.append(self.transaction_to_idx[i][None])
                        transactions[i][j] = rc
                    elif transaction == 1:
                        # record an insert
                        ic = ins.copy()
                        ic.append(self.transaction_to_idx[None][j])
                        transactions[i][j] = ic
                    else:
                        # If nodes i and j are different, record a change, otherwise there is no transaction
                        transactions[i][j] = chg.copy()
                        if node_distance == 1:
                            transactions[i][j].append(self.transaction_to_idx[i][j])

                    self.transactions[i][j] = transactions[i][j].copy()
                else:
                    # Previous transactions, leading up to a remove, insert or change
                    rem = transactions[i_minus_1][j]
                    ins = transactions[i][j_minus_1]

                    if n1.leftmost() - 1 < kr1.leftmost():
                        k1 = None
                    else:
                        k1 = n1.leftmost() - 1
                    if n2.leftmost() - 1 < kr2.leftmost():
                        k2 = None
                    else:
                        k2 = n2.leftmost() - 1
                    chg = transactions[k1][k2]

                    transaction = self.get_lowest_cost(len(rem) + self.rem_cost,
                                                       len(ins) + self.ins_cost,
                                                       len(chg) + len(self.transactions[i][j]))
                    if transaction == 0:
                        # record a remove
                        rc = rem.copy()
                        rc.append(self.transaction_to_idx[i][None])
                        transactions[i][j] = rc
                    elif transaction == 1:
                        # record an insert
                        ic = ins.copy()
                        ic.append(self.transaction_to_idx[None][j])
                        transactions[i][j] = ic
                    else:
                        # record a change
                        cc = chg.copy()
                        cc.extend(self.transactions[i][j])
                        transactions[i][j] = cc

    def get_corresponding_nodes(self):
        """Explain transactions"""
        transactions = self.transactions[len(self.t1) - 1][len(self.t2) - 1]
        remove = []
        insert = []
        change = []
        for i in range(0, len(transactions)):
            if transactions[i][0] is None:
                ins_node = self.t2[transactions[i][1]]
                insert.append(ins_node)
            elif transactions[i][1] is None:
                rem_node = self.t1[transactions[i][0]]
                remove.append(rem_node)
            else:
                prev_node = self.t1[transactions[i][0]]
                curr_node = self.t2[transactions[i][1]]
                change.append((prev_node, curr_node))
        return {'remove': remove, 'insert': insert, 'change': change}