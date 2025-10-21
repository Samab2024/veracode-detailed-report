from setuptools import setup, find_packages

setup(
    name="veracode-detailed-report",
    version="1.1.0",
    author="Soumik Roy",
    author_email="",
    description="Fetch Veracode Detailed Reports (XML/PDF) using HMAC authentication.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Samab2024/veracode-detailed-report",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "veracode-api-signing>=22.4.0",
    ],
    entry_points={
        "console_scripts": [
            "veracode-report=veracode_report.get_detailed_report:main",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
