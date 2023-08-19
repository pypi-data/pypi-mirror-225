from setuptools import setup, find_packages

setup(
    name="fumetest-cli",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "selenium",
        "python-dateutil",
    ],
    entry_points={
        'console_scripts': [
            'fumetest=fumetest_cli:cli',  # 'fumetest' is the command name users will type in the console
        ],
    },
)
