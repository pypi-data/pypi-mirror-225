from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A simpler version of GCP API"
LONG_DESCRIPTION = "A simpler version to get the most of Google Cloud Platform API"

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="gcp_duppla",
    version=VERSION,
    author="Fernando Cortés",
    author_email="<fcortes@pucp.edu.pe>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=["python", "gcp", "bigquery", "gcs", "pandas"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
