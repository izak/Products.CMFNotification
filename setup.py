from setuptools import setup, find_packages
import os

version = '2.2a1'

setup(
    name='Products.CMFNotification',
    version=version,
    description=\
        "A Plone product that allows users to be notified when various events "
        "occur in the portal: item creation or modification, workflow "
        "actions, etc.",
    long_description=open("README.txt").read() + "\n" +
                    open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
    "Framework :: Plone",
    "Programming Language :: Python",
    ],
    keywords='CMFNotification',
    author='Pilot Systems',
    author_email='ploneorg@pilotsystems.net',
    url='http://svn.plone.org/svn/collective/Products.CMFNotification',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
    setup_requires=["PasteScript"],
    paster_plugins=["ZopeSkel"],
    )
