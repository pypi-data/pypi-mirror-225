from setuptools import setup, find_packages

setup(
    name='aesthetic_text',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Liste des dépendances nécessaires
    ],
    author='Kyleex',
    author_email='antwill34@icloud.com',
    description='to stylized terminal text',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kyleex/aesthetic_text',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
