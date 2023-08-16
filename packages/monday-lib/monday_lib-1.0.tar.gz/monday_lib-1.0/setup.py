from distutils.core import setup
setup(
  name = 'monday_lib',         
  packages = ['monday_lib'],  
  version = '1.0',      
  license='GNU GPLv3',        
  description = 'monday_lib is a wrapper for Monday.com API library, every endpoint is made into Python here. Everything you need to get started is your Monday.com API key.', 
  author = 'Frederich Pedersen',                  
  author_email = 'frodo@hobbits.dk',      
  url = 'https://github.com/Frodothedwarf/monday_lib',   
  download_url = 'https://github.com/Frodothedwarf/monday_lib/archive/refs/tags/v_03.tar.gz',    
  keywords = ['monday', 'api', 'wrapper','endpoint','endpoints','monday.com'],   
  install_requires=[
          'requests',
          're',
          'time'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU GPLv3', 
    'Programming Language :: Python :: 3',
  ],
)