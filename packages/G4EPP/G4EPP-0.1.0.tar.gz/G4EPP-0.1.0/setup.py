from setuptools import setup, find_packages

VERSION = '0.1.0' 
DESCRIPTION = 'GEANT4 EPP Simulation wrapper'
LONG_DESCRIPTION = 'Python wrapper to process and plot GEANT4 EPP simulation outputs'

setup(
        name="G4EPP", 
        version=VERSION,
        author="Grant Berland",
        author_email="grant.berland@colorado.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        package_data={'my_pkg':['G4EPP/data/*']},
        include_package_data=True,
        install_requires=["matplotlib", "pandas", "numpy", "scipy", "seaborn", "wget"],  
        keywords=['python', 'EPP'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6'
            ]
)
