import unittest
from text_statistics import TextStatistics

# Mr. Headless Nick flipped his head back onto his eck,
# coughed, and said, "So - new Gryffindors! I hope you're going
# to help us win the house championship this year?"
text1 = TextStatistics("text_files/test1.txt")

# "How did he get covered in blood?" asked Seamus with great interest.
text2 = TextStatistics("text_files/test2.txt")

# Pam, pom, 666000, pam...
text3 = TextStatistics("text_files/test3.txt")

# Book, rice, rice, book, rice, pam pam pom pom 7777...
text4 = TextStatistics("text_files/test4.txt")

class MyTestCase(unittest.TestCase):
    def test_on_sentences_amount(self):
        RESULTS = 2, 1
        results = text1.sentences_amount(), text2.sentences_amount()
        self.assertEqual(results[0], RESULTS[0])
        self.assertEqual(results[1], RESULTS[1])

    def test_on_declarative_sentences_amount(self):
        RESULTS = 0, 1
        results = text1.declarative_sentences_amount(), text2.declarative_sentences_amount()
        self.assertEqual(results[0], RESULTS[0])
        self.assertEqual(results[1], RESULTS[1])

    def test_on_sentences_average_length(self):
        RESULT = 3, 9
        result = text3.sentences_average_length()
        self.assertEqual(RESULT[0], result[0])
        self.assertEqual(RESULT[1], result[1])

    def test_on_words_average_length(self):
        RESULT = 3
        result = text3.words_average_length()
        self.assertEqual(result, RESULT)

    def test_on_top_k_n_grams(self):
        RESULT = [('book', 'rice'), ('rice', 'rice'), ('rice', 'book')]
        result = text4.top_k_n_grams(3, 2)
        self.assertEqual(result, RESULT)

if __name__ == '__main__':
    unittest.main()
