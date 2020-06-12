import os
from unittest import skipIf

IS_TRAVIS = os.getenv('TRAVIS', '').lower().startswith('t')
skip_if_travis = skipIf(IS_TRAVIS, 'Test does not work in travis')
