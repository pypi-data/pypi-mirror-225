from pathlib import Path
from setuptools import setup, find_packages

long_description = Path("README.md").read_text()
reqs = Path("requirements.txt").read_text().strip().splitlines()

pkg = "time_in"
setup(
    name=pkg,
    version="0.1.1",
    url="https://github.com/seanbreckenridge/time-in",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description=("""CLI tool to figure out the time somewhere else"""),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(include=[pkg]),
    install_requires=reqs,
    package_data={pkg: ["py.typed"]},
    zip_safe=False,
    keywords="",
    python_requires=">=3.9",
    entry_points={"console_scripts": ["time-in = time_in.__main__:main"]},
    extras_require={
        "testing": [
            "mypy",
            "flake8",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
