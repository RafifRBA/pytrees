from setuptools import find_packages, setup

package_name = 'pytrees_patrol'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='veevry',
    maintainer_email='rafifraihanbahrulalam@mail.ugm.ac.id',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'pytrees_patrol = pytrees_patrol.pytrees_runner:main',
        ],
    },
)
