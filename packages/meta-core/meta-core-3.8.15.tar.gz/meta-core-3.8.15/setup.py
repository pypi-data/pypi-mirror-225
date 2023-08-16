from setuptools import setup, find_packages

requirements = [
    'opencv-python',
    'setuptools',
    'numpy',
    'pillow',
    'torch',
    'ftfy',
    'regex',
]

__version__ = 'V3.08.15'

setup(
    name='meta-core',
    version=__version__,
    author='CachCheng',
    author_email='tkggpdc2007@163.com',
    url='https://github.com/CachCheng/cvreid',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    description='Meta Core Toolkit',
    license='Apache-2.0',
    packages=find_packages(exclude=('docs', 'tests', 'scripts')),
    package_data={'metacore': ['open_clip/model_configs/*.json', 'open_clip/*.txt.gz']},
    zip_safe=True,
    include_package_data=True,
    install_requires=requirements,
)
