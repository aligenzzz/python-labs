from re import split, match, search, sub
import regular_expressions as rexp
from collections import Counter

class TextStatistics:
    def __init__(self, file_name):
        self._file_name = file_name
        self._validate_()

    def print_file(self):
        with open(self._file_name) as file:
            print(*file)

    def sentences_amount(self):
        sentences = self._split_into_sentences_()
        return len(sentences)

    def declarative_sentences_amount(self):
        sentences = self._split_into_sentences_()
        declarative_sentences = [sentence for sentence in sentences
                                 if sub(r'\s?"?\s?$', r'', sentence).endswith('.')]
        return len(declarative_sentences)

    def non_declarative_sentences_amount(self):
        return self.sentences_amount() - self.declarative_sentences_amount()

    def sentences_average_length(self):
        text = self._read_file_()

        # division of the text into sentences
        sentences = split(rexp.SENTENCE, text)
        # division of the sentences into words
        sentences_words = [split(rexp.WORD, sub(r'[?!.]+$', r'', sentence))
                           for sentence in sentences]
        # check the words for numbers
        sentences_words = [[word for word in words if not word.isdigit()] for words in
                           sentences_words]

        words_average_amount = int(sum(len(words) for words in sentences_words)
                                   / len(sentences_words))
        summation = 0
        for sentence_words in sentences_words:
            summation += sum(len(word) for word in sentence_words)

        return words_average_amount, int(summation / len(sentences))

    def words_average_length(self):
        words = self._split_into_words_()
        return int(sum(len(word) for word in words) / len(words))

    def top_k_n_grams(self, k: int = 10, n: int = 4):
        words = self._split_into_words_()
        ngrams = [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]

        ngram_count = Counter(ngrams)
        return [ngram for ngram, count in ngram_count.most_common(k)]

        # without Counter
        # ngram_count = self._count_n_grams_(ngrams)
        # return sorted(ngram_count.items(), key=lambda x: x[1], reverse=True)

    @staticmethod
    def _count_n_grams_(ngrams):
        ngram_count = {}
        for ngram in ngrams:
            if ngram not in ngram_count:
                ngram_count[ngram] = 1
            else:
                ngram_count[ngram] += 1
        return ngram_count

    def _split_into_words_(self):
        text = self._read_file_()
        words = split(rexp.WORD, text)
        # because regex expression doesn't work in the end of text + word != number
        words = [sub(r'[?.!\s]+$', r'', word.lower()) for word in words if not match(r'\d+', word)]
        return words

    def _split_into_sentences_(self):
        text = self._read_file_()
        sentences = split(rexp.SENTENCE, text)
        # for direct speech
        sentences = [sentence for sentence in sentences if not sentence.replace('"', ' ').isspace()]
        return sentences

    # only latin letters, numbers and separators must be processed
    def _validate_(self):
        text = self._read_file_()
        if search(r'[^A-Za-z-\'\d\s!?,.()":;]', text):
            raise Exception("Invalid input! Check your text one more time!")

    def _read_file_(self):
        with open(self._file_name) as file:
            return file.read()
