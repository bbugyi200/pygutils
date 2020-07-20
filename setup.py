"""The setup script."""

import setuptools


setuptools.setup(
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
    keywords='gutils',
    name='bbugyi-pygutils',
    packages=setuptools.find_packages(),
    test_suite='tests',
    tests_require=['pytest'],
    url='https://github.com/bbugyi200/pygutils',
    version='1.0.0',
    zip_safe=False,
)
