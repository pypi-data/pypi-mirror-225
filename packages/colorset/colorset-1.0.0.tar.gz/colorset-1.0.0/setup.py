from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='colorset',
  version='1.0.0',
  author='AlexTaran',
  author_email='at@dmtel.ru',
  description='Colorset management classes',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/AlexTaran/colorset',
  packages=find_packages(),
  install_requires=['lxml>=4.9.2'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='colorset legend python',
  project_urls={
    'Documentation': 'https://github.com/AlexTaran/colorset'
  },
  python_requires='>=3.10'
)

