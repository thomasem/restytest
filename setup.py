from distutils import core
import os
from pip import req
import setuptools


# What on earth is this?! (I think it's leftover from an initial and abandoned implementation)
requirements_path = os.path.join
requirements = [
    str(r.req) for r in req.parse_requirements('./requirements.txt',
                                               session=False)
]

core.setup(
    name='RestyTest',
    version='0.1.0',
    description="Example REST application exposing the relationship between"
                " Users and Groups.",
    author='Thomas Maddox',
    author_email='thomas.e.maddox@gmail.com',
    license="GPLv3",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
    ],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'restytest = restytest.api.app:serve'
        ]
    }
)
