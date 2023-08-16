from setuptools import setup, find_packages
with open('./README.md', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='liangutil',
    classifiers=[
        # 属于什么类型
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Natural Language :: Chinese (Simplified)"
    ],

    version='0.1.10',
    description='Encapsulate some common tool methods',
    author='LiAng',
    author_email='l2545721422@163.com',
    long_description=long_description,
    #README.md文本的格式，如果希望使用markdown语言就需要下面这句话
    long_description_content_type="text/markdown",

    requires=['datetime', 'os', 're', 'traceback', 'pytz', 'platform',
                 'random', 'time', 'requests', 'selenium', 'pymysql', 'redis',
                 'json', 'minio', 'wget', 'tarfile', 'zipfile', 'rarfile',
                 'zipfile', 'gzip', 'shutil', 'urllib','confluent_kafka'],
    packages=find_packages(),
    keywords=['python', 'utils', 'windows', 'mac', 'linux'],

    license="apache 3.0"
)