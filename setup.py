import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_jinja2',
    'passlib',
    'webhelpers'
    ]

setup(name='prototype_design_suite',
      version='0.0',
      description='prototype_design_suite',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Thomas E. Knickman',
      author_email='tknickman@gmail.com',
      url='www.thomasknickman.com',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='prototype_design_suite',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = prototype_design_suite:main
      [console_scripts]
      initialize_prototype_design_suite_db = prototype_design_suite.scripts.initializedb:main
      """,
      )
