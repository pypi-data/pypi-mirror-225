from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cloudsculpter',
    version='0.0.1',
    packages=find_packages(),
    author='Wes Ladd',
    author_email='wesladd@traingrc.com',
    description='A package to deploy cloudformation resources with natural language instructions, automatically healing failed deployments with OpenAI troubleshooting',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/righteousgambit/cloudsculpter',
    install_requires=[
        'boto3',      # AWS SDK for Python
        'openai',     # OpenAI API
        'pyyaml',     # YAML file management
        'termcolor',  # Colorize console output
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cloudsculpter = cloudsculpter.main:main',
        ],
    },
)
