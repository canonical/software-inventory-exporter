"""Set up software_inventory_exporter python module cli scripts."""

from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("LICENSE", encoding="utf-8") as f:
    project_license = f.read()

setup(
    name="software_inventory_exporter",
    use_scm_version={"local_scheme": "node-and-date"},
    description="Exporter for apt packages and snaps in json via web",
    long_description=readme,
    author="Canonical BootStack DevOps Centres",
    url="https://github.com/canonical/software-inventory-exporter",
    license=project_license,
    packages=["software_inventory_exporter"],
    entry_points={
        "console_scripts": [
            "software-inventory-exporter=software_inventory_exporter.cli:main",
        ]
    },
    setup_requires=["setuptools_scm"],
)
