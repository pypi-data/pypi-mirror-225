from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: Unix',
    'Operating System :: iOS',
]

setup(
    name='nlp-swahili-text-cleaner',
    version='0.0.2',
    description='Swahili text cleaning library',
   # long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Shadrack Kajigili',
    author_email='shadrackkajigili4@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='swahili_text_cleaner',
    packages=find_packages(),
    install_requires=['nltk']
)