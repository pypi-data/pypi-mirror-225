from setuptools import setup, find_packages

setup(
    name='2op_ai',
    version='0.1',
    description='A package for fine-tuning and utilizing the 2op_ai model',
    author='Your Name',
    author_email='sscla-ops@outlook.com',
    url='https://github.com/sscla1/2op_ai',
    packages=find_packages(),
    install_requires=[
    'torch',
    'transformers',
    'pandas',
    'nbformat',
    'chardet',
],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', # Modify as needed
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='machine-learning transformers fine-tuning ai',
)