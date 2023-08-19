from setuptools import setup, find_packages

# def readme():
#   with open('README.md', 'r') as f:
#     return f.read()
setup(name='sanic_filter',
      version='0.0.2',
      description='Sanic query filter',
      packages=['sanic_filter'],
      author_email='lolkin4777@gmail.com',
      install_requires=['SQLAlchemy>=2.0.20'],
      classifiers=[
          'Programming Language :: Python :: 3.10',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent'
      ],
      python_requires='>=3.9',
      zip_safe=False)

# setup(
#     name='sanic_filter',
#     version='0.0.1',
#     author='lolkin',
#     author_email='lolkin4777@gmail.com',
#     description='Sanic query filter',
#     # long_description=readme(),
#     long_description_content_type='text/markdown',
#     # url='home_link',
#     packages=find_packages(),
#     install_requires=['SQLAlchemy>=2.0.20'],
#     classifiers=[
#         'Programming Language :: Python :: 3.10',
#         'License :: OSI Approved :: MIT License',
#         'Operating System :: OS Independent'
#     ],
#     # keywords='example python',
#     project_urls={
#         'Documentation': 'link'
#     },
#     python_requires='>=3.9'
# )
