from setuptools import setup,find_packages
from pathlib import Path

setup(
	name = 'hugo-paulo-project',
	version = 1.0,
	description = 'Este pacote ira fornecer ferramentas de processamento de video',
	long_description = Path('README.md').read_text(),
	author = 'Hugo',
	author_email = 'hugo@gmail.com',
	keywords = ['camera','video','processamento'],
	packages = find_packages()
	)