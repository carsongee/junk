from setuptools import setup

setup(
    name='junk',
    version='0.0.0',
    py_modules=['junk'],
    install_requires=[
        'Click',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'junk = junk:cli',
        ]
    },
)
