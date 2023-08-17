from setuptools import setup, find_packages
 
setup(
    name = "py_lava_api",
    version = "1.1.0",
    keywords = ("lava", ),
    description = "Simple work with lava",
    long_description = "Simple work with lava",
    license = "MIT Licence",
 
    url = "https://github.com/DephPhascow/py_lava_api",
    author = "dphascow",
    author_email = "d.sinisterpsychologist@gmail.com",
 
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests"]
)