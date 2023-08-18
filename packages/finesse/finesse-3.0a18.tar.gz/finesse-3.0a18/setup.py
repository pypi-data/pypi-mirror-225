"""Setup file.

This file only contains the setup inforamtion for building Cython extensions. Everything
else is (and should be) in `setup.cfg`. Eventually it should be possible to get rid of
`setup.py` and make the build system entirely declarative (see #367).
"""

import os
import sys
import platform
import tempfile
import subprocess
import shutil
from pathlib import Path
from setuptools import setup
from Cython.Build import build_ext, cythonize
from Cython.Distutils import Extension
from distutils.errors import CompileError

SYS_NAME = platform.system()
NUM_JOBS = int(os.getenv("CPU_COUNT", os.cpu_count()))


def check_cc_compilation(code, include_paths=[], lib_paths=[], libs=[], args=[]):
    fn = lambda x: [x] if type(x) is str else x
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    filename = r"test.c"
    with open(filename, "w") as file:
        file.write(code)
    with open(os.devnull, "w") as fnull:
        args = [
            os.environ.get("CC", "cc"),
            filename,
            *fn(args),
            *("-I" + _ for _ in fn(include_paths)),
            *("-L" + _ for _ in fn(lib_paths)),
            *fn(libs),
        ]
        result = subprocess.call(args, stdout=fnull, stderr=sys.stderr)

    os.chdir(curdir)
    # clean up
    shutil.rmtree(tmpdir)
    return result == 0


def is_openmp_installed(include_paths=[], lib_paths=[], libs=[], args=[]):
    return check_cc_compilation(
        r"""
        #include <omp.h>
        #include <stdio.h>
        int main() {
        #pragma omp parallel
        printf("Hello from thread %d, nthreads %d\n", omp_get_thread_num(), omp_get_num_threads());
        }
        """,
        include_paths,
        lib_paths,
        libs,
        args,
    )


def is_klu_installed(include_paths=[], lib_paths=[], libs=[], args=[]):
    return check_cc_compilation(
        r"""
        #include "klu.h"
        int main() {
            klu_l_common klu;
            klu_l_defaults(&klu);
        }
        """,
        include_paths,
        lib_paths,
        libs,
        args,
    )


def get_conda_paths():
    try:
        library = sys.prefix
        # library = os.environ["CONDA_PREFIX"]
        if sys.platform == "win32":
            library = os.path.join(library, "Library")
        return os.path.join(library, "include"), os.path.join(library, "lib")
    except KeyError:
        return None, None


class finesse_build_ext(build_ext):
    def initialize_options(self):
        super().initialize_options()
        # default to parallel build
        self.parallel = NUM_JOBS


def make_extension(relpath, **kwargs):
    import numpy as np

    here = Path(__file__).parent.absolute()
    src_dir = Path("src")
    finesse_dir = src_dir / "finesse"

    def construct_ext_name(rp):
        names = []
        leading, trailing = os.path.split(rp)

        while trailing != "":
            names.append(trailing)

            leading, trailing = os.path.split(leading)

        names.reverse()
        if names[-1].endswith(".pyx"):
            names[-1] = names[-1].split(".")[0]

        return ".".join(names)

    # The optional arguments consisting of various directories,
    # macros, compilation args, etc. that will be passed to
    # Extension object constructor
    ext_args = {
        "include_dirs": [],
        "define_macros": [],
        "undef_macros": [],
        "library_dirs": [],
        "libraries": [],
        "runtime_library_dirs": [],
        "extra_objects": [],
        "extra_compile_args": [],
        "extra_link_args": [],
        "export_symbols": [],
        "cython_include_dirs": [],
        "cython_directives": [],
    }
    ### Setting up some global options that need to be passed ###
    ###                   to all extensions                   ###

    include_dirs = ext_args.get("include_dirs")
    # Include the src/finesse and NumPy header file directories
    include_dirs.extend([str(here / finesse_dir), np.get_include()])

    if SYS_NAME == "Windows":
        # switch off complex.h usage so we can use msvc's nonsensical complex
        # number implementation
        define_macros = ext_args.get("define_macros")
        define_macros.append(("CYTHON_CCOMPLEX", 0))

        # Try and get suitesparse from conda
        conda_include, conda_lib = get_conda_paths()

        if conda_include is not None:
            CONDA_SUITESPARSE_PATH = os.path.join(conda_include, "suitesparse")
            if os.path.exists(CONDA_SUITESPARSE_PATH):
                include_dirs.append(CONDA_SUITESPARSE_PATH)
            else:
                raise FileNotFoundError(
                    "Could not find suitesparse includes, install using `conda install suitesparse -c conda-forge`"
                )
            include_dirs.append(conda_include)
            ext_args.get("library_dirs").append(conda_lib)
        else:
            # Can try and use a local build, this is something a user will have to
            # fight with themselves for now
            raise NotImplementedError(
                "User specificed Suitesparse installation required"
            )
            # suitesparse = Path("C:\\Users\\a1223695\\git\\vs-suitesparse\\src\\SuiteSparse")
            # include_dirs.append(str(suitesparse / "SuiteSparse_config"))
            # include_dirs.append(str(suitesparse / "KLU" / "Include"))
            # include_dirs.append(str(suitesparse / "AMD" / "Include"))
            # include_dirs.append(str(suitesparse / "COLAMD" / "Include"))
            # include_dirs.append(str(suitesparse / "BTF" / "Include"))

            # library_dirs = ext_args.get("library_dirs")
            # library_dirs.append(
            #     str(Path("C:\\Users\\a1223695\git\\vs-suitesparse\\src\\x64\\Release"))
            # )
    else:
        # Now ensure suitesparse headers get included
        USR_SUITESPARSE_PATH = "/usr/include/suitesparse"
        if os.path.exists(USR_SUITESPARSE_PATH):
            include_dirs.append(USR_SUITESPARSE_PATH)

        # Grab the paths to suitesparse from conda if using this
        conda_include, conda_lib = get_conda_paths()
        if conda_include is not None:
            CONDA_SUITESPARSE_PATH = os.path.join(conda_include, "suitesparse")
            if os.path.exists(CONDA_SUITESPARSE_PATH):
                include_dirs.append(CONDA_SUITESPARSE_PATH)

            include_dirs.append(conda_include)
            ext_args.get("library_dirs").append(conda_lib)

    # define_macros = ext_args.get("define_macros")
    # define_macros.extend(
    #     [
    #         # Stops numpy version warning, cython uses an older API on purpose
    #         ("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION"),
    #     ]
    # )

    extra_compile_args = ext_args.get("extra_compile_args")
    if SYS_NAME != "Windows":
        extra_compile_args.extend(
            [
                "-O3",
                # Inlined cpdef functions in finesse.cymath extensions complain
                # about not being used (they are used outside of these extensions)
                # so we suppress these warnings for the moment
                "-Wno-unused-function",
                "-Wno-unused-variable",
                # "-DCYTHON_WITHOUT_ASSERTIONS",
            ]
        )
    if sys.maxsize > 2**32 and sys.platform == "win32":  # 64-bit windows
        extra_compile_args.append("-DMS_WIN64")

    ### Now adding the optional extra args needed for this specific extension ###

    for arg_opt, arg_list in ext_args.items():
        extra_args = kwargs.get(arg_opt)
        if extra_args:
            if isinstance(extra_args, str):
                extra_args = [extra_args]

            arg_list += extra_args

    ext_name = "finesse." + construct_ext_name(relpath)
    sources = [str(finesse_dir / relpath)]

    return Extension(
        ext_name,
        sources,
        language="c",
        **ext_args,
    )


def osx_openmp_check(open_mp_args, lib):
    conda_include, conda_lib = get_conda_paths()
    open_mp_args["extra_link_args"] = [lib]
    # Using the above, check if openmp is actually available or not
    return is_openmp_installed(
        include_paths=conda_include,
        lib_paths=conda_lib,
        libs=open_mp_args["extra_link_args"],
        args=open_mp_args["extra_compile_args"],
    )


def ext_modules():
    conda_include, conda_lib = get_conda_paths()
    cmatrix_args = {"libraries": "klu"}
    compile_time_env = {"FINESSE3_DISABLE_OPENMP": 0}

    # Argument pattern for extensions requiring OpenMP are annoying
    # various openmp implementations exist. Generally ok on Linux and windows
    # but OSX clang doesn't support openmp out of the box...
    if SYS_NAME == "Darwin":
        FINESSE3_DISABLE_OPENMP = os.environ.get("FINESSE3_DISABLE_OPENMP", 0)

        if FINESSE3_DISABLE_OPENMP == "1":
            open_mp_args = {}  # empty so no openmp linked
            compile_time_env["FINESSE3_DISABLE_OPENMP"] = 1
        else:
            open_mp_args = {"extra_compile_args": ["-Xpreprocessor", "-fopenmp"]}
            # Try both the intel and llvm library, apparently exactly the same
            # apart from one small difference. The osx_openmp_check will update the
            # open_mp_args with the right library value to use
            if not osx_openmp_check(open_mp_args, "-liomp5"):
                if not osx_openmp_check(open_mp_args, "-lomp"):
                    # Empty the openmp compile arugments, this removes the build time
                    # linking to the libomp and allows for OSX to build and run perfectly
                    # fine without any. See issue #450 for some discussions
                    # open_mp_args = {}
                    compile_time_env["FINESSE3_DISABLE_OPENMP"] = 1
                    raise CompileError("OSX OpenMP libraries not found.")

        if not is_klu_installed(
            include_paths=conda_include,
            lib_paths=conda_lib,
            libs="-lklu",
        ):
            raise CompileError("KLU Suitesparse libraries not found.")
    elif SYS_NAME == "Windows":
        open_mp_args = {"extra_compile_args": "/openmp"}
        # No testing for dependencies on Windows for issue #271, msvc is too
        # much of a nusiance to quickly just try and compile from subprocesses
        # will need something like `from distutils.ccompiler import new_compiler`
        # https://github.com/astropy/astropy-helpers/blob/master/astropy_helpers/openmp_helpers.py
    else:
        open_mp_args = {
            "extra_compile_args": "-fopenmp",
            "extra_link_args": "-fopenmp",
        }

        if not is_openmp_installed(
            include_paths=conda_include,
            lib_paths=conda_lib,
            libs=open_mp_args["extra_link_args"],
            args=open_mp_args["extra_compile_args"],
        ):
            raise CompileError("No OpenMP libraries not found.")

        if not is_klu_installed(
            include_paths=[conda_include, "/usr/include/suitesparse"],
            lib_paths=conda_lib,
            libs="-lklu",
        ):
            raise CompileError("KLU Suitesparse libraries not found.")

    # The argument patterns that get passed to all extensions
    default_ext_args = {}

    # See https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#compiler-directives
    # for in-depth details on the options for compiler directives
    compiler_directives = {
        # Embeds call signature in docstring of Python visible functions
        "embedsignature": True,
        # No checks are performed on division by zero (for big perfomance boost)
        "cdivision": True,
    }

    if os.environ.get("CYTHON_COVERAGE", False):
        # If we're in coverage report mode, then add the trace
        # macros to all extensions so that proper line tracing
        # is performed
        default_ext_args["define_macros"] = [
            ("CYTHON_TRACE", "1"),
            ("CYTHON_TRACE_NOGIL", "1"),
        ]

        # Ensure line tracing is switched on for all extensions.
        compiler_directives["linetrace"] = True

    # If debug mode is set then ensure profiling
    # is switched on for all extensions
    if os.environ.get("CYTHON_DEBUG", False):
        compiler_directives["profile"] = True

    # NOTE (sjr) Pass any extra arguments that a specific extension needs via a
    #            dict of the arg names: values here. See ext_args in make_extension
    #            function above for the options.
    ext_args = [
        ("enums.pyx", default_ext_args),
        ("cymath/*.pyx", {**default_ext_args, **open_mp_args}),
        ("thermal/*.pyx", default_ext_args),
        ("tree.pyx", default_ext_args),
        ("materials.pyx", default_ext_args),
        ("constants.pyx", default_ext_args),
        ("frequency.pyx", default_ext_args),
        # ("symbols.pyx", default_ext_args),
        ("parameter.pyx", default_ext_args),
        ("cyexpr.pyx", default_ext_args),
        ("element.pyx", default_ext_args),
        ("cmatrix.pyx", {**default_ext_args, **cmatrix_args}),
        ("knm/*.pyx", {**default_ext_args, **open_mp_args}),
        ("simulations/base.pyx", default_ext_args),
        ("simulations/basematrix.pyx", default_ext_args),
        ("simulations/KLU.pyx", default_ext_args),
        ("components/workspace.pyx", default_ext_args),
        ("components/mechanical.pyx", default_ext_args),
        ("components/modal/*.pyx", default_ext_args),
        ("detectors/workspace.pyx", default_ext_args),
        ("detectors/compute/amplitude.pyx", default_ext_args),
        ("detectors/compute/camera.pyx", {**default_ext_args, **open_mp_args}),
        ("detectors/compute/power.pyx", {**default_ext_args, **open_mp_args}),
        ("detectors/compute/quantum.pyx", default_ext_args),
        ("detectors/compute/gaussian.pyx", default_ext_args),
        ("tracing/*.pyx", default_ext_args),
        ("analysis/runners.pyx", default_ext_args),
        ("solutions/base.pyx", default_ext_args),
        ("solutions/array.pyx", default_ext_args),
        ("utilities/cyomp.pyx", {**default_ext_args, **open_mp_args}),
    ]

    exts = []
    for ext_rel_path, args in ext_args:
        exts.append(make_extension(os.path.normpath(ext_rel_path), **args))

    return cythonize(
        exts,
        # Produces HTML files showing level of CPython interaction
        # per-line of each Cython extension (.pyx) file
        annotate=False,
        language_level=3,
        nthreads=NUM_JOBS,
        compiler_directives=compiler_directives,
        gdb_debug=False,
        compile_time_env=compile_time_env,
    )


if __name__ == "__main__":
    setup(
        ext_modules=ext_modules(),
        cmdclass={"build_ext": finesse_build_ext},
        use_scm_version=True,
        setup_requires=["setuptools_scm"],
    )
