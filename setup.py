from setuptools import setup, find_packages

setup(
    name = 'plexshell',
    version = '0.0.1',
    description = 'A shell to interact with the Plex Media Server',
    author = 'Jamie Kirkpatrick',
    author_email = 'jamie@plexinc.com',
    packages = find_packages(exclude = ["tests", "doc"]),
    install_requires = [
        'lxml'
    ],
    entry_points = {
        'console_scripts': [
            'psh = plexshell.scripts.shell:main',
        ],
    },
    zip_safe = True
)
