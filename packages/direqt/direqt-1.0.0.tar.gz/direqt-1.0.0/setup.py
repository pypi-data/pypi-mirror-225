from setuptools import setup

setup(name='direqt',
      version='1.0.0',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python :: 3'
      ],
      description='Client library for Direqt Ads API',
      url='https://github.com/direqt/direqt-sdk-python',
      author='Myk Willis',
      author_email='myk@direqt.io',
      license='Apache License 2.0',
      packages=['direqt'],
      install_requires=[
            'google-auth',
            'requests',
            'requests_toolbelt'
      ],
      platforms='any',
      setup_requires=[
            'pytest-runner'
      ],
      tests_requires=[
            'pytest',
            'requests-mock'
      ],
      zip_safe=False)
