from setuptools import setup

APP = ['main.py']

DATA_FILES = [('',['img']),('',['sound']),('high_score.txt'),('manual.txt')]
OPTIONS = {'iconfile':'app.icns',}
setup(

  app = APP,
  data_files = DATA_FILES,
  options = {'py2app': OPTIONS},
  setup_requires = ['py2app'],

)
