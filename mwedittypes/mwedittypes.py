from mwedittypes.tree_differ import get_diff
from mwedittypes.node_differ import get_diff_count


class EditTypes:

    def __init__(self, prev_wikitext='', curr_wikitext='', lang='en', timeout=5):
        self.prev_wikitext = prev_wikitext
        self.curr_wikitext = curr_wikitext
        self.lang = lang
        self.timeout = timeout
        self.tree_diff = None
        self.actions = None

    def get_diff(self):
        self.tree_diff = get_diff(self.prev_wikitext, self.curr_wikitext, lang=self.lang, timeout=self.timeout)
        self.actions = get_diff_count(self.tree_diff)
        return self.actions