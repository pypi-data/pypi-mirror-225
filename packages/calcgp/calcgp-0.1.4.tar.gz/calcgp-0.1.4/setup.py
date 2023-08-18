import os
from setuptools import setup, find_packages

folder = os.path.dirname(__file__)

req_path = os.path.join(folder, "requirements.txt")
install_requires = []
if os.path.exists(req_path):
  with open(req_path) as fp:
    install_requires = [line.strip() for line in fp]

readme_path = os.path.join(folder, "README.md")
readme_contents = ""
if os.path.exists(readme_path):
  with open(readme_path) as fp:
    readme_contents = fp.read().strip()

setup(
    name="calcgp",
    version="0.1.4",
    description="Gaussian Process Regression framework for numerical integration and differentiation",
    author="Lukas Einramhof",
    author_email="lukas.einramhof@gmail.com",
    url="https://github.com/LukasEin/calcgp.git",
    long_description=readme_contents,
    long_description_content_type="text/markdown",
    license="MIT License",
    packages=find_packages(),
    package_data={},
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    extras_require={'testing': ['pytest>=5.0']},
    requires_python=">=3.8",
)