import setuptools
from pip._vendor.pkg_resources import require

setuptools.setup(
     name='trex-web',  
     version='0.0.2',
     author="Jack Lok",
     author_email="sglok77@gmail.com",
     description="TRex web package",
     packages=setuptools.find_packages(),
     package_data={'': ['templates/*', 'static/*.txt']},
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[            
          'flask',
          'Jinja2',
          'MarkupSafe',
          'phonenumbers',
          'requests',
          'testfixtures',
          'flask-babel',
          'Flask-CORS',
      ]
 )




