from setuptools import setup, find_packages

setup(
	author='Danil',
	author_email='radcenkodanil48@gmail.com',
	url='https://github.com/ProDanil3546/Neural-lib.git',
	license='GNU General Public License v3.0, see LICENSE file',
    name='SimpleNeuro',
    version='1.0.0',
    packages=['SimpleNeuro'],
    # указать зависимости, если они есть
    install_requires=[
        'numpy==1.25.2',
    ],
)
