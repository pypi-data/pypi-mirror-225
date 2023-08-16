import setuptools

extras_require = {
    "adafruit": [],
    "awair": [
        "requests>=2.28.2",
        "pyrfc3339>=1.1",
    ],
    "datastax": [
        "gql[requests]>=3.4.0",
    ],
    "google": [
        "google-cloud-bigquery-storage>=2.18.1",
    ],
    "grafana": [
        "requests>=2.28.2",
    ],
    "influxdb": [
        "influxdb-client>=1.36.0",
    ],
    "octopus": [
        "requests>=2.28.2",
        "pyrfc3339>=1.1",
    ],
    "pimoroni": [],
    "psutil": [
        "psutil>=5.9.4",
    ],
    "pypms": [
        "pypms>=0.7.1",
    ],
}

extras_require["all"] = [
    package for group in extras_require.values() for package in group
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snsary",
    version="0.1.0",
    author="Ben Thorner",
    author_email="benthorner@users.noreply.github.com",
    description="A framework for sensor metrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benthorner/snsary",
    project_urls={
        "Bug Tracker": "https://github.com/benthorner/snsary/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "cachetools>=5.3.0",
        "wrapt>=1.14.1",
    ],
    extras_require=extras_require,
)
