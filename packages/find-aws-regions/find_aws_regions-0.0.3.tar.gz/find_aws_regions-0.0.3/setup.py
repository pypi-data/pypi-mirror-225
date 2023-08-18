import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="find_aws_regions",
    version="0.0.3",
    author="Jason Underhill",
    author_email="jason@junderhill.com",
    description="Find the closest/best AWS region from your code bassed on latency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/junderhill/py-find-aws-region",
    package_dir = {'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires='>=3.6',
    install_requires=[
        'boto3',
        'requests>=2.31.0',
    ],
)
