import setuptools

setuptools.setup(
	name = 'datana',
	version = '0.3.4.7b',
	author = 'MasterLegend',
	description = 'datana pakage',
	long_description = 'Datana is a package for data processing in the field of chemistry. It can be used to process both computational and experimental data.',
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/MasterLegend/datana',
	py_modules = ['datana.atom', 'datana.spectrum', 'datana.figure', 'datana.structure', 'datana.dynamic', 'datana.dos'],
)