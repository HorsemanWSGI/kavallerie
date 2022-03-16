import os
from setuptools import setup, find_packages


version = "0.1.dev0"

install_requires = [
    'horseman',
    'http-session >= 0.2',
    'reiter.events',
    'roughrider.routing',
    'roughrider.predicate',
    'frozendict',
    'frozen_box',
    'transaction',
]

test_requires = [
    'WebTest',
    'pytest',
    'smtpdfix',
    'sqlalchemy.orm',
    'zope.sqlalchemy',
]


setup(
    name='kavallerie',
    version=version,
    author='Novareto GmbH',
    author_email='contact@example.com',
    url='http://www.example.com',
    download_url='',
    description='Uvcreha WebSite',
    long_description=(open("README.rst").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.rst")).read()),
    license='ZPL',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
    ],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    setup_requires=[],
    tests_require=test_requires,
    extras_require={
        'test': test_requires,
    }
)
