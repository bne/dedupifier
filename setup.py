from setuptools import setup

setup(
    name='Dedupifier',
    version='0.1',
    entry_points="""
    [console_scripts]
    dedupe=dedupifier.dedupe:main
    """,
)