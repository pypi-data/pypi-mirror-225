import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
  long_description = fh.read()

setuptools.setup(
  name="animage-data_sorter",
  version="1.1.6",
  author="zhaomy",
  author_email="zhaomy@an-image.cn",
  description="dicom sort",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://gitee.com/AnImage-Beijing/data_sorter",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)