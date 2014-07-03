import itertools
import unittest
from pathlib import Path

import pep8


class TestPep8(unittest.TestCase):
    def test_pep8(self):
        """Test that we conform to PEP8."""
        test_dir = Path(__file__).parent
        test_files = (str(f.absolute()) for f in test_dir.glob('*.py'))
        bot_dir = test_dir / '..' / 'jabberbot'
        pack_files = (str(f.absolute()) for f in bot_dir.glob('*.py'))
        files = itertools.chain(test_files, pack_files)
        style = pep8.StyleGuide()
        result = style.check_files(files)
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

if __name__ == '__main__':
    unittest.main()
