from setuptools import setup, find_packages

setup(
    name='il2ds-log-parser',
    version='0.1.0',
    description='Parser of IL-2 FB Dedicated Server events log.',
    license='MIT',
    url='https://github.com/IL2HorusTeam/il2ds-log-parser',
    author='Alexander Oblovatniy',
    author_email='oblovatniy@gmail.com',
    packages=find_packages(exclude=["log_examples", ]),
    install_requires=[i.strip() for i in open("requirements.pip").readlines()],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
    ],
)
