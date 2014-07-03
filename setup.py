from setuptools import setup, find_packages

setup(
    name='jabberbot',
    version='0.1.0',
    description='A Jabber Bot for my XMPP service',
    url='https://github.com/ScreenDriver/jabber-bot',
    author='RaspberryRice',
    author_email='christian@echooff.de',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        'dnspython3>=1.11.1',
        'feedparser>=5.1.3',
        'microsofttranslator>=0.5',
        'pep8>=1.5.7',
        'requests>=2.3.0',
        'simplejson>=3.5.2',
        'sleekxmpp>=1.3.1'
    ],
    package_data={
        'jabberbot': [
            'lang_codes.txt',
            'mother_jokes.txt',
            'slaps.txt'
        ]
    }
)
