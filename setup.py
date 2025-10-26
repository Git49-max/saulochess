# setup.py
from setuptools import setup, find_packages

setup(
    name='saulochess',
    version='0.1.0',  # Versão inicial. Incremente para 0.1.1, 0.2.0, etc.
    
    # Encontra a pasta 'saulochess' e a trata como o pacote principal
    packages=find_packages(),
    
    description='Ferramentas de análise e revisão de partidas de xadrez baseadas em Stockfish.',
    long_description=open('README.md', encoding='utf-8').read() if open('README.md', encoding='utf-8').read() else 'Análise de xadrez.',
    long_description_content_type='text/markdown',
    
    author='Saulo',
    author_email='seu.email@exemplo.com', # Use seu e-mail real ou um e-mail de suporte
    url='https://github.com/SeuUsuario/saulochess', # Preencha com o link do seu repositório no GitHub
    
    # Licença definida para o pacote. Corresponde à que você criou.
    license='MIT', 
    
    # Dependências do seu código. O usuário precisa ter estes instalados.
    install_requires=[
        'python-chess',
        'pandas',
        'numpy',
        'tqdm'
    ],
    
    classifiers=[
        'Development Status :: 3 - Alpha', # Indicando que ainda está em desenvolvimento inicial
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