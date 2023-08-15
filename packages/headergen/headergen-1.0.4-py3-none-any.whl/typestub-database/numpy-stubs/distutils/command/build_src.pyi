from distutils.command import build_ext
from numpy.distutils import log as log
from numpy.distutils.misc_util import appendpath as appendpath, fortran_ext_match as fortran_ext_match, get_cmd as get_cmd, is_sequence as is_sequence, is_string as is_string
from typing import Any

def subst_vars(target, source, d) -> None: ...

class build_src(build_ext.build_ext):
    description: str
    user_options: Any
    boolean_options: Any
    help_options: Any
    extensions: Any
    package: Any
    py_modules: Any
    py_modules_dict: Any
    build_src: Any
    build_lib: Any
    build_base: Any
    force: Any
    inplace: Any
    package_dir: Any
    f2pyflags: Any
    f2py_opts: Any
    swigflags: Any
    swig_opts: Any
    swig_cpp: Any
    swig: Any
    verbose_cfg: Any
    def initialize_options(self) -> None: ...
    libraries: Any
    data_files: Any
    def finalize_options(self) -> None: ...
    def run(self) -> None: ...
    get_package_dir: Any
    def build_sources(self) -> None: ...
    def build_data_files_sources(self) -> None: ...
    def build_npy_pkg_config(self) -> None: ...
    def build_py_modules_sources(self) -> None: ...
    def build_library_sources(self, lib_name, build_info) -> None: ...
    ext_target_dir: Any
    def build_extension_sources(self, ext) -> None: ...
    def generate_sources(self, sources, extension): ...
    def filter_py_files(self, sources): ...
    def filter_h_files(self, sources): ...
    def filter_files(self, sources, exts=...): ...
    def template_sources(self, sources, extension): ...
    def pyrex_sources(self, sources, extension): ...
    def generate_a_pyrex_source(self, base, ext_name, source, extension): ...
    def f2py_sources(self, sources, extension): ...
    def swig_sources(self, sources, extension): ...

def get_swig_target(source): ...
def get_swig_modulename(source): ...
def get_f2py_modulename(source): ...
