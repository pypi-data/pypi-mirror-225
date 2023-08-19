from setuptools import setup, find_packages

setup(
    name="emlabpkg",
    version="3.1",
    summary="Univeristy of Cincinnati, Physics Department, Dr. Mikheev's Lab Package. Contains driver for NF-ZM2376 and edited version of sweep",
    author="Sushant Padhye",
    author_email="padhyesm@mail.uc.edu",
    packages=find_packages(),
    install_requires=["qcodes"],
)