from distutils.core import setup

setup(
  name = 'SimpleNode',
  packages = ['SimpleNode'],
  version = '0.1',
  license='MIT',
  description = 'Package for working with Neural Networks for small projects',
  author = 'Artyom Yesayan',
  author_email = 'yesart8@gmail.com',
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Rkaid0/SimpleNode/archive/refs/tags/v_0.1.tar.gz',
  keywords = ['NeuralNetwork', 'GradientDescent', 'AI'],
  install_requires=[
          'numpy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10',
    'Operating System :: OS Independent',
  ],
)
