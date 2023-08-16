import os

from setuptools import find_packages, setup

base_path = os.path.abspath(os.path.dirname(__file__))

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

readme = ""
with open("README.md") as f:
    readme = f.read()

setup(
    name="UnlimitedGPT",
    author="Sxvxge",
    url="https://github.com/Sxvxgee/UnlimitedGPT",
    project_urls={
        "Documentation": "https://github.com/Sxvxgee/UnlimitedGPT/blob/main/README.md",
        "Issue tracker": "https://github.com/Sxvxgee/UnlimitedGPT/issues",
        "Changelog": "https://github.com/Sxvxgee/UnlimitedGPT/blob/main/CHANGELOG.md",
    },
    version="0.1.9.3",
    packages=["UnlimitedGPT", "UnlimitedGPT/internal"],
    # py_modules=["UnlimitedGPT"],
    license="GPL-3.0 license",
    description="An unofficial Python wrapper for OpenAI's ChatGPT API",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
