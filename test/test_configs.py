from scripta import configs
from unittest import TestCase
import tdir

CFGS = {
    'c1.yml': '{columns: 100, upload: true}',
    'c2.yml': '{verbose: True}',
}
SCRIPTS = ['c1.yml', 's.py', 'c2.yml', '{scripts: [s.sh]}']


@tdir.tdec('s.py', 's.sh', 's.junk', CFGS)
class ConfigsTest(TestCase):
    def test_configs(self):
        for scripts in (SCRIPTS, {'scripts': SCRIPTS}):
            actual = configs.to_config(scripts)
            expected = {
                'columns': 100,
                'scripts': ['s.py', 's.sh'],
                'upload': True,
                'verbose': True,
            }
            assert actual == expected

    def test_errors(self):
        with self.assertRaises(ValueError) as m:
            configs.to_config(SCRIPTS + ['dont_exist.py'])
        assert m.exception.args[0] == 'Cannot find dont_exist.py'

        with self.assertRaises(ValueError) as m:
            configs.to_config(SCRIPTS + ['s.junk'])
        assert m.exception.args[0] == 'Unknown suffixes: s.junk'

        with self.assertRaises(ValueError) as m:
            configs.to_config(SCRIPTS + ['}{'])
        expected = """\
Cannot load:
<argument 4: }{>: while parsing a block node
expected the node content, but found '}'
  in "<unicode string>", line 1, column 1:
    }{
    ^"""
        assert m.exception.args[0] == expected
