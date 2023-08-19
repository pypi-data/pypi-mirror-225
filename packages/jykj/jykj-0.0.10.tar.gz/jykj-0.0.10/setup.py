import setuptools

setuptools.setup(
    name="jykj",
    version="0.0.10",
    author="jykj",
    author_email="renshuai@jylink.com",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy", "scipy", "filterpy", "requests"
    ],
    python_requires=">=3",
)
