from setuptools import setup, find_packages
# from pathlib import Path
# this_directory = Path(__file__).resolve().parent
# readme_path = this_directory / "readme.md"
# long_description = readme_path.read_text(encoding = 'utf-8')

setup(
    	name = 'PARE_TOOLBOX',
    	version = '2023.8',
		url = 'https://wmpjrufg.github.io/PAREPY/',
        description = 'The PAREpy is an easy-to-use environment for applying probabilistic modeling.',
		# long_description = long_description,
		# long_description_content_type='text/markdown',   
    	license = 'MIT License',
        author = ['Wanderlei Malaquias Pereira Junior', 
                  'Donizetti Aparecido de Souza Junior', 
                  'Romes Antônio Borges',
                  'Mateus Pereira da Silva'],
    	author_email = 'wanderlei_junior@ufcat.edu.br',
        install_requires = ["numpy", "scipy", "pandas"],
		classifiers = [	
            			'Development Status :: 4 - Beta',
            			'Topic :: Education',
                        'Topic :: Scientific/Engineering',
                        'License :: OSI Approved :: MIT License',
						'Programming Language :: Python',
                        ],
        packages = find_packages()
     )

# https://pypi.org/classifiers/
# https://www.alura.com.br/artigos/como-publicar-seu-codigo-python-no-pypi