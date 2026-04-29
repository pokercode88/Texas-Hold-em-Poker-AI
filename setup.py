from setuptools import setup, find_packages

setup(
    name="texas-holdem-ai",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Texas Hold'em AI System with CFR and Reinforcement Learning",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/niubideren111/Texas-Holdem-AI-System",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: C++",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
    ],
    extras_require={
        "dev": ["pytest>=6.2.0", "black", "flake8"],
        "train": ["torch>=1.10.0", "tensorflow>=2.8.0"],
        "viz": ["matplotlib>=3.4.0"],
    },
    entry_points={
        "console_scripts": [
            "holdem-train=scripts.train:main",
            "holdem-play=scripts.play:main",
            "holdem-eval=scripts.evaluate:main",
        ],
    },
)