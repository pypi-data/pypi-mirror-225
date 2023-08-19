from setuptools import setup, find_packages

setup(
    name='lyg',
    version='3.8.5',
    packages=find_packages(),
    package_data={
        'lyg': [
            'python3.8/*.so',
            'python3.8/*.pyd',
            'python3.9/*.so',
            'python3.9/*.pyd',
            'python3.10/*.so',
            'python3.10/*.pyd',
            'python3.11/*.so',
            'python3.11/*.pyd'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows"
    ],
)

