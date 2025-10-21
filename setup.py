from setuptools import setup, find_packages

setup(
    name="veracode-detailed-report",
    version="1.1.0",
    description="Fetch Veracode detailed reports (XML or PDF) using HMAC authentication.",
    author="Soumik Roy",
    packages=find_packages(),
    install_requires=[
        "requests",
        "veracode-api-signing"
    ],
    entry_points={
        "console_scripts": [
            "veracode-report=veracode_report.get_detailed_report:main",
        ],
    },
    python_requires=">=3.8",
)
