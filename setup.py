from setuptools import setup, find_packages

setup(
    name="fede_crawl4ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.9.3",
        "pillow>=8.0.0",
        "pydantic>=1.8.0",
        "rich>=10.0.0",
        "cairosvg>=2.7.0",
    ],
    python_requires=">=3.8",
) 