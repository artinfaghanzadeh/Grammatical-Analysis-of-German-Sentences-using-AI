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
0.0.1

Date:
2024-08-07

License:
This project is licensed under the MIT License - see the LICENSE file for details.
"""
from colorama import init, Fore, Style
import operator
import requests


def print_logo():
    init(autoreset=True)
    print(Fore.LIGHTBLUE_EX + " _    _ __  __ ______ _ ______ _ ")
    print(Fore.LIGHTBLUE_EX + "| |  | |  \/  |  ____| |  __  | |")
    print(Fore.LIGHTBLUE_EX + "| |__| | \  / | |__  | | |  | | |")
    print(Fore.LIGHTCYAN_EX + "|  __  | |\/| | |__| | | |  | | |")
    print(Fore.LIGHTCYAN_EX + "| |  | | |  | | |    | | |__| | |")
    print(Fore.LIGHTCYAN_EX + "|_|  |_|_|  |_|_|    |_|______|_|")
    print(Fore.LIGHTMAGENTA_EX + "                                 ")
    print(Fore.LIGHTMAGENTA_EX + "        Powered by Artin Faghanzadeh")
    print(Style.RESET_ALL)  # Reset to default


class SentenceManual:
    __list_article = ["der", "die", "das", "den", "dem", "des"]

    __dict_article_nom = {"maskulin": "der", "neutral": "das", "feminin": "die", "plural": "die"}
    __dict_article_akk = {"maskulin": "den", "neutral": "das", "feminin": "die", "plural": "die"}
    __dict_article_dat = {"maskulin": "dem", "neutral": "dem", "feminin": "der", "plural": "den"}
    __dict_article_gen = {"maskulin": "des", "neutral": "des", "feminin": "der", "plural": "der"}

    __list_signs = [",", "."]

    def __init__(self, sentence: str):
        self.__sentence = sentence
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

        return list_1

    def result_showing(self):
        SentenceMuChat.__posting(self)
        return SentenceMuChat.response_checking(self.__response)

class SentenceDatabase:
    ...


print_logo()
# s1 = SentenceMuChat("https://app.mu.chat/api/agents/clzk1jkth005viq0jty1y8kqp/query", "token", "prompt")
# print(s1.result_showing())
# ['Ich\\', '"Nomen, 1. Person, Singular\\', '"halte\\', '"Verben, 1. Person, Singular, Präsens, Nominativ\\', '"sehr\\', '"Adverb\\', '"viel\\', '"Adjektiv\\', '"von\\', '"Präposition\\', '"dem\\', '"bestimmter Artikel, maskulin, Dativ\\', '"Projekt\\', '"Nomen, neutra']
