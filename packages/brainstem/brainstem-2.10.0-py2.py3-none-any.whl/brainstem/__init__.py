# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

"""
A Package that enables communication with Acroname Brainstem Modules and
BrainStem networks.


"""
import functools
import os
import struct

from sys import platform as sys_platform
from sys import version_info
from ._brainstem_c import ffi
import platform
import warnings

def BIT(n):
    return 1 << n


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)

    return new_func


if version_info < (3,):
    def b(x):
        return x
else:
    def b(x):
        if isinstance(x, str):
            return x.encode()
        else:
            return x


def str_or_bytes_to_bytearray(data, start_index=None, end_index=None):
    if isinstance(data, str):
        return bytearray(data[start_index:end_index].encode('utf-8'))
    else:
        return bytearray(b(data[start_index:end_index]))



def convert_int_args_to_bytes(args):
    bytes_data = b''
    for arg in args:
        if isinstance(arg, int) and 0 <= arg <= 255:
            bytes_data += struct.pack('B', arg)
        elif isinstance(arg, list) or isinstance(arg, tuple):
            for i in arg:
                if isinstance(i, int) and 0 <= i <= 255:
                    bytes_data += struct.pack('B', i)
                else:
                    raise ValueError('Invalid argument: %s must be int between 0 and 255.' % str(i))
        else:
            raise ValueError('Invalid argument: %s must be int or list/tuple of ints between 0 and 255.' % str(arg))

    return bytes_data


# Initialize the Brainstem C binding in init.
# Then you can import like so; 'from brainstem import _BS_C, ffi'
_Z_C = None
_CZ_C = None
_BS_C = None
arch, plat = platform.architecture()

if sys_platform.startswith('linux'):
    import cffi

    # Load the glibc core libraries for use of dlmopen and dlerror
    # Done at the top level to avoid re-loading glibc on each check
    _ffi_libc = cffi.FFI()
    _ffi_libc.cdef('''
        void *dlmopen (long int __nsid, const char*, int);
        char *dlerror(void);
    ''')

    # Magic behavior when dlopen has None passed to it!
    # If libpath is None, it returns the standard C library (which can be used to access the functions of glibc, on Linux).
    # https://cffi.readthedocs.io/en/latest/cdef.html#ffi-dlopen-loading-libraries-in-abi-mode
    _libc = _ffi_libc.dlopen(None)

    # Helper function to load a library in a temporary namespace to avoid polluting current
    # namespace when checking libraries
    def check_so_file(path):
        _libc.dlerror() # Clear existing dlerrors

        # Try to load the path in a new namespace, which we can discard immediately
        LM_ID_NEWLM = -1
        handle = _libc.dlmopen(LM_ID_NEWLM, path.encode('ascii'), ffi.RTLD_DEEPBIND | ffi.RTLD_LOCAL | ffi.RTLD_LAZY)
        if _libc.dlerror():
            return False
        return True

try:
    # Mac
    if sys_platform.startswith('darwin'):
        _BS_C = ffi.dlopen(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libBrainStem2.dylib'))

    # Windows
    elif sys_platform.startswith('win32'):
        if arch.startswith('32'):
            _Z_C  = ffi.dlopen(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'x86', 'libzmq-v140-mt-4_3_4'))
            _CZ_C = ffi.dlopen(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'x86', 'libczmq'))
            _BS_C = ffi.dlopen(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'x86', 'BrainStem2'))
        else:
            _Z_C  = ffi.dlopen(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'x64', 'libzmq-v140-mt-4_3_4'))
            _CZ_C = ffi.dlopen(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'x64', 'libczmq'))
            _BS_C = ffi.dlopen(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'x64', 'BrainStem2'))

    # Linux... So many Linux's...
    elif sys_platform.startswith('linux'):

        pathList = [os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Linux', 'x86_64',  '22.04', 'libBrainStem2.so'),
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Linux', 'x86_64',  '20.04', 'libBrainStem2.so'),
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Linux', 'x86_64',  '18.04', 'libBrainStem2.so'),
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Linux', 'x86_64',  '16.04', 'libBrainStem2.so'),
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Linux', 'aarch64', '16.04', 'libBrainStem2.so'),
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Linux', 'aarch64', '18.04', 'libBrainStem2.so'),
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Linux', 'aarch64', '20.04', 'libBrainStem2.so'),
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Linux', 'armv7l',  '11.7',  'libBrainStem2.so'),
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Linux', 'i686'  ,  '16.04', 'libBrainStem2.so')]

        for path in pathList:
            try:
                if check_so_file(path):
                    _BS_C = ffi.dlopen(path)
                    break
            except OSError:
                pass
            except Exception as e:
                print("Unexpected error:", e)
                pass

        if _BS_C is None:
            raise ImportError("This platform/architecture not supported.  Please contact Acroname support.")

# This exception is common when installing a whl that was built for a different platform.
# i.e. Installing a Windows compiled whl on a Mac.
# The platform checks above only serve to invoke the correct ffi command. If a whl was
# built for a different platform that means it won't have the correct underlying library.
except OSError:
    raise OSError("This platform/architecture not supported.  Please contact Acroname support.")

# These imports must happen here following the initialization of the CFFI library.
from . import link
from . import discover
from . import stem
from . import defs
from . import version
from . import result


