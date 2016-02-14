from setuptools import setup, find_packages


req = open('requirements.txt')
REQUIREMENTS = req.readlines()
req.close()

# Dynamically retrieve the version from the module
version_string = __import__('salvius').__version__

setup(
    name='salvius',
    version=version_string,
    url='https://github.com/gunthercox/salvius',
    description='Open source humanoid robot.',
    author='Gunther Cox',
    author_email='gunthercx@gmail.com',
    packages=find_packages(),
    package_dir={'salvius': 'salvius'},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license='MIT',
    zip_safe=True,
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    entry_points = {
        'console_scripts': [
            'salvius=salvius.salvius:main'
        ],
    }
)
