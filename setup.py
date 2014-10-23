try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

from distutils.spawn import spawn
from distutils.command.build import build
from distutils.command.build_ext import build_ext
import os
import sys

from llvmlite.utils import get_library_name


here_dir = os.path.dirname(__file__)


class LlvmliteBuild(build):

    def finalize_options(self):
        build.finalize_options(self)
        # The build isn't platform-independent
        if self.build_lib == self.build_purelib:
            self.build_lib = self.build_platlib

    def get_sub_commands(self):
        # Force "build_ext" invocation.
        commands = build.get_sub_commands(self)
        for c in commands:
            if c == 'build_ext':
                return commands
        return ['build_ext'] + commands


class LlvmliteBuildExt(build_ext):

    def run(self):
        build_ext.run(self)
        cmd = [sys.executable, os.path.join(here_dir, 'ffi', 'build.py')]
        spawn(cmd, dry_run=self.dry_run)
        # HACK: this makes sure the library file (which is large) is only
        # included in binary builds, not source builds.
        library_name = get_library_name()
        self.distribution.package_data = {
            "llvmlite.binding": [get_library_name()],
        }


packages = ['llvmlite',
            'llvmlite.binding',
            'llvmlite.llvmpy',
            'llvmlite.tests',
            ]

setup(name='llvmlite',
      description="lightweight wrapper around basic LLVM functionality",
      version="0.1",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
      ],
      # Include the separately-compiled shared library
      author="Continuum Analytics, Inc.",
      author_email="numba-users@continuum.io",
      url="https://github.com/numba/llvmlite",
      packages=packages,
      license="BSD",
      cmdclass={'build': LlvmliteBuild,
                'build_ext': LlvmliteBuildExt,
                },
      )