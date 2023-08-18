from setuptools import setup

setup(
    name="anyscan",
    version="1.0.0",
    description="A minimal, yet complete, python API for any block explorer powered by the Etherscan team. (e.g. etherscan.io, arbiscan.io, polygonscan.com, ...",
    url="https://github.com/gerrrg/anyscan",
    author="gerrrg",
    license="MIT",
    packages=[
        "explorer",
        "explorer.configs",
        "explorer.enums",
        "explorer.modules",
        "explorer.utils",
    ],
    install_requires=["requests"],
    include_package_data=True,
    zip_safe=False,
)
