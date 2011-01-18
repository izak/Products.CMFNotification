import os
from setuptools import find_packages
from setuptools import setup


version = open(os.path.join(
        'Products', 'CMFNotification', 'version.txt')).read().strip()
description = open('README.txt').read().strip()
long_description = '\n\n'.join((
        open(os.path.join(
        'Products', 'CMFNotification', 'README.txt')).read().strip(),
        open(os.path.join("docs", "HISTORY.txt")).read().strip()))

setup(
    name='Products.CMFNotification',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=(
        'Framework :: Plone',
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        ),
    keywords='CMFNotification plone notification e-mail',
    author='Pilot Systems',
    author_email='ploneorg@pilotsystems.net',
    url='http://plone.org/products/cmfnotification',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=(
        'setuptools',
        'Plone >= 3.0',
        ),
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
    )
