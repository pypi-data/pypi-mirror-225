from setuptools import find_packages, setup

setup(
    name="typed_graphene",
    packages=find_packages(include=["typed_graphene", "typed_graphene.*"]),
    version="0.0.1",
    description="typed-graphene package",
    author="Jeong Yeon Nam<tonynamy@apperz.co.kr>",
    license="MIT",
    install_requires=[],
    setup_requires=["graphene>=2.0.0, <3"],
    tests_require=["pytest==7.4.0"],
    test_suite="tests",
)
