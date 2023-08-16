import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-ec2-spot-simple",
    "version": "2.1.0",
    "description": "CDK construct library to create EC2 Spot Instances simply.",
    "license": "Apache-2.0",
    "url": "https://github.com/tksst/cdk-ec2-spot-simple/",
    "long_description_content_type": "text/markdown",
    "author": "Takashi Sato<takashi@tks.st>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/tksst/cdk-ec2-spot-simple.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_ec2_spot_simple",
        "cdk_ec2_spot_simple._jsii"
    ],
    "package_data": {
        "cdk_ec2_spot_simple._jsii": [
            "cdk-ec2-spot-simple@2.1.0.jsii.tgz"
        ],
        "cdk_ec2_spot_simple": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.24.0, <3.0.0",
        "constructs>=10.0.9, <11.0.0",
        "jsii>=1.87.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
