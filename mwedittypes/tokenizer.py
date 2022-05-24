import re
import string
from collections import Counter
from mwedittypes.constants import *

#Universal regex for punctuations

class Tokenizer:

    def __init__(self, english_unicode, non_english_unicode, lang='en'):
        self.english_punc_regex = r'[{0}]'.format(re.escape(string.punctuation))
        self.english_unicode = english_unicode
        self.non_english_unicode =  non_english_unicode
        self.lang = lang

    def get_punctuations(self, text):
        #get ellipsis
        ellipsis = re.findall(r'\.{3,}',text)
        text = re.sub(r'\.{3,}','',text)

        #Get other punctuations
        english_punc_regex = re.findall(self.english_punc_regex, text)

        english_unicode_pattern = re.compile(self.english_unicode, re.UNICODE)
        english_unicode_regex = re.findall(english_unicode_pattern, text)

        non_english_unicode_pattern = re.compile(self.non_english_unicode, re.UNICODE)
        non_english_punc_regex = re.findall(non_english_unicode_pattern, text)

        return ellipsis + english_punc_regex +english_unicode_regex + non_english_punc_regex


    def get_whitespace(self, text):
        #Get whitespaces. Detects newlines, return characters as well as spaces as whitespaces.
        whitespace = re.findall(r'[\s]',text)
        return whitespace
    

    def get_words(self, text):
        #This extracts words inclusive of those with hyphens and apostrophes
        if self.lang in NON_WHITESPACE_LANGUAGES:
            word_list = re.findall(r"[\w]", text)

        else:
            # Get words with optionally hyphens and apostrophe:
            # \b - word breaks at start and end of word
            # \w+ - matches 1 or more alphanumeric characters
            # [-']? allows for hyphen/apostrophes within word
            # ((?:...)+) capturing group (extract words) made up of 1+ non-capturing sequences of
            # alphanumeric + hyphen/apostrophe. this allows for many-time-hyphenated words and the non-capturing wrapped
            # in capturing is to only gather the entire word (otherwise capturing groups only capture the last instance)
            word_list = re.findall(r"\b((?:\w+[-']?)+)\b", text)
        return word_list

    def get_sentences(self, text):
        #This regex accounts for ellipsis and splits accordingly
        #Minimum sentence size is three words. So a sentence needs to have atleast 3 words in it
        min_sentence_size = 2
        #Add non-english sentence breaks
        sentences = re.split(SENTENCE_BREAKS_REGEX, text)
        sentences = [ sentence.strip() for sentence in sentences if len(self.get_words(sentence)) >= min_sentence_size]
        return sentences

    def get_paragraphs(self, text):
        if text != '':
            paragraphs = [paragraph.strip() for paragraph in re.split(r'\n{2}', text) if len(self.get_words(paragraph)) > 0]

            return paragraphs
        return []

    def tokenize_and_count(self, text):
        if self.lang in NON_WHITESPACE_LANGUAGES:
            word_key = 'Character'
        else:
            word_key = 'Word'

        return {'Whitespace':len(self.get_whitespace(text)),
                'Punctuation':len(self.get_punctuations(text)),
                word_key: len(self.get_words(text)),
                'Sentence':len(self.get_sentences(text)),
                'Paragraph': len(self.get_paragraphs(text))
                }

    def tokenize_and_get_occurence(self, text):
        whitespaces = self.get_whitespace(text)
        punctuation = self.get_punctuations(text)
        words = self.get_words(text)
        sentences = self.get_sentences(text)
        paragraphs = self.get_paragraphs(text)

        whitespace_occurence = Counter(whitespaces)
        punctuation_occurence = Counter(punctuation)
        words_occurence = Counter(words)
        sentences_occurence = Counter(sentences)
        paragraphs_occurence = Counter(paragraphs)

        if self.lang in NON_WHITESPACE_LANGUAGES:
            word_key = 'Character'
        else:
            word_key = 'Word'
        return {
            'Whitespace':dict(whitespace_occurence),
            'Punctuation':dict(punctuation_occurence),
            word_key:dict(words_occurence),
            'Sentence':dict(sentences_occurence),
            'Paragraph':dict(paragraphs_occurence)
        }