from setuptools import setup, find_packages

setup(
    name="stealth-browser",
    version="1.0.0",
    description="轻量级反检测浏览器指纹分析CLI工具",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="StealthBrowser Team",
    license="MIT",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[],
    extras_require={},
    entry_points={
        "console_scripts": [
            "stealth-browser=stealth_browser.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Environment :: Console",
    ],
)
