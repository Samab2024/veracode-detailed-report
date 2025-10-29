from setuptools import setup, find_packages

setup(
    name="veracode-xml",
    version="1.0.0",
    description="Unified CLI for Veracode XML API tasks like fetching detailed reports.",
    author="Soumik Roy",
    packages=find_packages(),
    install_requires=[
        "requests",
        "veracode-api-signing",
    ],
    entry_points={
        "console_scripts": [
            "veracode-xml=veracode_xml.cli:main",
        ],
    },
    python_requires=">=3.8",
)
