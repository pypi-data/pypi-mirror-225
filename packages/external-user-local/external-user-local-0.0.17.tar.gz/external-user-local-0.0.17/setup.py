import setuptools
# used by python -m build
# python -m build needs pyproject.toml or setup.py
setuptools.setup(
     name='external-user-local',  
     version='0.0.17', # https://pypi.org/project/external-user-local/
     author="Circles",
     author_email="info@circles.life",
     # TODO: Please update the description and delete this line
     description="PyPI Package for Circles external-user library Local/Remote Python",
     # TODO: Please update the long description and delete this line    
     long_description="This is a package for sharing common external-user function used in different repositories",
     long_description_content_type="text/markdown",
     url="https://github.com/circles",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
     ],
 )
