import setuptools

with open('./README.md', 'r', encoding = 'utf-8') as f:
    longDescription = f.read()

setuptools.setup(
    name = 'CheeseType',
    version = '0.0.3',
    author = 'Cheese Unknown',
    author_email = 'cheese@cheese.ren',
    description = '存放了一些常用自定义类型的库。',
    long_description = longDescription,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/CheeseUnknown/CheeseType',
    license = 'MIT',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11'
    ],
    keywords = 'type',
    python_requires = '>=3.11',
    install_requires = [],
    packages = setuptools.find_packages()
)
