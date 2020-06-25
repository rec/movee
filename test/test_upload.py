from scripta import upload
from pathlib import Path
from unittest import TestCase
from unittest import mock
import tdir

FILE = Path('test.cast')


@tdir.tdec(str(FILE))
class TestUpload(TestCase):
    def test_read(self):
        with mock.patch('scripta.upload._call') as mp:
            mp.side_effect = [['', 'https://f.a'], ['https://f.b']]
            url, create = upload.upload(FILE)
            assert create
            assert url == 'https://f.a'

            url, create = upload.upload(FILE)
            assert not create
            assert url == 'https://f.a'

            FILE.write_text('changed')

            url, create = upload.upload(FILE)
            assert create
            assert url == 'https://f.b'

    def test_error(self):
        with mock.patch('scripta.upload._call') as mp:
            mp.side_effect = [['ERROR']]
            with self.assertRaises(ValueError) as m:
                upload.upload(FILE)
            assert m.exception.args[0].startswith('Failed to upload')
