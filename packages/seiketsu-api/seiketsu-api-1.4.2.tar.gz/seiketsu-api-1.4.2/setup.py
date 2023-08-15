from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='seiketsu-api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='1.4.2',
    description='A Python library to interact with a chat API',
    author='LoLip_p',
    author_email='mr.timon51@gmail.com',
    url='https://github.com/yourusername/my-json-package',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "api_seiketsu": ["data/*.json"],
    },
    install_requires=[
        "google-cloud-firestore>=2.11.1",
        "google-auth>=2.22.0",
        "google-auth-httplib2>=0.1.0",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
