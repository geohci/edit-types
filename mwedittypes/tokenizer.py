import regex
from mwtokenizer.tokenizer import Tokenizer as MWTokenizer


class Tokenizer:
    def __init__(self, lang="en"):
        self.lang = lang
        self.tokenizer = MWTokenizer(language_code=lang)

    def get_punctuations(self, text):
        """Get all punctuation characters.

        Not used directly but left in as an available method.
        Note: this is broader than the Punctuation category characters per Unicode
        and also includes e.g., math symbols.
        See: https://en.wikipedia.org/wiki/Unicode_character_property#General_Category

        This won't exactly match what you get from tokenize_and_get_occurrence which will
        include punctuation that is a part of words (hyphens, abbreviations, etc.) in the word category.
        """
        return regex.findall(r"[^\w\s]", text)

    def get_whitespace(self, text):
        """Get all whitespace characters.

        Not used directly but left in as an available method.
        """
        return regex.findall(r"[\s]", text)

    def get_words(self, text):
        """Get all words.

        Not used directly but left in as an available method.
        This is not fully exclusive of get_whitespace and get_punctuation. Words
        will never include whitespace but can include internal punctuation like
        hyphens and terminating punctuation if the word is an abbreviation.
        """
        word_list = []
        for tok in self.tokenizer.word_tokenize(text, use_abbreviation=True):
            if regex.search(r"\w", tok):
                word_list.append(tok)
        return word_list

    def get_sentences(self, text):
        """Get all sentences.

        Not used directly but left in as an available method.
        """
        min_sentence_size = 5
        sentences = [
            s.strip()
            for s in self.tokenizer.sentence_tokenize(text, use_abbreviation=True)
            if len(s.strip()) >= min_sentence_size
        ]
        return sentences

    def get_paragraphs(self, text):
        """Get all paragraphs.

        Not used directly but left in as an available method.
        """
        paragraphs = [
            p.strip()
            for p in regex.split(r"\n{2}", text)
            if len(p.strip()) > 5  # basic character minimum for paragraphs
        ]
        return paragraphs

    def tokenize_and_get_occurrence(self, text):
        paragraphs = {}
        sentences = {}
        words = {}
        punctuation = {}
        whitespaces = {}
        for i, para in enumerate(regex.split(r"\n{2}", text)):
            if (
                i != 0
            ):  # we know there are paragraph breaks for total paragraphs - 1 so skip the first one
                whitespaces["\n"] = whitespaces.get("\n", 0) + 2
            sentences_found = False
            for sent in self.tokenizer.sentence_tokenize(para, use_abbreviation=True):
                num_words = 0
                for tok in self.tokenizer.word_tokenize(sent, use_abbreviation=True):
                    if tok.strip():
                        if regex.search(r"\w", tok):
                            words[tok] = words.get(tok, 0) + 1
                            num_words += 1
                        else:
                            for p in tok:
                                punctuation[p] = punctuation.get(p, 0) + 1
                    else:
                        for w in tok:
                            whitespaces[w] = whitespaces.get(w, 0) + 1
                if num_words >= 2:
                    sent = sent.strip()
                    sentences[sent] = sentences.get(sent, 0) + 1
                    sentences_found = True
            if sentences_found:
                para = para.strip()
                paragraphs[para] = paragraphs.get(para, 0) + 1

        return {
            "Whitespace": whitespaces,
            "Punctuation": punctuation,
            "Word": words,
            "Sentence": sentences,
            "Paragraph": paragraphs,
        }


def parse_change_text(prev_wikitext="", curr_wikitext="", lang="en", summarize=True, tokenizer=None):
    # Initialize tokenizer class
    if tokenizer is None:
        tokenizer = Tokenizer(lang=lang)

    prev_tokenizer = tokenizer.tokenize_and_get_occurrence(prev_wikitext)
    curr_tokenizer = tokenizer.tokenize_and_get_occurrence(curr_wikitext)

    result = {}
    for text_category in curr_tokenizer.keys():
        items_diff_list = list(
            set(curr_tokenizer[text_category].items())
            ^ set(prev_tokenizer[text_category].items())
        )
        for item in items_diff_list:
            diff = curr_tokenizer[text_category].get(item[0], 0) - prev_tokenizer[
                text_category
            ].get(item[0], 0)
            result[text_category] = dict(
                result.get(text_category, {}), **{item[0]: diff}
            )

        # Get the maximum value between the sum of positives and sum of negatives
        if summarize and len(result.get(text_category, {})) > 0:
            removals = sum(
                abs(item) for item in result[text_category].values() if item < 0
            )
            additions = sum(
                abs(item) for item in result[text_category].values() if item > 0
            )
            change = min(removals, additions)
            result[text_category] = {}
            removals -= change
            additions -= change

            if removals > 0:
                result[text_category]["remove"] = removals

            if additions > 0:
                result[text_category]["insert"] = additions

            if change > 0:
                result[text_category]["change"] = change
    return result
