from setuptools import setup

setup(
    name='mdnet',
    version='0.1.1',
    packages=['mdnet'],
    install_requires=[
        'markdown',
        'jinja2',
        'python-frontmatter'
    ],
    entry_points={
        'console_scripts': [
            'mdnet=mdnet.mdnet:main',
        ],
    },
)
