from setuptools import setup, find_packages

setup(
    name="Dager",
    version="0.7",
    packages=find_packages(),
    author="Idriss Animashaun",
    author_email="idriss.animashaun@intel.com",
    description="Data Acquisition and Generation Engine for Reporting",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iddy-ani/Dager_data",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'anyio==3.7.1',
        'certifi==2023.5.7',
        'dnspython==2.4.0',
        'exceptiongroup==1.1.2',
        'h11==0.14.0',
        'httpcore==0.17.3',
        'idna==3.4',
        'numpy==1.25.1',
        'pandas==2.0.3',
        'pymongo==4.4.1',
        'python-dateutil==2.8.2',
        'pytz==2023.3',
        'six==1.16.0',
        'sniffio==1.3.0',
        'tzdata==2023.3'
    ],
    python_requires='>=3.10',
)
