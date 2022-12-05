from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    required = [
        l.strip()
        for l in f.read().splitlines()
        if l.strip() and not l.strip().startswith("#")
    ]

setup_args = dict(
    name="gopoints",
    version="0.1.0",
    packages=find_packages(),
    author="Søren Winkel Holm",
    author_email="s183911@student.dtu.dk",
    install_requires=required,
    description="Running gopoints simulation",
    long_description_content_type="text/markdown",
    long_description=readme,
)

if __name__ == "__main__":
    setup(**setup_args)
