from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="manic-xai",
    version='1.0.79',
    author="Craig Pirie",
    author_email="c.pirie11@rgu.ac.uk",
    description="Genetic Algorithm for Generating Metacounterfactual Explanations",
    url = "https://github.com/craigybaeb/MANIC",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['manic'],
    install_requires=[
        "matplotlib>=3.4.3",
        "numpy>=1.21.2",
        "scikit-learn>=0.24.2",
        "seaborn>=0.11.2"],
    keywords=['manic', 'metacounterfactual', 'counterfactual', 'xai', 'explanation', 'aggregation', 'disagreement', 'agreement'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
