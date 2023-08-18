from setuptools import setup


setup(
    name="sarmat",
    version="1.4.0",
    packages=[
        "sarmat.core",
        "sarmat.core.actions",
        "sarmat.core.behavior",
        "sarmat.core.constants",
        "sarmat.core.context",
        "sarmat.core.context.containers",
        "sarmat.core.context.models",
        "sarmat.core.exceptions",
        "sarmat.core.factory",
        "sarmat.core.verification",
        "sarmat"
    ],
    install_requires=[
        "pydantic",
    ],
    url="",
    author="Artel",
    author_email="artel61@gmail.com",
    description="Sarmat",
)
