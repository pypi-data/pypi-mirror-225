from setuptools import setup, find_packages

setup(
    name="kiam_astro",
    version="3.3.2",
    url="https://github.com/shmaxg/KIAMToolbox",
    author="Maksim Shirobokov",
    author_email="shmaxg@gmail.com",
    description='KIAM Astrodynamics Toolbox',
    long_description='Astrodynamics toolbox for fundamental research and education.',
    keywords=['astrodynamics', 'spacecraft', 'mission analysis'],
    python_requires='>=3.9.0, <=3.9.17',
    packages=find_packages(),
    package_data={'kiam_astro': ['D:\\YandexDisk\\Python\\KIAMToolbox\\kiam_astro\\*']},
    include_package_data=True,
    install_requires=[
        "jdcal>=1.4.1",
        "networkx>=2.6.3",
        "numpy>=1.21.2",
        "scipy>=1.7.3",
        "plotly>=5.11.0",
        "kaleido>=0.2.1",
        "pillow>=9.4.0"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Natural Language :: Russian",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Fortran",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ]
)
