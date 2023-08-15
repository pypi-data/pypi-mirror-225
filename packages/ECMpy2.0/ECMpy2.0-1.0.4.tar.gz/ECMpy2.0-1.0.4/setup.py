from setuptools import setup, find_packages

setup(
    name='ECMpy2.0',
    version='1.0.4',
    packages=find_packages(),
    package_data={
        "ECMpy2.0-main": [
            "*",
            "*/*",
            "_cache/*",
            "analysis/*",
            "data/*",
            "model/*",
            "script/*"
        ]
    },
    license='MIT',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'cobra==0.21.0',
        'openpyxl',
        'requests',
        'pebble',
        'xlsxwriter',
        'Bio',
        'Require',
        'quest',
        'scikit-learn',
        'RDKit',
        'seaborn',
        'pubchempy',
        'torch',
        'ipykernel',
        'bioservices==1.10.4',
        'pyprobar',
        'xmltodict',
        'plotly',
        'kaleido',
        'nbformat',
        ],
    author='Zhitao Mao',
    author_email='mao_zt@tib.cas.cn',
    description='Automated construction of enzyme constraint models using ECMpy workflow.',
    url='https://github.com/tibbdc/ECMpy2.0',
)
