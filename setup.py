from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
	print("[Error] Please use python --version greater 3")
	exit(1)


setup(
	name="sqlhandle",
	version=open('sqlhandle/version.py').read(),
	description=('Simple sqlhandle for python'),
	url='https://github.com/breath2live/sqlhandle',

	author='Sam Classix',
	author_email='sam.classix@example.com',
	license=open('LICENSE').read(),

	long_description=open('README.md').read(),
	#packages=find_packages(),
	packages=['sqlhandle'],
	include_package_data=True,

	install_requires=['numpy', 'pandas', 'pymysql']
)
