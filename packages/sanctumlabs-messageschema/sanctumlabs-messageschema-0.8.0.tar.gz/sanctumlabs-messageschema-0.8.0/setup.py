from setuptools import setup, find_packages
import os

version = os.environ.get(
    "PACKAGE_VERSION",
    os.environ.get("CI_COMMIT_TAG", os.environ.get("CI_JOB_ID", "0.1-dev")),
)

setup(
    name="sanctumlabs-messageschema",
    version=version,
    description="Shared data models & message schemas for Sanctum Labs services",
    author="Brian Lusina",
    author_email="1178317-BrianLusina@users.noreply.gitlab.com",
    license="Proprietary",
    url="https://gitlab.com/sanctumlabs/libraries/messageschema",
    packages=find_packages(),
    package_data={"sanctumlabs": ["py.typed", "*.pyi", "**/*.pyi"]},
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=["protobuf >= 4.22.4", "protoc-gen-validate >= 1.0.0"],
)
