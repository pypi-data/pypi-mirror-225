from distutils.core import setup
with open('README.md', 'r') as f:
    long_description = f.read()
setup(
  name = 'pathnav',
  packages = ['pathnav'],
  version = '1.2.7',
  long_description= long_description,
  long_description_content_type='text/markdown',
  license='Mozilla Public License 2.0',
  description = 'Navigate paths with ease',
  author = 'TitusHM',
  author_email = '',
  url = 'https://github.com/titushm/pathnav',
  download_url = 'https://github.com/titushm/pathnav/archive/refs/heads/main.zip',
  keywords = ['path', 'navigation', 'path edit'],
  install_requires=[],
  classifiers=[
	'Development Status :: 4 - Beta',
	'Intended Audience :: Developers',
	'Topic :: Software Development :: Build Tools',
	'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7',
	'Programming Language :: Python :: 3.8',
	'Programming Language :: Python :: 3.9',
	'Programming Language :: Python :: 3.10',
	'Programming Language :: Python :: 3.11'
  ],
)