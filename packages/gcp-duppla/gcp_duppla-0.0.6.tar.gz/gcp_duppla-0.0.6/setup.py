from setuptools import setup, find_packages

VERSION = "0.0.6"
DESCRIPTION = "A simpler version of GCP API"
LONG_DESCRIPTION = "A simpler version to get the most of Google Cloud Platform API, using prebuild functions to get data from BigQuery and Google Cloud Storage."

setup(
    name="gcp_duppla",
    version=VERSION,
    author="Fernando Cortés",
    author_email="<fcortes@pucp.edu.pe>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "gcp", "bigquery", "gcs", "pandas"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ],
)
