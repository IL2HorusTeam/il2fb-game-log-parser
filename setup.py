from setuptools import setup

setup(
    name='il2ds-log-parser',
    version='0.9.0',
    description='Parser of IL-2 FB Dedicated Server events log.',
    license='BSD License',
    url='https://github.com/IL2HorusTeam/il2ds-log-parser',
    author='Alexander Oblovatniy',
    author_email='oblovatniy@gmail.com',
    packages=['src/il2ds_log_parser', ],
    package_dir={'il2ds_log_parser': 'src/il2ds_log_parser', },
    install_requires=[i.strip() for i in open("requirements.pip").readlines()],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Free for non-commercial use',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
    ],
)
