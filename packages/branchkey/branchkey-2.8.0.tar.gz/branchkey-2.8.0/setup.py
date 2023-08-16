import setuptools
import os

current_directory = os.path.dirname(os.path.abspath(__file__))


try:
    with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except Exception:
    long_description = ""

setuptools.setup(
    name="branchkey",
    version="2.8.0",
    author="BranchKey",
    author_email="info@branchkey.com",
    description="Client application to interface with the BranchKey system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://branchkey.com",
    project_urls={
        "Homepage": "https://branchkey.com",
        "Repository": "https://gitlab.com/branchkey/client_application",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["requests", "numpy",
                      "pika", "responses", "pysocks"],
)
