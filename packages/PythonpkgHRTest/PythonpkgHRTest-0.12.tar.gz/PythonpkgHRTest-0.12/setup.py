from setuptools import setup, find_packages


setup(
    name='PythonpkgHRTest',
    version='0.12',
    license='MIT',
    author="suryateja",
    author_email='suryateja.d@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/3PPMSTest/PythonpkgHRTest',
    keywords='PythonpkgHRTest',
    install_requires=[
          'scikit-learn',
      ],

)
