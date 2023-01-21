from distutils.core import setup

from setuptools import find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(name='iMail',  # 包名
      version='1.0.0',  # 版本号
      description='iMail is a simple and useful email notification script.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Zhiwei Li',
      author_email='lizhw.cs@outlook.com',
      url='https://github.com/mtics',
      install_requires=['Pillow'],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Topic :: Communications :: Email',
          'Operating System :: OS Independent'
      ],
      )
