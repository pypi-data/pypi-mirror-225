from distutils.core import setup

setup(name='socksimap',
    version='1.0.1',
    description='Connect to IMAP through Socks',
    long_description=open('README.md', "r").read(),
    long_description_content_type='text/markdown',
    install_requires=["PySocks"],
    author='optinsoft',
    author_email='optinsoft@gmail.com',
    keywords=['socks','imap'],
    url='https://github.com/optinsoft/socksimap',
    packages=['socksimap']
)