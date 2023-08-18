from setuptools import setup

setup(name='async_nec_beamer',
      version='0.2.2',
      description='NEC Beamer Web Interface Wrapper (Async)',
      url='https://github.com/heinrich-foto/async_nec_beamer',
      author='Heinrich-Foto',
      author_email='async_nec_beamer@heinrich-foto.de',
      license='MIT',
      packages=['async_nec_beamer'],
      install_requires=[
          'aiohttp[speedups]',
          'click'
      ],
      zip_safe=False,
      scripts=['bin/async_nec_beamer'],
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      )
