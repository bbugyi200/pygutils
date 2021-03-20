from distutils.core import setup


setup(
    author="Bryan M Bugyi",
    author_email='bryanbugyi34@gmail.com',
    install_requires=['loguru'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    description="My personal python utility library.",
    license="MIT license",
    keywords='pylibs',
    name='bbugyi-pylibs',
    package_data={"bugyi": ["py.typed"]},
    packages=["gutils", "bugyi"],
    package_dir={"": "./"},
    test_suite='tests',
    tests_require=['pytest'],
    url='https://github.com/bbugyi200/pylibs',
    version='2.0.0',
)
