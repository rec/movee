from . import test_config
from pathlib import Path
from scripta import scripta
from scripta.times import DEFAULT_TIMES
from scripta.times import Times
from scripta.typing_errors import ErrorMaker
from unittest import TestCase
import tdir

TEST_CASTS = (
    'git-adjust.cast',
    'git-new.cast',
)
CAST_DIR = Path(__file__).parent.parent / 'data/recorded'
CAST_FILES = ','.join(str(CAST_DIR / t) for t in TEST_CASTS)


def _val(*s, **kwargs):
    return scripta.validated_config(s, **kwargs)


@tdir('cast', 's.py', 's.sh', svg={'foo': 'bar'})
class ValidateTest(TestCase):
    def test_empty(self):
        actual = _val('s.py')
        assert actual == EMPTY

    def test_full(self):
        actual = _val(
            's.py',
            '--cast=kast',
            '--svg',
            '--errors={row: 0.5, column: 0.25, shift: 0.125}',
            '--times=[0.25, 0.5]',
            '--height=40',
            '--width=60',
            '--theme=dracula',
            f'--keys={CAST_FILES}',
        )

        expected = dict(
            EMPTY,
            cast=Path('kast'),
            svg=None,
            errors=ErrorMaker(0.5, 0.25, 0.125),
            times=Times(keystroke_max=0.25, keystroke_scale=0.5),
            height=40,
            width=60,
            theme='dracula',
            keys=CAST_TIMES,
        )

        if actual != expected:
            keys = actual['keys']
            for i in range(0, len(keys), 6):
                print(keys[i : i + 6], '+')
        assert actual == expected

    def test_edge1(self):
        em = ErrorMaker(0.5, 0.25, 0.125)
        actual = _val('s.py', errors=em)
        assert actual['sources'] == [Path('s.py')]
        assert actual == dict(EMPTY, errors=em)

    def test_edge2(self):
        em = ErrorMaker(0.5, 0.25, 0.125)
        actual = _val('s.py', errors='{row: 0.5, column: 0.25, shift: 0.125}')
        assert actual == dict(EMPTY, errors=em)

    def test_edge3(self):
        em = ErrorMaker(0.5, 0.25, 0.125)
        errors = {'row': 0.5, 'column': 0.25, 'shift': 0.125}
        actual = _val('s.py', errors=errors)
        assert actual == dict(EMPTY, errors=em)

    def test_edge4(self):
        actual = _val('s.py', keys='0.125, 0.25')
        assert actual == dict(EMPTY, keys=[0.125, 0.25])

    def test_error1(self):
        with self.assertRaises(ValueError) as m:
            _val('s.py', '--cast=cast', '--svg=svg')
        msg = '--cast: cast exists but is not a directory'
        assert m.exception.args[0] == msg

    def test_error2(self):
        with self.assertRaises(ValueError) as m:
            _val('s.py', '--errors=wombat')
        msg = 'Did not understand --errors=wombat'
        assert m.exception.args[0] == msg

    def test_error3(self):
        with self.assertRaises(ValueError) as m:
            _val('s.py', '-wfrog')
        msg = '--width takes a numeric argument'
        assert m.exception.args[0] == msg

    def test_error4(self):
        with self.assertRaises(ValueError) as m:
            _val('s.py', '--width=-4')
        msg = 'width must be non-negative'
        assert m.exception.args[0] == msg

    def test_error5(self):
        with self.assertRaises(ValueError) as m:
            _val('s.py', '--theme=oops')
        msg = 'Unknown asciinema theme "oops"'
        assert m.exception.args[0] == msg

    def test_error6(self):
        with self.assertRaises(ValueError) as m:
            _val('s.py', '--keys=oops')
        msg = 'Cannot open file: oops'
        assert m.exception.args[0] == msg

    def test_error7(self):
        with self.assertRaises(ValueError) as m:
            _val('s.py', '--keys=[frog, 2]')
        msg = "Do not understand --keys=['frog', 2]"
        assert m.exception.args[0] == msg

    def test_error8(self):
        with self.assertRaises(ValueError) as m:
            _val('s.py', '--keys=[-2, 2]')
        msg = 'Times must all be positive'
        assert m.exception.args[0] == msg

    def test_error9(self):
        with self.assertRaises(ValueError) as m:
            _val('s.py', keys=range(3))
        msg = 'Do not understand --keys=range(0, 3)'
        assert m.exception.args[0] == msg

    def test_errors(self):
        with self.assertRaises(ValueError) as m:
            _val('s.py', '--keys=oops', '--theme=oops')
        msgs = (
            'keys: Cannot open file: oops\n',
            'theme: Unknown asciinema theme "oops"\n',
        )
        assert m.exception.args == msgs


EMPTY = {
    'errors': ErrorMaker(),
    'height': 0,
    'keys': DEFAULT_TIMES,
    'sources': [Path('s.py')],
    'svg': '',
    'times': Times(),
    'upload': False,
    'verbose': False,
    'width': 0,
}

EMPTY = dict(test_config.EMPTY, **EMPTY)

CAST_TIMES = (
    [0.216651, 0.103281, 0.112404, 0.176665, 0.071936, 0.159863]
    + [0.071946, 0.184407, 0.104091, 0.159072, 0.224978, 0.327647]
    + [0.320951, 0.590714, 0.167993, 0.08019, 0.09861, 0.10951]
    + [0.064346, 0.209382, 0.127448, 0.287592, 0.047234, 0.15993]
    + [0.384483, 0.175331, 0.049915, 0.13645, 0.295683, 0.224675]
    + [0.294919, 1.311568, 0.152082, 0.079611, 0.031942, 0.160039]
    + [0.111917, 0.105129, 0.046969, 0.112043, 0.104859, 0.063408]
    + [0.521513, 0.318589, 0.130067, 0.175492, 0.671009, 0.720869]
    + [0.192975, 0.103656, 0.071348, 0.177079, 0.096632, 0.158702]
    + [2.409039, 2.505049, 0.552014, 0.113301, 0.063011, 0.880361]
    + [0.361001, 0.006971, 0.527535, 0.272698, 0.224039, 0.377035]
    + [1.222674, 0.174766, 0.072263, 0.082268, 0.126736, 0.046715]
    + [0.185112, 0.134974, 0.199987, 0.055927, 0.112692, 0.15266]
    + [0.232544, 0.087741, 0.256009, 0.262898, 0.184035, 0.064209]
    + [0.065504, 0.399982, 0.094893, 0.103926, 0.065951, 0.094017]
    + [0.120932, 0.056286, 0.095438, 0.175722, 0.256131, 0.088106]
    + [0.280533, 0.463416, 0.230709, 0.048459, 0.129254, 0.166791]
    + [0.090083, 0.277678, 0.160283, 0.232837, 0.20731, 0.583874]
    + [0.184536, 0.464224, 0.008078, 0.424248, 0.393825, 0.238557]
    + [0.527304, 0.199935, 0.081218, 0.094779, 0.13603, 0.113675]
    + [0.167917, 0.15112, 0.488342, 0.079417, 0.081903, 0.078143]
    + [0.360658, 0.319363, 0.897751, 0.152925, 0.167456, 0.319897]
    + [0.271519, 0.312159, 0.407615, 0.185548, 0.103724, 0.112296]
    + [1.032202, 0.087336, 2.46589, 0.382671, 0.112725, 0.263728]
    + [1.208175, 1.184511, 0.089274, 0.192702, 0.238428, 0.689484]
    + [1.399128, 0.176732, 0.119813, 0.126776, 0.488927, 0.367609]
    + [0.111864, 0.201576, 0.775532, 0.087377, 0.224296, 0.223846]
    + [0.128225, 0.065133, 0.431897, 0.385595, 0.069654, 0.176099]
    + [0.216494, 0.287977, 0.368093, 0.249227, 0.077822, 0.104782]
    + [0.119143, 0.080661, 0.256287, 0.10465, 0.113004, 0.230278]
    + [0.080311, 0.159292, 0.224094, 0.263918, 2.840831, 0.224586]
    + [0.104054, 0.111584, 0.224523, 0.087787, 0.072035, 0.112099]
    + [0.128072, 0.119979, 0.127889, 0.648027, 0.055956, 0.104153]
    + [0.743253, 0.240137, 0.079981, 0.104014, 0.182638, 0.121325]
    + [0.079982, 0.144126, 0.407897, 0.103791, 0.056254, 0.192057]
    + [0.112089, 0.087191, 0.097125, 0.079964, 0.112101, 0.128048]
    + [0.055972, 1.150562]
)
