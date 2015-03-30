import os
import re


def run_command(msg, *args):
    """Returns the available chickentag menu

    You can ask for a single meal: !chickentag H12"""
    chicken = [
        'H1 - Hühnerfleisch Chop-Suey (mit versch. Gemüse)',
        'H2 - Knusprig gebackenes Hühnerbrustfilet (mit Gemüse, süß-sauer)',
        'H3 - Hühnerbrust in Erdnusssauce (mit versch. Gemüse)',
        ('H4 - Gung Pao - Hühnerbrustfilet (in Hoisin Sauce mit Gemüse und '
         'Cashew Nüssen, scharf )'),
        ('H5 - Hühnerbrust nach Kanton-Art (pikant gewürzt mit Gemüse '
         '(scharf))'),
        ('H6 - Hühnerbrust in Thai Rot Curry (mit Kokosmilch, Chili und '
         'Thai-Basilikum, scharf)'),
        ('H7 - gebratenes Hühnerbrustfilet nach Thai Art (mit versch. Gemüse '
         'und Thai-Basilikum (scharf))'),
        ('H8 - gebratenes Hühnerbrustfilet (mit Zitronengras und '
         'Limettenblätter, scharf)'),
        'H9 - Hühner Sate Spiesse (mit hausgem. Sauerkraut)',
        'H10 - gebratenes Hühnerbrustfilet (mit Zwiebeln)',
        'H11 - knusprige Hähnchen (mit Gemüse und Knoblauch)',
        ('H12 - knuspriges Hähnchen (mit versch. Gemüse und Thai-Basilikum, '
         'scharf)'),
        'H13 - Knuspriges Hähnchen (mit Erdnusssauce)',
        'H14 - Knuspriges Hähnchen (mit Thai Curry Sauce, scharf)',
        ('H15 - Knuspriges Hähnchen nach Thai-Art (mit versch. Gemüse, '
         'Thai-Basilikum in Hoisin Sauce, scharf)'),
        'H16 - Knuspriges Hähnchen (mit Gemüse)',
        ('H17 - Hühnerbrustfilet in Kokosmilch (mit versch. Gemüse, '
         'Curry-Sauce)'),
        'H18 - Knuspriges Hähnchen (mit Gemüse, Kokomilch, Curry-Sauce)']
    if args:
        try:
            index = int(re.findall(r"\d+", args[0])[0]) - 1
            return 'groupchat', chicken[index]
        except:
            pass
    return 'groupchat', os.linesep.join(chicken)
