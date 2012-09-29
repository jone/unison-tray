from setuptools import setup, find_packages


setup(name='utray',
      version='1.0a1',
      description="Tray icon and fs change dectection for unison.",
      author='Jonas Baumann',
      author_email='jone@jone.ch',
      url='http://github.com/unison-tray',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'watchdog',
        'croniter',
        ],

      entry_points = {
        'console_scripts' : [
            'tray = utray.app:run',
            ]})
