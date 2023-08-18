from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='MultiValueSplitter',
  version='0.0.1',
  description='column_splitter_filler',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  # No URL provided
  author='ashish_jaimon',
  author_email='ashishjaimon98@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='', 
  packages=find_packages(),
)