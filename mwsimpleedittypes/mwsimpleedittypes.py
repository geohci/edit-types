from mwsimpleedittypes.differ import get_diff

class EditTypes:

    def __init__(self, prev_wikitext='', curr_wikitext='', lang='en', timeout=5):
        self.prev_wikitext = prev_wikitext
        self.curr_wikitext = curr_wikitext
        self.lang = lang
        self.timeout = timeout
        self.actions = None

    def get_diff(self):
        self.actions = get_diff(self.prev_wikitext, self.curr_wikitext, lang=self.lang, timeout=self.timeout)
        return self.actions