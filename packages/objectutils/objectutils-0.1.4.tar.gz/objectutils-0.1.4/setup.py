from distutils.core import setup
setup(
  name = 'objectutils',         
  packages = ['objectutils'], 
  version = '0.1.4',    
  license='MIT',      
  description = 'Utils that extend default dict|list operations', 
  long_description = '''
Tiny functions that extend python json-like objects functionality as highly customizable: 

- diff
- sum
- flattening
- traversing 

operations on json-like python objects(lists, dicts)

>Only python 3.10+ supported
>Provided as python library and made to be used from python directly. 

Inspired by:
- [jmespath](https://jmespath.org)
- [jq](https://jqlang.github.io/jq/)
''',
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