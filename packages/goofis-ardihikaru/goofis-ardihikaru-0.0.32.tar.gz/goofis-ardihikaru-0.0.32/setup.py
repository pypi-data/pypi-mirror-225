import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="goofis-ardihikaru",
    version="0.0.32",
    license='MIT',
    author="Muhammad Febrian Ardiansyah",
    author_email="mfardiansyah@outlook.com",
    description="Modules to extract information from Google Finance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/goofis-ardihikaru/0.0.1/#files",
    install_requires=[  # package dependency
        'ujson==5.8.0',
        'requests==2.31.0',
        'parsel==1.8.1',
        'fake-useragent==1.2.1',
        'simplejson==3.19.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platforms='any',
    keywords='asyncio',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8"
)
