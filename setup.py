from setuptools import setup

setup(name='service_check',
	version='1.0.1',
	description='Wraps around Ansible, and Sqlite to check remote Service statuses',
	author='Luke Pafford',
	author_email='lukepafford@gmail.com',
	license='MIT',
	packages=['service_check'],
	zip_safe=False,
	entry_points={
		'console_scripts': [
				'service_check = service_check.__main__:main'
		]
	}
)
