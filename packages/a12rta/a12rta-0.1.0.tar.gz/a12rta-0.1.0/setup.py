from setuptools import setup, find_packages

setup(
    name="a12rta",
    version="0.1.0",
    description='Script tails logs on N-boxes (ssh)',
    author='Pawel Suchanecki',
    author_email='Pawel.Suchanecki@gmail.com',
    python_requires='>=3.7',
    packages=find_packages(),
    install_requires=[
        "fabric>=2.5.0,<3.0.0",  # The actual version range depends on your code's compatibility
        "PyYAML>=5.4,<6.0",
        "asyncio>=3.4.3,<4.0",  # Since Python 3.7, asyncio is part of the standard library
    ],
    extras_require={
        "dev": [
            "twine>=3.4,<4.0",
        ]
    },
    entry_points={
        'console_scripts': [
            'a12rta=a12rta.a12rta:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
