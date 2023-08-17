from setuptools import find_packages, setup

with open("README.md", "r",encoding="utf8") as f:
	long_description = f.read()

setup(
	name = "RSensePy",
	version = "0.0.2",
	description = "Biophysical parameter calculator for Landsat 8 data",
	package_dir ={"":"app"},
	packages = find_packages(where="app"),
	long_description=long_description,
	long_description_content_type="text/markdown",
	url = "https://github.com/richiedlon/SoftwareDevProject",
	author = "richiedlon/opeyami",
	license="MIT",
	cliassifiers=[
		"License :: MIT License",
		"Programming Language :: Python :: 3.9"
	],

	install_requires = ["rasterio>=1.3.0","matplotlib>=3.7.0","shapely>=2.0.0","Fiona>=1.9.4.post1","geopandas>=0.13.0"],
	extras_requires={
		"dev":["pytest>=7.0",
		"twine>=4.0.2", 
		"sphinx>=4.2.0",
		"myst-parser",
		"sphinx_rtd_theme"],
	},
	python_requires=">=3.9.16",


	)