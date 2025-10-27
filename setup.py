from setuptools import setup, find_packages

setup(
    name='saulochess',
    version='0.1.7.01',
    
    # Encontra a pasta 'saulochess' e a trata como o pacote principal
    packages=find_packages(),
    
    description='Ferramentas de análise e revisão de partidas de xadrez baseadas em Stockfish.',
    
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    
    author='Saulo',
    author_email='doroteios@outlook.com',
    url='https://github.com/Git49-max/saulochess',
    
    license='MIT',
    
    install_requires=[
        'python-chess',
        'pandas',
        'numpy',
        'tqdm'
    ],
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Games/Entertainment',
    ],
    keywords='chess stockfish analysis engine review',
)