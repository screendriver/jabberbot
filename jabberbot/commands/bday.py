import jabberbot.locale
from microsofttranslator import Translator

trans_client_id = None
trans_client_sec = None


def run_command(msg, *args):
    """Sends a happy birthday in an random language greeting

You can add a nickname: bday <nick>
    """
    lang_code, country = jabberbot.locale.random()
    greet = 'Happy birthday to you'
    translator = Translator(trans_client_id, trans_client_sec)
    translated = translator.translate(greet, lang_code)
    mtype = 'groupchat'
    if args:
        return mtype, '{} @{} (translated to {})'.format(
            translated,
            ' '.join(args),
            country)
    return mtype, '{} (translated to {})'.format(translated, country)
