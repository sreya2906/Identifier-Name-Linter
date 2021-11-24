from setuptools import setup
import os
from git.repo.base import Repo

if not os.path.exists("./Language-Implementations/tree-sitter-python"):
    Repo.clone_from("https://github.com/tree-sitter/tree-sitter-python", "./Language-Implementations/tree-sitter-python")
if not os.path.exists("./Language-Implementations/tree-sitter-javascript"):
    Repo.clone_from("https://github.com/tree-sitter/tree-sitter-javascript", "./Language-Implementations/tree-sitter-javascript")
if not os.path.exists("./Language-Implementations/tree-sitter-ruby"):
    Repo.clone_from("https://github.com/tree-sitter/tree-sitter-ruby", "./Language-Implementations/tree-sitter-ruby")
if not os.path.exists("./Language-Implementations/tree-sitter-go"):
    Repo.clone_from("https://github.com/tree-sitter/tree-sitter-go", "./Language-Implementations/tree-sitter-go")

setup(name='Identifier-Name-Linter',
      version='1.0',
      description='Fetching Identifier and running Violation Checks',
      url='https://github.com/sreya2906/Identifier-Name-Linter',
      author='Sreya Bhattacharya',
      author_email='sreya2906@gmail.com',
      license='MIT',
      python_requires='>3.6',
      install_requires=[
          'PyGithub', 'tree_sitter', 'pyenchant', 'GitPython'
      ],
      zip_safe=False)
