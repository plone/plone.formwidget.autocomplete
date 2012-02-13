from setuptools import setup, find_packages

version = '1.2.3'

setup(name='plone.formwidget.autocomplete',
      version=version,
      description="AJAX selection widget for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='Plone selection widget AJAX',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://plone.org/products/plone.formwidget.autocomplete',
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
