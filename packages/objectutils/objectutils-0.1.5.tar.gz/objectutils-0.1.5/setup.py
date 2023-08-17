from distutils.core import setup

with open("README.md") as file:
    ld = file.read()

setup(
  name = 'objectutils',         
  packages = ['objectutils'], 
  version = '0.1.5',    
  license='MIT',      
  description = 'Utils that extend default dict|list operations', 
  long_description = ld,
  long_description_content_type = "text/markdown",
  author = 'Chmele',              
  url = 'https://github.com/Chmele/difflib/tree/main',  
  keywords = ['dict', 'json', 'jq', 'jmespath'], 
  classifiers=[
    'Development Status :: 3 - Alpha',    
    'Intended Audience :: Developers',  
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.1',
  ],
)