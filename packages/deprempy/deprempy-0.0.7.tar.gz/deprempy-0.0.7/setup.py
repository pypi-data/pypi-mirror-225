from setuptools import setup, find_packages

setup(
    name="deprempy",
    version="0.0.7",
    description="Kandilli Rasathanesi aracılığı ile elde edilen deprem sinyallerini kullanarak depremleri gösteren bir Python kütüphanesidir.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gihtub.com/Meinos10/deprempy",
    author="Emre",
    author_email="E.tmen2023@gmail.com",
    license="MIT",
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    keywords=["deprempy","deprempython", "deprem", "deprem-python", "deprem-py"],
    packages=find_packages(),
    requires=["requests", "beautifulsoup4"]
)