from setuptools import setup
# pypi-AgEIcHlwaS5vcmcCJGQyOWMzMjg2LTMzODgtNDBlYi05ZDViLTk1NTUyZDNkYjhmNwACKlszLCJiMDZjMWMxMi02NGM4LTRhN2UtYjE3YS0xZWQxZjVkZDcwYmEiXQAABiBi9W-GyUaYoCLbDC56j7WaljoroJ-6gPAcYwerdZ6GoA
readme = open('./README.md', 'r')

setup(
    name='error-simplesqlite',
    packages=['simplesqlite'],
    version='0.0.1',
    description='Simplesqlite is a sqlite3 based python library that provides a simple interface to communicate with a sqlite database',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author_email='carlos.bramila98@gmail.com',
    author='Carlos Brayan',
    url='https://github.com/carterror/simplesqlite',
    download_url='https://github.com/carterror/simplesqlite/tarbal/0.0.1',
    keywords=['db', 'sqlite'],
    classifiers=[],
    license='Creative Commons',
    include_package_data=True

)