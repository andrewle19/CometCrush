from setuptools import setup

APP = ['main.py']

DATA_FILES = [('',['img']),('',['sound']),('high_score.txt')]
OPTIONS = {'iconfile':'app.ico',}
setup(

  app = APP,
  data_files = DATA_FILES,
  options = {'py2exe': OPTIONS},
  setup_requires = ['py2exe'],

)
