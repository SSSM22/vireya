from pathlib import Path
from setuptools import setup

ROOT = Path(__file__).resolve().parent
README = (ROOT / "README.md").read_text(encoding="utf-8")

setup(
    name="vireya",
    version="0.1.0",
    description="Vireya domain scaffold",
    long_description=README,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=["vireya"],
    include_package_data=True,
    python_requires=">=3.11",
)
