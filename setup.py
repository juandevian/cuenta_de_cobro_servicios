from setuptools import setup, find_packages

setup(
    name="ori_cc_servicios",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        'colorlog',
        'python-dateutil',
        'python-dotenv',
        'mysql-connector-python',
        'openpyxl',
        'pandas',
        'pydantic',
        'PyQt5',
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'ori-cc-servicios=main:main',
        ],
    },
)