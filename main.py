import operator
import easyocr

class Sentence:
    __list_article = ["der", "die", "das", "den", "dem", "des"]

    __dict_article_nom = {"maskulin": "der", "neutral": "das", "feminin": "die", "plural": "die"}
    __dict_article_akk = {"maskulin": "den", "neutral": "das", "feminin": "die", "plural": "die"}
    __dict_article_dat = {"maskulin": "dem", "neutral": "dem", "feminin": "der", "plural": "den"}
    __dict_article_gen = {"maskulin": "des", "neutral": "des", "feminin": "der", "plural": "der"}

    __list_signs = [",", "."]

    def __init__(self, sentence: str):
        self.__sentence = sentence
        self.__splitted_sentence = [Sentence.__remove_sign(i) for i in self.__sentence.split(" ")]

    @staticmethod
    def __remove_sign(word):
        str_1 = ""
        j = 0
        for i in range(len(word)):
            if word[-1] in Sentence.__list_signs:
                str_1 = word[0:(len(word) - 1)]
                word = str_1
                j += 1

            elif j == 0:
                str_1 = word

            elif word[-1] not in Sentence.__list_signs:
                break
        return str_1

    def __find_article(self):
        no = operator.countOf(self.__splitted_sentence, "der") +\
                  operator.countOf(self.__splitted_sentence, "die") +\
                  operator.countOf(self.__splitted_sentence, "das") +\
                  operator.countOf(self.__splitted_sentence, "den") +\
                  operator.countOf(self.__splitted_sentence, "dem") +\
                  operator.countOf(self.__splitted_sentence, "des")

        gen_article_normal = ([i, operator.countOf(self.__splitted_sentence, i), operator.indexOf(self.__splitted_sentence, i)]
                       for i in self.__list_article if operator.countOf(self.__splitted_sentence, i) == 1)

        if no == 0:        # Ich bin Artin
            return "No article"

        elif no == 1:        # Ich habe das Buch / Ich kenne ein Mann, der viel Zeit hat.
            for i in gen_article_normal:
                return i

        elif no > 1:         # Ich kenne der Mann, der viel Zeit hat.
            splitted_copy = self.__splitted_sentence.copy()
            list_article = []

            for i in range(len(self.__splitted_sentence)):
                if self.__splitted_sentence[i] in self.__list_article:
                    list_article.append([self.__splitted_sentence[i], operator.indexOf(splitted_copy, self.__splitted_sentence[i])])
                    splitted_copy[i] = None

            return list_article

    def show(self):
        print(self.__find_article())

class OCR:
    def __init__(self, image_address, language="en"):
        self.__image_address = image_address
        self.__language = language

    @property
    def image_address(self):
        return self.__image_address

    @property
    def language(self):
        return self.__language

    def __read(self):
        reader = easyocr.Reader([self.language])
        self.__result = reader.readtext(self.__image_address)

    def show(self):
        print(self.__result)


# s1 = Sentence("Ich habe das die die Buch")
# s1.show()

o1 = OCR('image.jpg')
o1.show()

"""
try to make the list_no > 1 to give me the full info if i had 3 die or ... .

"""


