from setuptools import setup, find_packages

setup(
    name='utilspkg',
    version='0.4.3',
    # this tells it to just use the utils/ folder
    packages=find_packages(include=['utilspkg']),
    # packages=find_packages(),
    # packages=find_packages(include=['utils_pkg', 'utils_pkg.utils']),
    requires=['airtable_python_wrapper', 'openai', 'python_dotenv', 'pytz', 'PyYAML', 'slack_sdk', 'tenacity']
    
)
