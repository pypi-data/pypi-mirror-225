import setuptools


def load_long_description():
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description


def get_version():
    with open("msp/__init__.py", "r") as f:
        for line in f.readlines():
            if line.startswith("__version__"):
                return line.split('"')[1]
        else:
            raise TypeError("NO MSP_VERSION")


def get_required_packages():
    required_packages = []
    with open("requirements.txt", "r") as f:
        for line in f.readlines():
            required_packages.append(line.strip())
    return required_packages


setuptools.setup(
    name="msp",
    version=get_version(),
    author="sktdmi",
    author_email="mls@sktai.io",
    description="MSP SDK",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/sktaiflow/msp-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiohttp==3.8.4",
        "requests==2.30.0",
        "opentelemetry-api==1.13.0",
        "opentelemetry-sdk==1.13.0",
        "opentelemetry-instrumentation-requests==0.34b0",
        "opentelemetry-exporter-otlp==1.13.0",
        "opentelemetry-instrumentation-aiohttp-client==0.34b0",
    ],
)
