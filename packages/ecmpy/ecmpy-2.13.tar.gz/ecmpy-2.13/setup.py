from setuptools import setup, find_packages

setup(
    name='ecmpy',
    version='2.13',
    packages=find_packages(),
    package_data={
        "ecmpy": [
            "*",
            "*/*",
            "_cache/ncbi_taxonomy/*",
            "_cache/sabio_rk_total/*",            
            "analysis/get_kcat_mw_by_AutoPACMEN/reaction_kcat_MW.csv",
            "data/*",
            "model/*",
            "script/*"
            "ipynb_checkpoints/ECMpy_function-checkpoint.py"
            "ipynb_checkpoints/get_ecGEM_onestop-checkpoint.py"            
            "__pacache__/*"            
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
