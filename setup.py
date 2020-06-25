import scripta

_classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3.8',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]

with open('requirements.txt') as f:
    REQUIRED = f.read().splitlines()

if __name__ == '__main__':
    from setuptools import setup

    setup(
        name='scripta',
        version=scripta.__version__,
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/scripta',
        tests_require=['pytest'],
        py_modules=['scripta'],
        description='Script asciinema movies',
        long_description=open('README.rst').read(),
        license='MIT',
        classifiers=_classifiers,
        keywords=['documentation'],
        scripts=['scripts/scripta'],
        packages=['scripta'],
        install_requires=REQUIRED,
    )
