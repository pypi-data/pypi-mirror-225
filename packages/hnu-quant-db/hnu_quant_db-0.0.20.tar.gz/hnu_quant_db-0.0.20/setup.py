from setuptools import setup, find_packages

setup(
    name='hnu_quant_db',
    version='0.0.20',
    description='HNU Quant Association Database Query Tool',
    author='rikkaka',
    author_email='793329010@qq.com',
    
    packages=find_packages(),
    
    exclude_package_data={
        '': ['*.pyc', '*.pyo', '*.pyd'],
        'private': ["token"]
    },
    
    install_requires=[
        'pandas >= 2.0',
        'sqlalchemy >= 2.0',
        'psycopg2-binary >= 2.9',
        'baostock >= 0.8.8',
        'cachetools >= 5.0',
    ],
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.10',
    ],
)
    