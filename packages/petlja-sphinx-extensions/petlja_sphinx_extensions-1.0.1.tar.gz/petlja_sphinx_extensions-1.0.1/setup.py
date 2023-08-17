from setuptools import setup, find_packages

setup(
    python_requires=">=3.7",
    version='1.0.1',
    author="Fondacija Petlja",
    author_email="team@petlja.org",
    description="Petlja's sphinx extensions for e-learning content",
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
    name='petlja_sphinx_extensions',
    packages=find_packages(),
    install_requires=[
        'sphinx',
    ],
)