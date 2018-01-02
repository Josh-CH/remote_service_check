from setuptools import setup, find_packages

setup(name='service_check',
	version='1.0.1',
	description='Wraps around Ansible, and Sqlite to check remote Service statuses',
	author='Luke Pafford',
	author_email='lukepafford@gmail.com',
	license='MIT',
	packages=find_packages(exclude=['test']),
	zip_safe=False,
	install_requires=['colorama', 'ansible'],
	classifiers=[
			'Development Status :: 5 - Production/Stable',
			'Intended Audience :: System Administrators',
			'Environment :: Console',
			'Operating System :: POSIX :: Linux',
			'Programming Language :: Python :: 3',
			'Topic :: System :: Monitoring',
			],
	keywords='ansible sqlite3 monitoring',
	python_requires='>=3',
	package_data={'': ['scripts/*', 'db'] },
	include_package_data=True,
	entry_points={
		'console_scripts': [
				'service_check = service_check.__main__:main'
		]
	}
)
