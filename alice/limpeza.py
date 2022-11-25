from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator


class CleanComents:
    def __init__(self, coments):
        self._comments = np.array(list(coments))
        self._punctuation = self.read_punctuation()
        self._portuguese_stops = set(stopwords.words('portuguese'))
        self._list_words = []

    @property
    def coments(self):
        return self._comments

    @property
    def punctuation(self):
        return self._punctuation

    @property
    def portuguese_stops(self):
        return self._portuguese_stops

    @property
    def list_words(self):
        return self._list_words

    def remove_emoji(self, s):
        return ''.join(i for i in s if ord(i) <= 255)

    def lower_case(self, palavra):
        return str.lower(palavra)

    def remove_caracter(self, palavra):
        if palavra.startswith('-'):
            return palavra.replace('-', '')
        return palavra

    def read_punctuation(self):
        return {'.', ',', ';', ':', '!', '´', '`', "'", '...', ')', '(', "''", "``", "´´", '?', '..', '*', '-', '@',
                '%', '$', '#', '&', '/'}

    def clean(self):
        v_remove_emoji = np.vectorize(self.remove_emoji)
        v_lower_case = np.vectorize(self.lower_case)
        v_remove_caracter = np.vectorize(self.remove_caracter)

        comments = v_remove_emoji(self._comments)
        comments = v_lower_case(comments)

        listwords = [
            p for c in comments for p in word_tokenize(c)
        ]

        listwords = [
            p for p in listwords if p not in self.portuguese_stops and p not in self.punctuation
        ]

        listwords = v_remove_caracter(listwords).tolist()

        listwords = [
            p for p in listwords if p not in self.portuguese_stops
        ]

        self._list_words.extend(listwords)

    def counter(self):
        counte = Counter(self._list_words)
        return counte.most_common()

    def corpus(self):
        return ' '.join(self._list_words)

    def word_clound(self):
        alice_colors = np.array(Image.open('alice_colorida.png'))
        image_colors = ImageColorGenerator(alice_colors)
        wc = WordCloud(collocations=False, background_color='white', stopwords=self.portuguese_stops, mask=alice_colors
                       ).generate(self.corpus())

        plt.figure(figsize=(20, 13))
        plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
        plt.axis('off')
        plt.show()
