from setuptools import setup

package_name = 'turtlebot4_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('lib/' + package_name, [package_name+'/comunicacion.py']),
        ('lib/' + package_name, [package_name+'/logger.py']),
        ('lib/' + package_name, [package_name+'/protocol.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu20',
    maintainer_email='ubuntu20@todo.todo    ',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_node = turtlebot4_controller.first_node:main",
            "draw_circle = turtlebot4_controller.draw_circle:main",
            "pose_subscriber = turtlebot4_controller.pose_subscriber:main",
            "turtle_controller = turtlebot4_controller.turtle_controller:main",
            "turtle_draw = turtlebot4_controller.turtle_draw:main",
            "server_turtle = turtlebot4_controller.server_turtle:main",
            "turtle_client = turtlebot4_controller.turtle_controller_client:main"
        ],
    },
)
