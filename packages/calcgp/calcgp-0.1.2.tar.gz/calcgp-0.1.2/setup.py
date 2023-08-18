import setuptools

setuptools.setup(
    name="calcgp",
    version="0.1.2",
    author="Lukas Einramhof",
    author_email="lukas.einramhof@gmail.com",
    description=
    "Gaussian Process Regression framework for numerical integration and differentiation",
    url="https://github.com/LukasEin/calcgp.git",
    download_url="https://github.com/LukasEin/calcgp/archive/refs/tags/v_01.tar.gz",
    # packages=setuptools.find_packages("./calcgp"),
    packages=["calcgp"],
    install_requires=[
        'jax', 'jaxopt'
    ],
    extras_require={'testing': ['pytest>=5.0']},
    python_requires='>=3.7'
    )