from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    install_requires = f.read().splitlines()

setup(
    name='boxcraft',
    version='0.0.2',
    author='JustMe',
    author_email='lomv0209@gmail.com',
    description='Libreria para el Procesamiento Distribuido',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Lucho00Cuba/boxcraft',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    keywords='python box',
    install_requires=install_requires,
    python_requires='>=3.6',
)