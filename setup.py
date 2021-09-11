from setuptools import setup, find_packages

setup(
    name='xp_pen_userland_config_util',
    version='0.1.1',
    description='Configuration GUI for xp_pen_userland',
    author='Aren Villanueva',
    author_email='kurikaesu@users.noreply.github.com',
    url='https://github.com/kurikaesu/xp-pen-userland-config-util',
    license='GPLv3',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'gui_scripts': ['xp_pen_userland_config_util=xp_pen_userland_config_util.__main__:main']
    },
    data_files=[
        ('share/applications/', ['config/xp_pen_userland_config_util.desktop'])
    ],
    install_requires=['PyGObject', 'psutil', 'pynput'],
    classifiers=[
        'Development Status :: - 3 Alpha',
        'Programming Language :: Python :: 3'
    ]
)
