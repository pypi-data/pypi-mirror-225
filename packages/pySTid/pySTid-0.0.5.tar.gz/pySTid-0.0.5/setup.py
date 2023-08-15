from setuptools import setup

long_description = open('README.rst').read()

setup(name="pySTid",
      version="0.0.5",
      author="Sensor Access",
      description="Python wrapper for using access the STid credential issuing server",
      long_description_content_type='text/markdown',
      long_description=long_description,
      maintainer_email="admin@sensoraccess.co.uk",
      install_requires=[''],
      packages=['pySTid'],
      license_files=('LICENSE.txt',),
      data_files=[('', ['pySTid/stidmobile-id-com-chain.pem'])],
      include_package_data=True,
      zip_safe=False)

