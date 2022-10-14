from mwedittypes.node_differ import get_diff_count
from mwedittypes.simple_differ import get_diff as simple_get_diff
from mwedittypes.tree_differ import get_diff


class StructuredEditTypes:

    def __init__(self, prev_wikitext='', curr_wikitext='', lang='en', timeout=False, debug=False):
        self.prev_wikitext = prev_wikitext
        self.curr_wikitext = curr_wikitext
        self.lang = lang
        self.timeout = timeout
        self.debug = debug
        self.tree_diff = None
        self.actions = None

    def get_diff(self):
        self.tree_diff = get_diff(self.prev_wikitext, self.curr_wikitext, lang=self.lang,
                                  timeout=self.timeout, debug=self.debug)
        self.actions = get_diff_count(self.tree_diff, lang=self.lang)
        return self.actions


class SimpleEditTypes:

    def __init__(self, prev_wikitext='', curr_wikitext='', lang='en'):
        self.prev_wikitext = prev_wikitext
        self.curr_wikitext = curr_wikitext
        self.lang = lang
        self.actions = None

    def get_diff(self):
        self.actions = simple_get_diff(self.prev_wikitext, self.curr_wikitext, lang=self.lang)
        return self.actions
