import setuptools
 
setuptools.setup(
    name="searchdatamodels",
    version="0.0.5",
    author="James Baker",
    author_email="james@talentium.io", 
    license="MIT",
    install_requires=[
          'wandb', 'numpy', 'strsimpy', 'scipy', 'sentence-transformers',
      ],
    # classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)