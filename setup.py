from setuptools import setup

setup(name='Identifier-Name-Linter',
      version='1.0',
      description='Fetching Identifier and running Violation Checks',
      url='https://github.com/sreya2906/Identifier-Name-Linter',
      author='Sreya Bhattacharya',
      author_email='sreya2906@gmail.com',
      license='MIT',
      python_requires='>3.6',
      install_requires=[
          'PyGithub', 'tree_sitter', 'pyenchant'
      ],
      zip_safe=False)
