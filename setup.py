from setuptools import setup, find_packages
import os

try:
    from setuptest import test
except ImportError:
    from setuptools.command.test import test

version = __import__('admin_history').__version__

def read(fname):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-admin-history",
    version = version,
    url = 'http://github.com/writepython/django-admin-history',
    license = 'BSD',
    platforms=['OS Independent'],
    description = "A plugable admin app that shows admin history in the admin.",
    long_description = read('README.txt'),
    author = 'Ryan McCormack',
    author_email = 'writepython@gmail.com',
    packages=find_packages(),
    install_requires = (
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    cmdclass={'test': test},
    test_suite='setuptest.setuptest.SetupTestSuite',
    tests_require=(
        'django-setuptest>=0.1.1',
        'argparse',  # apparently needed by django-setuptest on python 2.6
    ),
)
