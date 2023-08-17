import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GEMAP", # Replace with your own username
    version="0.0.30",
    author="Krishan Gupta, Kaifu Chen",
    author_email="krishan57gupta@gmail.com",
    description="Regression-Based Approaches to Predict Cellular Metabolomic Profiles from Transcriptomic Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krishan57gupta/GEMAP",
    packages=setuptools.find_packages(),
    install_requires=[],
    package_data={
        'GEMAP': ['data/*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.6',
)
