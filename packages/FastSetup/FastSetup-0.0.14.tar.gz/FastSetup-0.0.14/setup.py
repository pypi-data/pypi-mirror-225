from setuptools import setup, find_packages
 

classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: MIT License',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='FastSetup',
  version='0.0.14',
  description='Static code in python scripts',
  long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Tareq Abeda',
  author_email='TareqAbeda@outlook.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='FastSetup', 
  packages=find_packages(),
  install_requires=[''] 
)
