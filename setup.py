from setuptools import find_packages
from setuptools import setup

version = "2.0.0a1"

setup(
    name="plone.formwidget.autocomplete",
    version=version,
    description="AJAX selection widget for Plone",
    long_description=open("README.rst").read() + "\n" + open("CHANGES.rst").read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="Plone selection widget AJAX",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/plone.formwidget.autocomplete/",
    license="GPL version 2",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["plone", "plone.formwidget"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "setuptools",
        "z3c.formwidget.query",
        "plone.z3cform >= 0.7.4",
        "Products.CMFCore",
        "Products.GenericSetup",
        "z3c.form",
        "Zope",
    ],
    extras_require={
        "test": [
            "plone.testing",
            "plone.app.testing",
        ],
    },
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
