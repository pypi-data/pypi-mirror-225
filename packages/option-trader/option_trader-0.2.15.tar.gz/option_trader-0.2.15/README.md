option trader

# package development
cd option_trader/src
pip install e .
py -m build
py -m twine upload --repository pypi dist/*


#tests
https://docs.pytest.org/en/latest/explanation/goodpractices.html