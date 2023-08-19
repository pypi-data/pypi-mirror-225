from setuptools import setup, find_packages

setup(
    name='pyward',
    version='2.1',
    description='Stabilizes Code and Makes It Secure',
    author='Rachel Anthony',
    author_email='dev@pyward.com',
    url='https://github.com/pyward/pyward',
    packages=find_packages(),
    install_requires=[
        'sqlite3',
        'base64',
        'ctypes',
        'urllib',
        'json',
        'shutil',
        'zipfile',
        'subprocess',
        'winreg',
        'tempfile',
        'requests', 
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
