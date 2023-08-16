import setuptools

setuptools.setup(name='aespark', version='0.2.0',  # 202308161015
                 description='Generate a QR code that can adapt to the cylinder',
                 long_description=open(
                     'README.md', 'r', encoding='utf-8').read(),
                 author='wtianxin',
                 author_email='1007582510@qq.com',
                 url='https://pypi.org/project/aespark/',
                 license='MIT',  # 与之前你选用的许可证类型有关系
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 include_package_data=True,
                 install_requires=[
                     'jieba>=0.42.1',
                     'tqdm>=4.64.1',
                     'jionlp>=1.5.2',
                     'python-docx>=0.8.11',
                     'openpyxl>=3.1.2',
                 ],
                 keywords='aespark',
                 classifiers=[
                     "Natural Language :: Chinese (Simplified)",
                     "Development Status :: 3 - Alpha",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python",
                     "Programming Language :: Python :: 3.4",
                     "Programming Language :: Python :: 3.5",
                     "Programming Language :: Python :: 3.6",
                     "Programming Language :: Python :: 3.7",
                     "License :: OSI Approved :: MIT License",
                     "Topic :: Utilities"
                 ],
                 )
