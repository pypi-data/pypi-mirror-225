import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "geeeks",
    version = "0.0.5",
    author = "yashpra1010 (Yash Prajapati)",
    author_email = "yashpra1010@gmail.com",
    description = "A package to make your life easy.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires = ">=3.6"
)