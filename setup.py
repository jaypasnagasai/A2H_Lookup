from setuptools import setup, find_packages

setup(
    name="pclookup",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas"],
    entry_points={
        "console_scripts": [
            "biolookup=biolookup.run:main",
        ]
    },
)
