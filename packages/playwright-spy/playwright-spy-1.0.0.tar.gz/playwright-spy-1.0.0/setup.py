from pathlib import Path

import setuptools

version = Path("VERSION").read_text().strip()
long_description = Path("README.md").read_text()

setuptools.setup(
    name="playwright-spy",
    version=version,
    author="dsppman",
    author_email="dsppman@gmail.com",
    description="A plugin for playwright to prevent detection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dsppman/playwright-spy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=[
        "playwright>=1.15",
    ]
)