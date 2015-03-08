import os
import random
from microsofttranslator import Translator

trans_client_id = None
trans_client_sec = None


def run_command(msg, *args):
    """Displays a 'enjoy your meal' message in a random language"""
    rand_lang = random_lang()
    meal = 'Enjoy your meal'
    translator = Translator(trans_client_id, trans_client_sec)
    translated = translator.translate(meal, rand_lang[0])
    meal = '{} (translated to {})'.format(translated, rand_lang[1])
    return 'groupchat', meal


def random_lang():
    dirpath = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dirpath, 'lang_codes.txt')
    with open(filepath) as f:
        lines = [tuple(line.strip().split(';')) for line in f]
        langs = dict(lines)
    lang_code = random.choice(list(langs))
    country = langs[lang_code]
    return lang_code, country
