from setuptools import setup, find_packages

setup(
    name="promptip",
    version="0.0.1",
    description="Command-line tool to fine-tune prompts for optimal use with GPT-3.5 and GPT-4.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="José Nery",
    author_email="josenerydev@gmail.com",
    url="https://github.com/josenerydev/promptip",
    packages=find_packages(),
    install_requires=["pathspec"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "console_scripts": [
            "promptip=promptip.promptip:main",
        ],
    },
)
