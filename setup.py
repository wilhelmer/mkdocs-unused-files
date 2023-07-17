from setuptools import setup, find_packages

setup(
    name='mkdocs-unused-files',
    version='0.2.0',
    description='An MkDocs plugin to find unused (orphaned) files in your project.',
    long_description='',
    keywords='mkdocs',
    url='https://github.com/wilhelmer/mkdocs-unused-files.git',
    author='Lars Wilhelmer',
    author_email='lars@wilhelmer.de',
    license='MIT',
    python_requires='>=2.7',
    install_requires=[
        'mkdocs>=1.0.4',
        'beautifulsoup4>=4.12.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'unused_files = mkdocs_unused_files.plugin:UnusedFilesPlugin'
        ]
    }
)
