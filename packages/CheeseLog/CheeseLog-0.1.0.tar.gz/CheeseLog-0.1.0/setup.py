import setuptools

with open('./README.md', 'r', encoding = 'utf-8') as f:
    longDescription = f.read()

setuptools.setup(
    name = 'CheeseLog',
    version = '0.1.0',
    author = 'Cheese Unknown',
    author_email = 'cheese@cheese.ren',
    description = '日志系统。可在控制台输出一定格式的、可选颜色的内容，并支持写入指定的日志文件。',
    long_description = longDescription,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/CheeseUnknown/CheeseLog',
    license = 'MIT',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11'
    ],
    keywords = 'log',
    python_requires = '>=3.11',
    install_requires = [],
    packages = setuptools.find_packages()
)
