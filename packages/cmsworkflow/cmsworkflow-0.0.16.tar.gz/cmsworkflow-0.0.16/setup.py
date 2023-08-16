from setuptools import setup, find_packages


setup(
    name='cmsworkflow',
    author="Hasan Ozturk, Hamed Bakhshiansohi, Luca Lavezzo",
    version='0.0.16',
    description="A high level package which provides tools to get useful information about CMS workflows",
    url="https://github.com/pypa/sampleproject",
    python_requires=">=3.6",
    packages=find_packages(include=['workflow', 'workflow.*']), # Include everything under workflow/
    package_data={'workflow': ['conf/serviceConfiguration.json']},  # Include data files
    install_requires=['pip>20.0.0','jira','pandas'],  # Specify required dependencies
)
