# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from ctypes import \
    CDLL, POINTER, Structure, c_size_t, \
    c_void_p, c_char_p, c_float, c_int, \
    c_uint8, c_int32, c_uint32, c_uint64, c_int64
from enum import Enum
from os import environ
from os.path import isdir, join


class Type(Enum):
    RAW = 0
    PTR = 1
    STR = 2
    I8 = 3
    U8 = 4
    I16 = 5
    U16 = 6
    I32 = 7
    U32 = 8
    I64 = 9
    U64 = 10
    F16 = 11
    F32 = 12
    F64 = 13


class ImageProc(Enum):
    RAW = 0
    UNSIGNED_NORM = 1
    WHITENING = 2
    SIGNED_NORM = 4
    IMAGENET = 8
    MIRROR = 0x1000
    FLIP = 0x2000


class ModelType(Enum):
    NONE = 0
    PEOPLE_DETECTION = 10
    FACE_DETECTION = 20
    HEAD_POSE = 30
    HUMAN_POSE = 40


class VAALBox(Structure):
    _fields_ = [('xmin', c_float),
                ('ymin', c_float),
                ('xmax', c_float),
                ('ymax', c_float),
                ('score', c_float),
                ('label', c_int)]


class VAALEuler(Structure):
    _fields_ = [('yaw', c_float),
                ('pitch', c_float),
                ('roll', c_float)]


class VAALKeypoint(Structure):
    _fields_ = [('x', c_float),
                ('y', c_float),
                ('score', c_float)]


def version() -> str:
    """
    Version of the underlying vaal.ext library, the .ext varies across
    platforms.

        * Windows: ``VAAL.dll``
        * Linux: ``libvaal.so``
        * MacOS: ``libvaal.dylib``

    Returns:
        version string as major.minor.patch-extra format.
    """
    string = lib.vaal_version(None, None, None, None)
    return c_char_p(string).value.decode('utf-8')


def strerror(err) -> str:
    """
    Provides the human-readable string representation of the VAALError.

    Returns:
        String for the VAALError code (int).
    """
    string = lib.vaal_strerror(err)
    return c_char_p(string).value.decode('utf-8')


def load_library(libname=None) -> CDLL:
    """
    Internal function used to load and configure the vaal library. This
    function should not be called directly but instead is called automatically
    when the deepview.vaal library is first loaded.

    The environment variable ``VAAL_LIBRARY`` can be used to point to the
    location of ``vaal.dll/dylib/so`` for cases where it cannot be found.

    Note:
        The library is not part of the Python package but is installed
        separately, typically as part of DeepView VisionPack installations.

    Returns:
        A ctypes.CDLL object containing the vaal library.

    Raises:
        :py:class:`EnvironmentError`: if the vaal library cannot be located.
    """
    if 'VAAL_LIBRARY' in environ:
        libname = environ['VAAL_LIBRARY']

    if libname is not None:
        if isdir(libname) and libname.endswith('.framework'):
            return CDLL(
                join(libname, 'Versions', 'Current', 'VAAL'))
        else:
            return CDLL(libname)
    else:
        try:
            return CDLL('VAAL.dll')
        except OSError:
            pass

        try:
            return CDLL('./VAAL.dll')
        except OSError:
            pass

        try:
            return CDLL('libvaal.so')
        except OSError:
            pass

        try:
            return CDLL('libvaal.dylib')
        except OSError:
            pass

    raise EnvironmentError(
        'Unable to load the VAAL library.  Try setting the environment \
         variable VAAL_LIBRARY to the VAAL library.')


def load_symbols(lib: CDLL):
    """
    Loads the symbols from the VAAL library into the `lib` object to be used by
    the various Python API.

    Args:
        lib: Library object returned from :func:`load_library()`
    """
    lib.vaal_version.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
    lib.vaal_version.restype = c_void_p

    lib.vaal_strerror.argtypes = [c_int]
    lib.vaal_strerror.restype = c_void_p

    lib.vaal_type_sizeof.argtypes = [c_uint32]
    lib.vaal_type_sizeof.restype = c_size_t

    lib.vaal_type_name.argtypes = [c_uint32]
    lib.vaal_type_name.restype = c_char_p

    lib.vaal_clock_now.argtypes = None
    lib.vaal_clock_now.restype = c_int64

    lib.vaal_context_create.argtypes = [c_char_p]
    lib.vaal_context_create.restype = c_void_p

    lib.vaal_context_release.argtypes = [c_void_p]
    lib.vaal_context_release.restype = None

    lib.vaal_parameter_count.argtypes = [c_void_p]
    lib.vaal_parameter_count.restype = c_size_t

    lib.vaal_parameter_name.argtypes = [
        c_void_p, c_size_t, c_char_p, c_size_t, POINTER(c_size_t)]
    lib.vaal_parameter_name.restype = c_int

    lib.vaal_parameter_info.argtypes = [
        c_void_p, c_char_p, POINTER(c_int), POINTER(c_size_t), POINTER(c_int)]
    lib.vaal_parameter_info.restype = c_int

    lib.vaal_parameter_gets.argtypes = [
        c_void_p, c_char_p, c_char_p, c_size_t, POINTER(c_size_t)]
    lib.vaal_parameter_gets.restype = c_int

    lib.vaal_parameter_sets.argtypes = [
        c_void_p, c_char_p, c_char_p, c_size_t]
    lib.vaal_parameter_sets.restype = c_int

    lib.vaal_parameter_getf.argtypes = [
        c_void_p, c_char_p, POINTER(c_float), c_size_t, POINTER(c_size_t)]
    lib.vaal_parameter_getf.restype = c_int

    lib.vaal_parameter_setf.argtypes = [
        c_void_p, c_char_p, POINTER(c_float), c_size_t]
    lib.vaal_parameter_setf.restype = c_int

    lib.vaal_parameter_geti.argtypes = [
        c_void_p, c_char_p, POINTER(c_int32), c_size_t, POINTER(c_size_t)]
    lib.vaal_parameter_geti.restype = c_int

    lib.vaal_parameter_seti.argtypes = [
        c_void_p, c_char_p, POINTER(c_int32), c_size_t]
    lib.vaal_parameter_seti.restype = c_int

    lib.vaal_parameter_getu.argtypes = [
        c_void_p, c_char_p, POINTER(c_uint32), c_size_t, POINTER(c_size_t)]
    lib.vaal_parameter_getu.restype = c_int

    lib.vaal_parameter_setu.argtypes = [
        c_void_p, c_char_p, POINTER(c_uint32), c_size_t]
    lib.vaal_parameter_setu.restype = c_int

    lib.vaal_context_deepviewrt.argtypes = [c_void_p]
    lib.vaal_context_deepviewrt.restype = c_void_p

    lib.vaal_load_model_file.argtypes = [c_void_p, c_char_p]
    lib.vaal_load_model_file.restype = c_int

    lib.vaal_load_model.argtypes = [c_void_p, c_size_t, c_void_p]
    lib.vaal_load_model.restype = c_int

    lib.vaal_unload_model.argtypes = [c_void_p]
    lib.vaal_unload_model.restype = c_int

    lib.vaal_run_model.argtypes = [c_void_p]
    lib.vaal_run_model.restype = c_int

    lib.vaal_load_frame_memory.argtypes = [
        c_void_p,
        c_void_p,
        c_void_p,
        c_uint32,
        c_int32,
        c_int32,
        POINTER(c_int32),
        c_uint32]
    lib.vaal_load_frame_memory.restype = c_int

    lib.vaal_load_frame_physical.argtypes = [
        c_void_p,
        c_void_p,
        c_uint64,
        c_uint32,
        c_int32,
        c_int32,
        POINTER(c_int32),
        c_uint32]
    lib.vaal_load_frame_physical.restype = c_int

    lib.vaal_load_frame_dmabuf.argtypes = [
        c_void_p,
        c_void_p,
        c_int,
        c_uint32,
        c_int32,
        c_int32,
        POINTER(c_int32),
        c_uint32]
    lib.vaal_load_frame_dmabuf.restype = c_int

    lib.vaal_load_image.argtypes = [
        c_void_p,
        c_void_p,
        POINTER(c_uint8),
        c_size_t,
        POINTER(c_int32),
        c_uint32]
    lib.vaal_load_image.restype = c_int

    lib.vaal_load_image_file.argtypes = [
        c_void_p,
        c_void_p,
        c_char_p,
        POINTER(c_int32),
        c_uint32]
    lib.vaal_load_image_file.restype = c_int

    lib.vaal_label.argtypes = [c_void_p, c_int]
    lib.vaal_label.restype = c_char_p

    lib.vaal_boxes.argtypes = [c_void_p, c_void_p, c_size_t, POINTER(c_size_t)]
    lib.vaal_boxes.restype = c_int
    lib.vaal_keypoints.argtypes = [
        c_void_p, c_void_p, c_size_t, POINTER(c_size_t)]
    lib.vaal_keypoints.restype = c_int
    lib.vaal_euler.argtypes = [c_void_p, c_void_p, POINTER(c_size_t)]
    lib.vaal_euler.restype = c_int

    lib.vaal_get_tensor_by_name.argtypes = [c_void_p, c_char_p]
    lib.vaal_get_tensor_by_name.restype = c_void_p

    lib.vaal_output_tensor.argtypes = [c_void_p, c_int]
    lib.vaal_output_tensor.restype = c_void_p

    lib.vaal_output_count.argtypes = [c_void_p]
    lib.vaal_output_count.restype = c_int

    lib.vaal_output_name.argtypes = [c_void_p, c_int]
    lib.vaal_output_name.restype = c_char_p

    # model.c Implementations
    lib.vaal_model_probe.argtypes = [c_char_p, c_uint32]
    lib.vaal_model_probe.restype = c_void_p

    lib.vaal_model_path.argtypes = None
    lib.vaal_model_path.restype = c_char_p


if 'lib' not in locals():
    lib = load_library()
    load_symbols(lib)
