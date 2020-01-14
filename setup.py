from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='azure_eventhubs_client',
    version="0.95",
    author="Knockri",
    author_email="saman@knockri.com",
    url='https://github.com/KnockriInc/azure_eventhubs_client',
    maintainer='Saman A. Pour',
    maintainer_email='samanamp@knockri.com',
    description="Azure Eventhubs client that simply works",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['redis', 'azure-eventhub==1.3.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
