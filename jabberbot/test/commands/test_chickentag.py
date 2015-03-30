import os
import unittest
from jabberbot.commands import chickentag


class TestChickentagCommand(unittest.TestCase):
    def setUp(self):
        self.menus = [
            'H1 - Hühnerfleisch Chop-Suey (mit versch. Gemüse)',
            ('H2 - Knusprig gebackenes Hühnerbrustfilet (mit Gemüse, '
             'süß-sauer)'),
            'H3 - Hühnerbrust in Erdnusssauce (mit versch. Gemüse)',
            ('H4 - Gung Pao - Hühnerbrustfilet (in Hoisin Sauce mit Gemüse '
             'und Cashew Nüssen, scharf )'),
            ('H5 - Hühnerbrust nach Kanton-Art (pikant gewürzt mit Gemüse '
             '(scharf))'),
            ('H6 - Hühnerbrust in Thai Rot Curry (mit Kokosmilch, Chili und '
             'Thai-Basilikum, scharf)'),
            ('H7 - gebratenes Hühnerbrustfilet nach Thai Art (mit versch. '
             'Gemüse und Thai-Basilikum (scharf))'),
            ('H8 - gebratenes Hühnerbrustfilet (mit Zitronengras und '
             'Limettenblätter, scharf)'),
            'H9 - Hühner Sate Spiesse (mit hausgem. Sauerkraut)',
            'H10 - gebratenes Hühnerbrustfilet (mit Zwiebeln)',
            'H11 - knusprige Hähnchen (mit Gemüse und Knoblauch)',
            ('H12 - knuspriges Hähnchen (mit versch. Gemüse und '
             'Thai-Basilikum, scharf)'),
            'H13 - Knuspriges Hähnchen (mit Erdnusssauce)',
            'H14 - Knuspriges Hähnchen (mit Thai Curry Sauce, scharf)',
            ('H15 - Knuspriges Hähnchen nach Thai-Art (mit versch. Gemüse, '
             'Thai-Basilikum in Hoisin Sauce, scharf)'),
            'H16 - Knuspriges Hähnchen (mit Gemüse)',
            ('H17 - Hühnerbrustfilet in Kokosmilch (mit versch. Gemüse, '
             'Curry-Sauce)'),
            'H18 - Knuspriges Hähnchen (mit Gemüse, Kokomilch, Curry-Sauce)']

    def test_run_command_without_menu(self):
        mtype, resp = chickentag.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, os.linesep.join(self.menus))

    def test_run_command_with_menu(self):
        mtype, resp = chickentag.run_command(None, 'H13')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'H13 - Knuspriges Hähnchen (mit Erdnusssauce)')

    def test_run_command_with_wrong_menu(self):
        mtype, resp = chickentag.run_command(None, 'foo')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, os.linesep.join(self.menus))
