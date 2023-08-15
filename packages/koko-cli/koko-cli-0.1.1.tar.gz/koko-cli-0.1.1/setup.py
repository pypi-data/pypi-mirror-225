from setuptools import setup, find_packages

setup(
    name='koko-cli',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'faiss-cpu',
        'datasets',
        'transformers',
        'sentence_transformers',
        'InstructorEmbedding',
        'questionary'
    ],
    entry_points={
        'console_scripts': [
            'koko=koko_pkg.koko:main',
            'initialize_koko=koko_pkg.initialize_koko:initialize_koko',
        ],
    },
)