import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "lambda-error-sns-sender",
    "version": "0.0.50",
    "description": "CDK construct to send Lambda detail errors to AWS SNS Topic.",
    "license": "Apache-2.0",
    "url": "https://github.com/ServerlessLife/lambda-error-sns-sender.git",
    "long_description_content_type": "text/markdown",
    "author": "Marko (ServerlessLife)<marko@serverlesslife.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/ServerlessLife/lambda-error-sns-sender.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "lambda-error-sns-sender",
        "lambda-error-sns-sender._jsii"
    ],
    "package_data": {
        "lambda-error-sns-sender._jsii": [
            "lambda-error-sns-sender@0.0.50.jsii.tgz"
        ],
        "lambda-error-sns-sender": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.70.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
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
