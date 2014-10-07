from distutils.core import setup

setup(
    name='kanc',
    version='1.0',
    packages=['kanc', 'kanc.command'],
    install_requires = ['tabulate'],
    scripts=['scripts/kanc'],
    )

