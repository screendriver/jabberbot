import jabberbot.locale
from microsofttranslator import Translator

trans_client_id = None
trans_client_sec = None


def run_command(msg, *args):
    """Displays a 'enjoy your meal' message in a random language"""
    lang_code, country = jabberbot.locale.random()
    meal = 'Enjoy your meal'
    translator = Translator(trans_client_id, trans_client_sec)
    translated = translator.translate(meal, lang_code)
    meal = '{} (translated to {})'.format(translated, country)
    return 'groupchat', meal
