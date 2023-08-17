import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='S_Taper',
	version="0.8.1.6",
	author="Nikita_Khalitov",
	author_email="nik1020031.nik@gmail.com",
	description="Simple write-read add-on to SQLite3",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/TheYoungEngineers/SulfTaper",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.10",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	# Требуемая версия Python.
	python_requires='>=3.8'
)
