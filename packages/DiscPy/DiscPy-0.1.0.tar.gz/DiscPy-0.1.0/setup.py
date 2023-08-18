from setuptools import setup

setup(
    name='DiscPy',
    version='0.1.0',    
    description='A example Python package',
    url='https://github.com/Chaaronn/DiscPy',
    author='Matt Voce',
    author_email='mattvoce117@gmail.com',
    license='MIT License',
    packages=['DiscPy'],
    install_requires=['requests'                    
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
)