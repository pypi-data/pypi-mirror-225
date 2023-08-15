from setuptools import setup, Extension
setup(
    name='fmath',
    version='1.0.0',
    license='MIT',
    author='Elisha Hollander',
    author_email='just4now666666@gmail.com',
    description='A library for Python for fast math on floats',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/donno2048/fmath',
    project_urls={
        'Documentation': 'https://github.com/donno2048/fmath#readme',
        'Bug Reports': 'https://github.com/donno2048/fmath/issues',
        'Source Code': 'https://github.com/donno2048/fmath',
    },
    python_requires='>=3.0',
    classifiers=['Programming Language :: Python :: 3'],
    ext_modules=[Extension('fmath', ['pyfmath.c'])],
    zip_safe=False,
)