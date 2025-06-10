from setuptools import setup, find_packages

setup(
    name="gsscoder_python",  # your package name
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,  # important to include files listed in MANIFEST.in
    install_requires=[
        "pandas",
        "pyreadr",
        # add other dependencies your package needs
    ],
    author="Sebastian Heslin-Rees",
    author_email="Sebastian.Heslin-Rees@london.gov.uk",
    description="Python implementation to recode GSS codes",
    url="https://github.com/yourusername/gsscoder_python", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)