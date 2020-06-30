import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StravaAnalysis",
    packages=["StravaAnalysis"],
    version="0.1.4",
    license="MIT",
    description="Fully automates the collection of Strava data via their API and neatly structures this inside json "
                "files per activity.",
    author="JerBouma",
    author_email="jer.bouma@gmail.com",
    url="https://github.com/JerBouma/StravaAnalysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["strava", "analysis", "api"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
)