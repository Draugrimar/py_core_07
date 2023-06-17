from setuptools import setup

setup(name='clean_folder',
      version='0.1.1',
      description='Cleaning and sorting service.',
      url='https://github.com/Draugrimar/py_core_07',
      author='Draugrimar',
      author_email='mr.sanscrit@gmail.com',
      license='none',
      packages=['clean_folder'],
      entry_points={'console_scripts': ['cleaning = clean_folder.sort:cleaning']})