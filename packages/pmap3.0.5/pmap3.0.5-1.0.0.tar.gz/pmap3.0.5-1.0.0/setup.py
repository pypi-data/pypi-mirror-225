from setuptools import setup
import os

requirements = []
with open('requirements.txt') as f:
    for line in f:
        splitted = line.split("#")
        stripped = splitted[0].strip()
        if len(stripped) > 0:
            requirements.append(stripped)
setup(
    name='pmap3.0.5',
    version='1.0.0',
    packages=['RAPID', 'RAPID.util', 'RAPID.models', 'RAPID.pointillist', 'RAPID.network', 'RAPID.Impressionist',
              'RAPID.spatialanalysis', 'RAPID.GUI'],
    url='',
    license='GNU 3.0',
    author='Nishant Thakur',
    author_email='nishantthakur7g@gmail.com',
    description='TEST PMAP',
    install_requires=requirements,
    package_data={'RAPID': ['Model/*']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'RAPID=RAPID.Impressionist.runRAPIDzarr:run_rapid',
            'RAPIDG=RAPID.GUI.RAPIDGUI:run_rapid_gui',
            'RAPIDO=RAPID.pointillist.predictobject:RAPIDObject',
            'RAPIDD=RAPID.util.denoise:run_denoise'

        ],
    },
)
