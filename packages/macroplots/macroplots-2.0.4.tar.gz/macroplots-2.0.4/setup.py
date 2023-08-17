from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()
print('Hello from setup')
setup(
  name='macroplots',
  version='2.0.4',
  author='Izy_Golstein',
  author_email='osipovaajr@gmail.com',
  description='This is my first module',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/IzyGolstein',
  packages=find_packages(),
  install_requires=['requests>=2.25.1','pandas == 2.0.3', 'plotly == 5.9.0'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  project_urls={
    'Documentation': 'https://github.com/IzyGolstein'
  },
  python_requires='>=3.7'
)