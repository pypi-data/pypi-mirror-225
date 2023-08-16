from setuptools import setup
setup(name='oyl',version='2.5.5',author='Lin Ouyang',
    packages=["oyl","oyl.nn"], 
    include_package_data=True,
    install_requires=["numpy","matplotlib","pandas","pyshp"]
)
