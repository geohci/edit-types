import re
import string
#Universal regex for punctuations

class Tokenizer:

    def __init__(self, english_unicode, non_english_unicode):
        self.english_punc_regex = r'[{0}]'.format(re.escape(string.punctuation))
        self.english_unicode = english_unicode
        self.non_english_unicode =  non_english_unicode

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
        whitespace = re.findall(r'[\n\r\s]+',text)
        return whitespace
    

    def get_words(self, text):
        word_list = re.findall(r'\w+',text)
        return word_list

    def get_sentences(self, text):
        sentences = re.split(r'[!?]+|(?<!\.)\.(?!(?<=\d.)\d)(?!\.)', text)
        sentences = sentences[:-1]
        return sentences

    def tokenize_and_count(self, text):
        return {'whitespace_count':len(self.get_whitespace(text)),
                'punctuation_count':len(self.get_punctuations(text)),
                'word_count': len(self.get_words(text)),
                'sentence_count':len(self.get_sentences(text))
                }

