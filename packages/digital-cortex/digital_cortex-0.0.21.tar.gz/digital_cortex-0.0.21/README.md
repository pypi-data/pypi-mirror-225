# digital-cortex-python

Python Client package for Digital Cortex

[# https://packaging.python.org/en/latest/tutorials/packaging-projects/]()

Aug-08-2023

twine upload --repository testpypi dist/* should reference the [testpypi] section in .pypirc. It is not.

to get around this, I need to enter `__token__` as my username and my api key as password. 

You must update the version number in pyproject.toml every time you want to push.

You should probably move this to Poetry


FUNCTIONS WERE WRITTEN FOR THE OLD VERSION OF DC
