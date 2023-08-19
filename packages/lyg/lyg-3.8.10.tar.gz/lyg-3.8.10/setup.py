from setuptools import setup, find_packages

setup(
    name='lyg',
    version='3.8.10',
    packages=find_packages(),
    package_data={
        'lyg': [
            '*.so',
            '*.pyd'
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
    # 如果需要的话，也可以添加其他元数据
    author="LYG.AI",
    author_email="team@lyg.ai",
    url="https://lyg.ai",  # 可以修改为你的库的实际URL
)

