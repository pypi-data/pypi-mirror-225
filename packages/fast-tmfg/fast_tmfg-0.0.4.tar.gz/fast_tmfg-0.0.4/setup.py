import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="fast_tmfg",
    version="0.0.4",
    author="Antonio Briola",
    author_email="anto.briola96@gmail.com",
    description="The official package to compute the Triangulated Maximally Filtered Graph (TMFG).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FinancialComputingUCL/Triangulated_Maximally_Filtered_Graph",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=["numpy", "pandas", "networkx"],
    packages=["fast_tmfg"],
    )
