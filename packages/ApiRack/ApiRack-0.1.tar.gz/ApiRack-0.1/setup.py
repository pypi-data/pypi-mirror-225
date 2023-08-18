from setuptools import setup, find_packages

setup(
    name='ApiRack',
    version='0.1',
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
            'rack=rack_pkg.rack:main',
            'initialize_rack=rack_pkg.initialize_rack:initialize_rack',
        ],
    },
)
