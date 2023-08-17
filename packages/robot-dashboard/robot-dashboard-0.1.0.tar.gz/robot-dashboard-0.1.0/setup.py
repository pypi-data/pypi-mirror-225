from setuptools import setup, find_packages

setup(
    name='robot-dashboard',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'dash',
        'pandas',
        'plotly',
        'beautifulsoup4',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'robot-dashboard = robot_dashboard.app:main'
        ],
    },
)
