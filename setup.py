from setuptools import setup, find_packages

version = '1.5.1.dev0'

setup(name='plone.formwidget.autocomplete',
      version=version,
      description="AJAX selection widget for Plone",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.rst").read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 5.1",
          "Framework :: Plone :: 5.2",
          "Framework :: Plone :: 6.0",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
        ],
      keywords='Plone selection widget AJAX',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='https://github.com/plone/plone.formwidget.autocomplete/',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.formwidget'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'z3c.formwidget.query',
          'plone.z3cform >= 0.7.4',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
