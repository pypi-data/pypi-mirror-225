from setuptools import setup

setup(
    name='phyddle',
	version='0.0.6',
	description='A module for fiddling around with phylogenetic models and deep learning'
	author='Michael Landis, Ammon Thompson',
	author_email='michael.landis@wustl.edu, ammon.thompson@gmail.com',
	packages=['phyddle'],
	install_requires=[
		'dendropy',
		'h5py',
		'keras',
		'matplotlib',
		'numpy',
		'pandas',
		'pypdf',
		'scikit-learn',
		'scipy',
		'tensorflow',
		'tqdm'
	],
    entry_points = {
        'console_scripts': ['phyddle=phyddle.command_line:run'],
    }
)
