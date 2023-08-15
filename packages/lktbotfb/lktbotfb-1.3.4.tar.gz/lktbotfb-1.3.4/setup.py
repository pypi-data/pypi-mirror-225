from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='lktbotfb',
  version='1.3.4',
  description='This makes it easy for you to create a chatbot for your Facebook page',
  long_description=open('README.txt').read(),
  url='https://github.com/AmirLouktaila/lktbotfb',  
  author='Salah Louktaila',
  author_email='amir.Louktila@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['chatbot','fbbot','fbchat'], 
  package_dir={"":"src"},
  packages=find_packages(where="src"),  
  install_requires=['django'],


)