from setuptools import find_packages, setup
import pathlib

# 若Discription.md中有中文 須加上 encoding="utf-8"
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
HERE = pathlib.Path(__file__).parent.resolve()
requirements = (HERE / "requirements.txt").read_text(encoding="utf8")
EX_INSTALL_REQUIRES = {s.strip().split('==')[0]: s.strip().split('==')[1] if len(s.strip().split('==')) > 1 else ""
                       for s in requirements.split("\n")}
INSTALL_REQUIRES = [s.strip() for s in requirements.split("\n")]
setup(
    name="shaku-database",
    version="1.1.12",
    author="hawktorng",
    author_email="hawktorng@shaku.com.tw",
    description="Shaku Database util",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hawktorng1/test_shaku",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
    extras_require=EX_INSTALL_REQUIRES
)
