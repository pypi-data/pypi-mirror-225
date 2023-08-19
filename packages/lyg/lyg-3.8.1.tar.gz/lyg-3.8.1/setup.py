from setuptools import setup, find_packages

setup(
    name='lyg',
    version='3.8.1',  # 递增的版本号
    packages=find_packages(),
    package_data={
        'lyg': ['*.so', '*.pyd']
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows"
    ],
)

