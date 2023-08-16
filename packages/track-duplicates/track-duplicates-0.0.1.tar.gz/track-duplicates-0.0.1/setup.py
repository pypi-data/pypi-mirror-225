from setuptools import setup
import versioneer

requirements = [
    "pandas>=1.4.2",
    "tqdm>=4.64.1",
    "pysam>=0.17.0",
    "numpy>=1.21.2",
    "biopython>=1.79",
    "pyarrow>=12.0.1",
]

setup(
    setup_requires=[
        # Setuptools 18.0 properly handles Cython extensions.
        "setuptools>=39.1.0",
        "Cython>=0.29.24",
    ],
    name="track-duplicates",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A simple tool to extract reads from a certain taxa from BAM files",
    license="MIT",
    author="Antonio Fernandez-Guerra",
    author_email="antonio@metagenomics.eu",
    url="https://github.com/genomewalker/track-duplicates",
    packages=["track_duplicates"],
    entry_points={"console_scripts": ["trackDups=track_duplicates.__main__:main"]},
    install_requires=requirements,
    keywords="track-duplicates,GTDB",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
