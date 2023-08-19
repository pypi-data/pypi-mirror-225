from setuptools import setup
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
from setuptools.command.develop import develop
import shutil
import glob
import sys
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

run_path = r'runtime/bin64'
win_dlls = glob.glob(path.abspath(path.join(run_path, 'pco_f*.dll')))
win_dlls += [
    path.abspath(path.join(run_path, 'pco_recorder.dll')),
    path.abspath(path.join(run_path, 'pco_conv.dll')),
    path.abspath(path.join(run_path, 'sc2_cam.dll')),
    path.abspath(path.join(run_path, 'sc2_clhs.dll')),
    path.abspath(path.join(run_path, 'sc2_genicam.dll')),
    path.abspath(path.join(run_path, 'sc2_gige.dll')),
    path.abspath(path.join(run_path, 'sc2_cl_me4.dll'))
]

linux_so = {}  # major copies
for f in glob.glob(path.abspath(path.join(run_path, "lib*.so.*.*.*"))):
    linux_so.update({f: path.basename(f[:f[:f.rfind('.')].rfind('.')])})

# .so
for f in glob.glob(path.abspath(path.join(run_path, "libpco_f*.so.*.*.*"))):
    if path.basename(f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')]) == 'libpco_file.so':
        continue
    linux_so.update({f: path.basename(f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')])})


package_list = [
    './genicam',
    './LICENSE.txt',
    './license.pdf',
    './license_3rdParty.pdf']
package_list += [path.join('pco', path.basename(i)) for i in win_dlls]
package_list += [path.join('pco', linux_so[i]) for i in linux_so]


class RuntimeInstall(install):
    """Install setup to copy shared libraries"""

    def run(self):
        install.run(self)

        dest_path = path.join(path.abspath(self.root), 'pco')
        for full_lib in linux_so:
            shutil.copy(full_lib, path.abspath(path.join(dest_path, linux_so[full_lib])))

        for file in win_dlls:
            shutil.copy(file, dest_path)
        shutil.copytree(path.abspath(path.join(run_path, 'genicam')), path.abspath(path.join(dest_path, 'genicam')))


class RuntimeDevelop(develop):
    """Install setup to copy shared libraries in local directory """

    def run(self):
        develop.run(self)

        if sys.platform.startswith('win32'):
            run_path = 'C:\\pco_runtime\\bin64'
        elif sys.platform.startswith('linux'):
            run_path = '/opt/pco/pco_runtime/bin64'
        else:
            print("Package not supported on platform " + sys.platform)
            raise SystemError
        win_dlls = []
        win_dlls = glob.glob(path.abspath(path.join(run_path, 'pco_f*.dll')))
        win_dlls += [
            path.abspath(path.join(run_path, 'pco_recorder.dll')),
            path.abspath(path.join(run_path, 'pco_conv.dll')),
            path.abspath(path.join(run_path, 'sc2_cam.dll')),
            path.abspath(path.join(run_path, 'sc2_clhs.dll')),
            path.abspath(path.join(run_path, 'sc2_genicam.dll')),
            path.abspath(path.join(run_path, 'sc2_gige.dll')),
            path.abspath(path.join(run_path, 'sc2_cl_me4.dll'))
        ]

        dest_path = path.join(path.abspath(this_directory), 'pco')

        # .so.<major>
        linux_so = {}
        for f in glob.glob(path.abspath(path.join(run_path, "lib*.so.*.*.*"))):
            linux_so.update({f: path.basename(f[:f[:f.rfind('.')].rfind('.')])})

        # .so
        for f in glob.glob(path.abspath(path.join(run_path, "libpco_f*.so.*.*.*"))):
            if path.basename(f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')]) == 'libpco_file.so':
                continue
            linux_so.update({f: path.basename(f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')])})

        for full_lib in linux_so:
            shutil.copy(full_lib, path.abspath(path.join(dest_path, linux_so[full_lib])))

            # .so.<major>.<minor>.<patch>
            # shutil.copy(full_lib, dest_path)

        for file in win_dlls:
            shutil.copy(file, dest_path)
        shutil.copytree(path.abspath(path.join(run_path, 'genicam')), path.abspath(path.join(dest_path, 'genicam')))


setup(
    name='pco',
    packages=['pco'],
    version='2.0.3',
    license='MIT',

    description='This class provides methods for using pco cameras.',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    author='Excelitas PCO GmbH',
    author_email='support.pco@excelitas.com',
    url='https://www.excelitas.com/de/product/pco-software-development-kits/',

    keywords=[
        'pco',
        'camera',
        'flim',
        'scmos',
        'microscopy'
    ],

    install_requires=[
        'numpy'
    ],
    package_data={
        'pco': package_list
    },

    cmdclass={'install': RuntimeInstall,
              'develop': RuntimeDevelop},

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 8',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',

        'Topic :: Scientific/Engineering'
    ]
)
