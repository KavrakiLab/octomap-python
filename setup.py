import subprocess

import numpy
from Cython.Distutils import build_ext
from setuptools import Extension, setup


def get_long_description():
    with open('README.md') as f:
        long_description = f.read()
    return long_description


subprocess.run(
    [
        'cmake',
        '-Bbuild',
        '-DBUILD_OCTOVIS_SUBPROJECT=OFF',
        '-DCMAKE_CXX_FLAGS="-w"',
        '.',
        ],
    cwd = 'src/octomap',
    check = True
    )

subprocess.run(['cmake', '--build', 'build/'], cwd = 'src/octomap', check = True)

ext_modules = [
    Extension(
        'octomap', ['octomap/octomap.pyx'],
        include_dirs = [
            'src/octomap/octomap/include', 'src/octomap/dynamicEDT3D/include', numpy.get_include()
            ],
        language = 'c++',
        extra_objects = [
            "src/octomap/lib/libdynamicedt3d.a",
            "src/octomap/lib/liboctomap.a",
            "src/octomap/lib/liboctomath.a"
            ]
        )
    ]

setup(
    name = 'octomap-python',
    version = '1.9.8',
    install_requires = ['numpy'],
    extras_require = {
        'example': ['glooey', 'imgviz', 'pyglet', 'trimesh[easy]'],
        },
    license = 'BSD',
    maintainer = 'Zachary Kingston',
    maintainer_email = 'zak@rice.edu',
    url = 'https://github.com/zkingston/octomap-python',
    ext_modules = ext_modules,
    cmdclass = {'build_ext': build_ext},
    )
