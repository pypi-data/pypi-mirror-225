from setuptools import setup, find_packages

setup(
    name="emlabpkg",
    version="1.3",
    author="Sushant Padhye",
    author_email="padhyesm@mail.uc.edu",
    packages=find_packages(),
    install_requires=["qcodes"],
)
