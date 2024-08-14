"""
=================================================
Grammatical Analysis of German Sentences using AI
=================================================

Description:
This project aims to analyze the grammatical structure of German sentences using artificial intelligence (AI).
The process involves multiple steps to ensure accurate results.

Author:
Artin Faghanzadeh

Contact:
+98 920 929 0024 (Telegram)

Version:
0.0.12

Date:
2024-08-07

License:
This project is licensed under the MIT License - see the LICENSE file for details.
"""
from colorama import init, Fore, Style
import operator
import requests
import string
import collections
import pandas as pd

def print_logo():
    init(autoreset=True)
    print(Fore.LIGHTBLUE_EX + " _    _ __  __ ______     ____  ______  ____")
    print(Fore.LIGHTBLUE_EX + "| |  | |  \/  |  ____|   / / | |  __  | | \x5c \x5c")
    print(Fore.LIGHTBLUE_EX + "| |__| | \  / | |__     /_/| | | |  | | | |\x5c_\x5c")
    print(Fore.LIGHTCYAN_EX + "|  __  | |\/| | |__|       | | | |  | | | |")
    print(Fore.LIGHTCYAN_EX + "| |  | | |  | | |          | | | |__| | | |")
    print(Fore.LIGHTCYAN_EX + "|_|  |_|_|  |_|_|          |_| |______| |_|")
    print(Fore.LIGHTMAGENTA_EX + "                                 ")
    print(Fore.LIGHTMAGENTA_EX + "        Powered by Artin Faghanzadeh")
    print(Style.RESET_ALL)  # Reset to default


# =============================
class SentenceManual:
    __list_article = ["der", "die", "das", "den", "dem", "des"]

    __dict_article_nom = {"maskulin": "der", "neutral": "das", "feminin": "die", "plural": "die"}
    __dict_article_akk = {"maskulin": "den", "neutral": "das", "feminin": "die", "plural": "die"}
    __dict_article_dat = {"maskulin": "dem", "neutral": "dem", "feminin": "der", "plural": "den"}
    __dict_article_gen = {"maskulin": "des", "neutral": "des", "feminin": "der", "plural": "der"}

    __list_signs = [",", "."]

    __dict_personal_noun = {"ich": "1. Person, Singular", "du": "2. Person, Singular",
                                "er": "3. Person, Singular, Maskulin", "sie": "3. Person, Singular, Feminin",
                                "es": "3. Person, Singular, Neutral", "wir": "1. Person, Plural",
                                "ihr": "2. Person, Plural", "Sie": "3. Person, Plural"}
    __list_personal_noun = ["ich", "du", "er", "sie", "es", "wir", "ihr"]
    __list_personal_noun_not_sie = ["ich", "du", "er", "es", "wir", "ihr"]


    def __init__(self, sentence: str, verb_excel: str):
        self.__sentence = sentence
        self.__verb_excel = verb_excel
        self.__splitted_sentence = [SentenceManual.__remove_sign(i) for i in self.__sentence.split(" ")]

    @staticmethod
    def __remove_sign(word):
        str_1 = ""
        j = 0
        for i in range(len(word)):
            if word[-1] in SentenceManual.__list_signs:
                str_1 = word[0:(len(word) - 1)]
                word = str_1
                j += 1

            elif j == 0:
                str_1 = word

            elif word[-1] not in SentenceManual.__list_signs:
                break
        return str_1

    @staticmethod
    def __lower(word: str):
        list_temp = []
        for i in word:
            if 90 >= ord(i) >= 65:
                list_temp.append(chr(ord(i) + 32))

            else:
                list_temp.append(i)

        return "".join(list_temp)

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

    def __find_noun(self):
        list_noun = []
        list_sentences_personal_noun = []
        dict_defined_personal_noun = collections.defaultdict(object)
        dict_defined_personal_noun_sie = collections.defaultdict(object)

        for i in range(len(self.__splitted_sentence)):
            if (self.__splitted_sentence[i] != SentenceManual.__lower(self.__splitted_sentence[i]) and
                    SentenceManual.__lower(self.__splitted_sentence[i]) not in self.__list_personal_noun):

                list_noun.append(self.__splitted_sentence[i])

            if SentenceManual.__lower(self.__splitted_sentence[i]) in self.__list_personal_noun:
                list_sentences_personal_noun.append(self.__splitted_sentence[i])

        if len(list_sentences_personal_noun) > 0:
            for i in list_sentences_personal_noun:
                if self.__lower(i) in self.__list_personal_noun_not_sie:
                    dict_defined_personal_noun[i] = self.__dict_personal_noun[self.__lower(i)]

                if self.__lower(i) == "sie":        # sie: plural, singular (by verb)
                    ...

        return f"{list_noun}\t\t{list_sentences_personal_noun}\t\t{dict_defined_personal_noun}"

    def __find_verb(self):
        verb_name = (i for i in pd.read_excel(self.__verb_excel, usecols=[0]).iloc[:, 0])

        def read_column(file_path: str, column_number: int):
            counter_row_1 = 0
            df = pd.read_excel(file_path, usecols=[column_number])

            for value in df.iloc[:, 0]:
                yield [value, counter_row_1]
                counter_row_1 += 1

        def modal_check(list_a, person: str):
            match person:
                case "1. Person, Singular":
                    for value in read_column(self.__verb_excel, 1):
                        if SentenceManual.__lower(list_a[0]) == value[0]:
                            return [next(verb_name), SentenceManual.__lower(list_a[0]), "1. Person, Singular"]

                        next(verb_name)

                        if value[1] == "mögen kii":
                            return False

                case "2. Person, Singular":
                    for value in read_column(self.__verb_excel, 2):
                        if SentenceManual.__lower(list_a[0]) == value[0]:
                            return [next(verb_name), SentenceManual.__lower(list_a[0]), "2. Person, Singular"]

                        next(verb_name)

                        if value[1] == "mögen kii":
                            return False

                case "3. Person, Singular, Maskulin":
                    for value in read_column(self.__verb_excel, 3):
                        if SentenceManual.__lower(list_a[0]) == value[0]:
                            return [next(verb_name), SentenceManual.__lower(list_a[0]), "3. Person, Singular, Maskulin"]

                        next(verb_name)

                        if value[1] == "mögen kii":
                            return False
                case "3. Person, Singular, Feminin":
                    for value in read_column(self.__verb_excel, 3):
                        if SentenceManual.__lower(list_a[0]) == value[0]:
                            return [next(verb_name), SentenceManual.__lower(list_a[0]), "3. Person, Singular, Feminin"]

                        next(verb_name)

                        if value[1] == "mögen kii":
                            return False
                case "3. Person, Singular, Neutral":
                    for value in read_column(self.__verb_excel, 3):
                        if SentenceManual.__lower(list_a[0]) == value[0]:
                            return [next(verb_name), SentenceManual.__lower(list_a[0]), "3. Person, Singular, Neutral"]

                        next(verb_name)

                        if value[1] == "mögen kii":
                            return False

                case "1. Person, Plural":
                    for value in read_column(self.__verb_excel, 4):
                        if SentenceManual.__lower(list_a[0]) == value[0]:
                            return [next(verb_name), SentenceManual.__lower(list_a[0]), "1. Person, Plural"]

                        next(verb_name)

                        if value[1] == "mögen kii":
                            return False

                case "2. Person, Plural":
                    for value in read_column(self.__verb_excel, 5):
                        if SentenceManual.__lower(list_a[0]) == value[0]:
                            return [next(verb_name), SentenceManual.__lower(list_a[0]), "2. Person, Plural"]

                        next(verb_name)

                        if value[1] == "mögen kii":
                            return False

                case "3. Person, Plural":
                    for value in read_column(self.__verb_excel, 6):
                        if SentenceManual.__lower(list_a[0]) == value[0]:
                            return [next(verb_name), SentenceManual.__lower(list_a[0]), "3. Person, Plural"]

                        next(verb_name)

                        if value[1] == "mögen kii":
                            return False

        list_verb_possibility = [self.__splitted_sentence[0], self.__splitted_sentence[1], self.__splitted_sentence[-1]]
        person = str

        for i in list_verb_possibility:
            if i == self.__splitted_sentence[0]:
                if i in list(self.__dict_personal_noun.keys()):
                    person = self.__dict_personal_noun[i]
                    list_verb_possibility.remove(i)
                    continue

                elif SentenceManual.__lower(i) in list(self.__dict_personal_noun.keys()):
                    person = self.__dict_personal_noun[SentenceManual.__lower(i)]
                    list_verb_possibility.remove(i)
                    continue

            elif i != self.__splitted_sentence[0]:
                if i in list(self.__dict_personal_noun.keys()):
                    person = self.__dict_personal_noun[i]
                    list_verb_possibility.remove(i)
                    continue

                elif 65 <= ord(i[0]) <= 90 and i != self.__splitted_sentence[0]:
                    list_verb_possibility.remove(i)

        if modal_check(list_verb_possibility, person) != None:
            """
            print the other verb
            """
            return modal_check(list_verb_possibility, person)

        else:
            ...

    def show(self):
        print(self.__find_verb())

class SentenceMuChat:
    def __init__(self, mu_chat_url: str, authorization_api_token: str, prompt):
        self.__mu_chat_url = mu_chat_url
        self.__authorization_api_token = authorization_api_token
        self.__prompt = prompt
        self.__response = None

    def __posting(self):
        url = self.__mu_chat_url
        payload = {
            "query": self.__prompt,
            "temperature": 0.0,
            "modelName": "gpt_3_5_turbo",
        }

        headers = {
            "Authorization": f"Bearer {self.__authorization_api_token}",
            "Content-Type": "application/json"
        }

        self.__response = requests.request("POST", url, json=payload, headers=headers)

    @staticmethod
    def response_checking(response):
        response_number = str(response).split(" ")[1].split(">")[0].split("[")[1].split("]")[0]

        if int(response_number) == 200:
            return SentenceMuChat.text_extraction(response.text)

        else:
            return int(response_number)

    @staticmethod
    def text_extraction(text):
        list_1 = []
        temp = text.split("{")[1]
        temp_1 = temp[11:len(text.split("{")[1]) - 12]
        for i in temp_1.split("\\n"):
            list_1.append(i.split(":")[0][1:len(i.split(":")[0]) - 1])
            list_1.append(i.split(":")[1][1:len(i.split(":")[1]) - 1])

        list_letters = string.ascii_letters
        for i in range(len(list_1)):
            while list_1[i][0] not in list_letters:
                list_1[i] = list_1[i][1: len(list_1[i])]

            while list_1[i][-1] not in list_letters:
                list_1[i] = list_1[i][0: len(list_1[i]) - 1]

        return list_1

    def result_showing(self):
        SentenceMuChat.__posting(self)
        return SentenceMuChat.response_checking(self.__response)
# Mu-Chat AI
# print_logo()
# s1 = SentenceMuChat("https://app.mu.chat/api/agents/clzk1jkth005viq0jty1y8kqp/query",
#                     "Secure_API",
#                     "Sentence")       # like "Ich halte sehr viel von dem Projekt."
# print(s1.result_showing())
# OUTPUT: ['Ich', 'Nomen, 1. Person, Singular', 'halte', 'Verben, 1. Person, Singular, Präsens, Nominativ', 'sehr', 'Adverb', 'viel', 'Adjektiv', 'von', 'Präposition', 'dem', 'bestimmter Artikel, maskulin, Dativ', 'Projekt', 'Nomen, neutra']

class SentenceDatabase:
    ...

s1 = SentenceManual("machst du das zukaufen.", "Verb.xlsx")
s1.show()
