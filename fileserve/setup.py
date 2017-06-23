from setuptools import setup,find_packages

install_requires = [
    'tornado>=3.1.0',
]

setup(
    name='fileserve',
    version='0.2',
    description='tornado simple HttpService',
    author='syf',
    author_email='git@suyafei.com',
    url='https://github.com/myyyy',
    keywords = 'HttpService',
    license='BSD',
    py_modules=['fileserve'],
    packages = ['fileserve'],
    scripts = ['fileserve/server.py'],
    package_data={'fileserve': ['static/*',
        'templates/index.html'
    ]},
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
)
