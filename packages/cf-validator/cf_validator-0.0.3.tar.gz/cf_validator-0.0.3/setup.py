from setuptools import setup

setup(
    name='cf_validator',
    version='0.0.3',
    description='Accepts the path or web url of cloudformation document and validates it.',
    py_modules=["cf_validator"],
    package_dir={'':'src'},
)