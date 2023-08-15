import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='io-components',                           # should match the package folder
    packages=['io-components'],                     # should match the package folder
    version='0.0.1',                                # important for updates
    license='MIT',                                  # should match your chosen license
    description='Testing installation of Package',
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Nicolas Pichon',
    author_email='pichon.nicolas1@gmail.com',
    url='https://github.com/eatcala/io-components', 
    project_urls = {                                # Optional
        "Bug Tracker": "https://github.com/eatcala/io-components/issues"
    },
    install_requires=['requests'],                  # list all packages that your package uses
    keywords=["pypi", "io-components"],             #descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    
    download_url="https://github.com/eatcala/io-components/archive/refs/tags/0.0.1.tar.gz",
)
