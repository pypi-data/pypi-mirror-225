"""Module for setting up system and respective brik configurations"""


def env():
	from jinja2 import Environment, PackageLoader

	return Environment(loader=PackageLoader("brik.config"))
