from pathlib import Path
from movee import render
from unittest import TestCase
import tdir

CAST_FILE = Path(__file__).parent / 'sample.cast'
SVG_FILE = Path(__file__).parent / 'sample.svg'


@tdir
class TestRender(TestCase):
    def test_render(self):
        render.render_file(CAST_FILE, 'test.svg')
        expected = SVG_FILE.read_text()
        actual = Path('test.svg').read_text()
        assert expected == actual
