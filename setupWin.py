from setuptools import setup

EXE = ['main.py']

DATA_FILES = [('',['img']),('',['sound']),('high_score.txt')]
OPTIONS = {'iconfile':'app.ico',}
setup(

  exe = EXE,
  data_files = DATA_FILES,
  options = {'py2exe': OPTIONS},
  setup_requires = ['py2exe'],

)
