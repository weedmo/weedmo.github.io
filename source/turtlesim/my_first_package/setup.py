from setuptools import find_packages, setup

package_name = 'my_first_package'

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
    maintainer='i',
    maintainer_email='i@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_first_node = my_first_package.my_first_node:main',
            'my_subscriber = my_first_package.my_first_subscriber:main',
            'my_publisher  = my_first_package.my_first_publisher:main',
            'my_temp_sub  = my_first_package.my_second_subscriber:main',
            'my_temp_pub  = my_first_package.my_second_publisher:main'
        ],
    },
)
