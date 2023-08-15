import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

NAME = 'django-gcloud-connectors'

DESCRIPTION = 'A Django library for connecting to Google Cloud Datastore from Python 3 runtimes.'
URL = 'https://gitlab.com/potato-oss/google-cloud/django-gcloud-connectors'
LONG_DESCRIPTION = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

AUTHOR = "Potato London Ltd."
AUTHOR_EMAIL = "mail@p.ota.to"

if os.environ.get('CI_COMMIT_TAG'):
    VERSION = os.environ['CI_COMMIT_TAG']
else:
    VERSION = '1.0.0'

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    keywords=["Google Cloud Datastore", "Google App Engine", "Django"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=[
        'django>=2.0,<=3.3',
        'pyyaml>=6.0.1,<6.1',
        'google-cloud-datastore>=1.15.3',
        'pyuca==1.2',
    ],
    include_package_data=True,
    extras_require={
        'test': [
            "unittest-xml-reporting==3.2.0",
            "sleuth-mock==0.1"
        ]
    },
)
