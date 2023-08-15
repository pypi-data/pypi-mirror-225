
from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
        name                =   'pfdo_mgz2image',
        version             =   '2.1.7',
        description         =   'Runs mgz2image on each nested dir of an inputdir',
        long_description    =   readme(),
        python_requires     =   ">= 3.8",
        url                 =   'http://github.com/FNNDSC/pfdo_mgz2image',
        author              =   'FNNDSC',
        author_email        =   'dev@babyMRI.org',
        license             =   'MIT',
        packages            =   ['pfdo_mgz2image'],
        install_requires=[
            'pfmisc',
            'pftree',
            'pfdo',
            'mgz2imgslices==2.1.2',
            'scikit-image',
            'nibabel',
            'pandas',
            'numpy',
            'imageio',
            'matplotlib',
        ],
        test_suite          =   'nose.collector',
        tests_require       =   ['nose'],
        entry_points={
          'console_scripts': [
              'pfdo_mgz2image = pfdo_mgz2image.__main__:main'
          ]
        },
        zip_safe            =   False,
        )
