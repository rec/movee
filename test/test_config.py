from pathlib import Path
from movee import config
from movee import parse
from unittest import TestCase
import tdir

SOURCES = ['c1.yml', 's.py', 'c2.yml', '{sources: [s.sh]}']


@tdir(
    's.py',
    's.sh',
    's.junk',
    {
        'c1.yml': '{width: 100, upload: true}',
        'c2.yml': '{verbose: True}',
        'c3.yml': '{svg: wombat}',
    },
)
class ConfigTest(TestCase):
    def test_config(self):
        s2 = {'sources': SOURCES[:-1] + ['s.sh']}
        for sources in (SOURCES, s2):
            actual = config.read_config(sources)
            expected = {
                'width': 100,
                'sources': [Path('s.py'), Path('s.sh')],
                'upload': True,
                'verbose': True,
            }
            assert actual == expected

    def test_svg1(self):
        sources = [{'sources': ['s.py'], 'svg': 'ph/'}, {'svg': None}]
        actual = config.read_config(sources)
        expected = {'sources': [Path('s.py')], 'svg': None}
        assert actual == expected

    def test_svg2(self):
        flags = vars(parse.parse('s.py c3.yml --svg=ph/'.split()))
        actual = config.read_config(flags)
        expected = dict(EMPTY, sources=[Path('s.py')], svg='ph/')
        assert actual == expected

    def test_svg3(self):
        flags = vars(parse.parse('s.py c3.yml'.split()))
        actual = config.read_config(flags)
        expected = dict(EMPTY, sources=[Path('s.py')], svg='wombat')
        assert actual == expected

    def test_svg4(self):
        flags = vars(parse.parse('s.py c3.yml --svg'.split()))
        actual = config.read_config(flags)
        expected = dict(EMPTY, sources=[Path('s.py')], svg=None)
        assert actual == expected

    def test_errors1(self):
        with self.assertRaises(ValueError) as m:
            config.read_config(SOURCES + ['dont_exist.py'])
        assert m.exception.args[0] == 'Cannot find dont_exist.py\n'

    def test_errors2(self):
        with self.assertRaises(ValueError) as m:
            config.read_config(SOURCES + ['s.junk'])
        assert m.exception.args[0] == 'Suffix unknown: s.junk\n'

    def test_errors3(self):
        with self.assertRaises(ValueError) as m:
            config.read_config(SOURCES + ['}{'])
        expected = """\
Cannot load:
<argument 4>: while parsing a block node
expected the node content, but found '}'
  in "<unicode string>", line 1, column 1:
    }{
    ^
"""
        assert m.exception.args[0] == expected

    def test_errors4(self):
        with self.assertRaises(ValueError) as m:
            config.read_config({'foo': 'bar'})
        assert m.exception.args[0] == 'No source file given'

    def test_errors5(self):
        with self.assertRaises(ValueError) as m:
            config.read_config({'sources': ['s.py'], 'frog': 'toad'})
        assert m.exception.args[0] == 'Invalid for config: frog\n'

    def test_errors6(self):
        flags = vars(parse.parse('s.py [] --svg=ph/'.split()))

        with self.assertRaises(TypeError) as m:
            config.read_config(flags)
        assert m.exception.args[0] == 'Expected str or dict'

    def test_errors7(self):
        with self.assertRaises(TypeError) as m:
            config.read_config([[]])
        assert m.exception.args[0] == 'Expected str or dict'


EMPTY = {
    'cast': None,
    'dry_run': False,
    'errors': None,
    'height': None,
    'keys': None,
    'prompt': None,
    'sources': None,
    'svg': None,
    'quit_on_error': False,
    'theme': None,
    'times': None,
    'upload': False,
    'verbose': False,
    'width': None,
}
