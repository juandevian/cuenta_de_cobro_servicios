from setuptools import setup, find_packages

setup(
    name="ori_cc_servicios",
    version="0.2.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        'colorlog',
        'dateutil',
        'dotenv',
        'keyring',
        'mysql.connector',
        'openpyxl',
        'pandas',
        'pydantic',
        'PyQt5',
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'ori-cc-servicios=main:main',
        ],
    },
)