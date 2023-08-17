from distutils.core import setup

with open("README.md", 'r') as file:
    longDiscription = file.read() 

setup(
  name = 'SimpleNode',
  packages = ['SimpleNode'],
  version = '0.4a3',
  license='MIT',
  description = 'Package for working with Neural Networks for small projects',
  long_description_content_type = "text/markdown",
  long_description = longDiscription,
  author = 'Artyom Yesayan',
  author_email = 'yesart8@gmail.com',
  url = 'https://github.com/Rkaid0/SimpleNode',
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
  ],
)
