from setuptools import setup

setup(
    name = "PyNewDisk", 
    version = "0.0.1",
    author = "William Waterson",
    author_email = "<dank.txt@gmail.com>",
    url = "https://github.com/fora1ds/newdisk",
    packages = ["pynewdisk"],
    description = "A small Linux library for working with disks.",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: C",
        "Programming Language :: Cython",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries"
    ],
    keywords = ["ata", "disk", "sata", "scsi", "smart"],
    license = "MIT"
) 
