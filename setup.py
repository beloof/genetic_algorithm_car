from setuptools import setup, find_packages

setup(
    name="genetic_algorithm_car",  # Name of the package
    version="1.0.0",  # Initial version
    author="Lassioued Badis",
    description="A simulation of cars learning to drive using genetic algorithms.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/beloof/genetic_algorithm_car",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pygame",
        "numpy",
        "matplotlib"
    ],
)
