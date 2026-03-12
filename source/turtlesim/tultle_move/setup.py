from setuptools import find_packages, setup

package_name = 'tultle_move'

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
    maintainer='weed',
    maintainer_email='weed@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sub_t = tultle_move.subscriber_t:main',
            'pub_t = tultle_move.publisher_t:main',
            'cmd_pose = tultle_move.turtle_cmd_and_pose:main',
            'service_server = tultle_move.service_server:main',
            'dist_action_server = tultle_move.dist_turtle_action_server:main',
            'multi_thread=tultle_move.multi_thread:main'
        ],
    },
)
