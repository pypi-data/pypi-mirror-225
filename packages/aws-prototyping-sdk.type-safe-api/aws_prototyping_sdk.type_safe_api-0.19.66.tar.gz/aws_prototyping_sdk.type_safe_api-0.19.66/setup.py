import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws_prototyping_sdk.type_safe_api",
    "version": "0.19.66",
    "description": "@aws-prototyping-sdk/type-safe-api",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-prototyping-sdk",
    "long_description_content_type": "text/markdown",
    "author": "AWS APJ COPE<apj-cope@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/aws-prototyping-sdk"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_prototyping_sdk.type_safe_api",
        "aws_prototyping_sdk.type_safe_api._jsii"
    ],
    "package_data": {
        "aws_prototyping_sdk.type_safe_api._jsii": [
            "type-safe-api@0.19.66.jsii.tgz"
        ],
        "aws_prototyping_sdk.type_safe_api": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.81.0, <3.0.0",
        "aws_prototyping_sdk.nx_monorepo<1.0.0",
        "aws_prototyping_sdk.pdk_nag<1.0.0",
        "cdk-nag>=2.27.24, <3.0.0",
        "constructs>=10.2.39, <11.0.0",
        "jsii>=1.82.0, <2.0.0",
        "projen>=0.71.92, <0.72.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": [
        "src/aws_prototyping_sdk/type_safe_api/_jsii/bin/clean-openapi-generated-code",
        "src/aws_prototyping_sdk/type_safe_api/_jsii/bin/copy-gradle-wrapper",
        "src/aws_prototyping_sdk/type_safe_api/_jsii/bin/generate",
        "src/aws_prototyping_sdk/type_safe_api/_jsii/bin/generate-html-redoc-docs",
        "src/aws_prototyping_sdk/type_safe_api/_jsii/bin/generate-mock-data",
        "src/aws_prototyping_sdk/type_safe_api/_jsii/bin/parse-openapi-spec"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
