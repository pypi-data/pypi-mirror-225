# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from ctypes import \
    cast, c_void_p, c_int, c_int32, c_uint32, c_float, c_size_t, \
    create_string_buffer, byref
from deepview.vaal.library import VAALBox, VAALKeypoint, VAALEuler, \
    lib, strerror, Type, ModelType
from enum import Enum


class Context:
    """
    DeepView VAAL Context is used to manage DeepViewRT models with VisionPack.
    """

    def __init__(self, engine="npu", model_type=ModelType.NONE):
        if model_type != ModelType.NONE:
            c_model_type = c_uint32(model_type.value)
            self._handle = lib.vaal_model_probe(
                engine.encode('utf-8'), c_model_type)
        else:
            self._handle = lib.vaal_context_create(engine.encode('utf-8'))

    def __del__(self):
        if self._handle is not None:
            lib.vaal_context_release(self._handle)
            self._handle = None

    def __getitem__(self, key):
        t = self.parameter_type(key)

        if t is Type.STR:
            sz = c_size_t()
            err = lib.vaal_parameter_gets(
                self._handle, key.encode('utf-8'), None, 0, byref(sz))
            if err != 0:
                raise KeyError(
                    'failed to get value for parameter %s: %s' %
                    (key, strerror(err)))
            if sz.value == 0:
                return ''
            v = create_string_buffer(b'\000' * sz.value)
            err = lib.vaa_parameter_gets(
                self._handle, key.encode('utf-8'), v, len(v), None)
            if err != 0:
                raise KeyError(
                    'failed to get value for parameter %s: %s' %
                    (key, strerror(err)))
            return v.value.decode('utf-8')
        elif t is Type.U32:
            sz = c_size_t(1)
            v = c_uint32()
            err = lib.vaal_parameter_getu(
                self._handle, key.encode('utf-8'), byref(v), sz, None)
            if err != 0:
                raise KeyError(
                    'failed to get value for parameter %s: %s' %
                    (key, strerror(err)))
            return v.value
        elif t is Type.I32:
            sz = c_size_t(1)
            v = c_uint32()
            err = lib.vaal_parameter_getu(
                self._handle, key.encode('utf-8'), byref(v), sz, None)
            if err != 0:
                raise KeyError(
                    'failed to get value for parameter %s: %s' %
                    (key, strerror(err)))
            return v.value
        elif t is Type.F32:
            sz = c_size_t(1)
            v = c_float()
            err = lib.vaal_parameter_getf(
                self._handle, key.encode('utf-8'), byref(v), sz, None)
            if err != 0:
                raise KeyError(
                    'failed to get value for parameter %s: %s' %
                    (key, strerror(err)))
            return v.value
        raise TypeError('parameter %s has unsupported type: %s' % (key, t))

    def __setitem__(self, key, value):
        if isinstance(value, str):
            err = lib.vaal_parameter_sets(
                self._handle, key.encode('utf-8'), value.encode('utf-8'), 0)
            if err != 0:
                raise RuntimeError(
                    'failed to set parameter %s: %s' % (key, strerror(err)))
        elif isinstance(value, int):
            err = lib.vaal_parameter_seti(
                self._handle, key.encode('utf-8'), c_int32(value), 1)
            if err != 0:
                raise RuntimeError(
                    'failed to set parameter %s: %s' % (key, strerror(err)))
        elif isinstance(value, Enum):
            err = lib.vaal_parameter_seti(
                self._handle, key.encode('utf-8'), c_int32(value.value), 1)
            if err != 0:
                raise RuntimeError(
                    'failed to set parameter %s: %s' % (key, strerror(err)))
        elif isinstance(value, float):
            err = lib.vaal_parameter_setf(
                self._handle, key.encode('utf-8'), c_float(value), 1)
            if err != 0:
                raise RuntimeError(
                    'failed to set parameter %s: %s' % (key, strerror(err)))
        else:
            raise TypeError(
                'unsupported parameter value type: %s' % type(value))

    def parameter_type(self, key):
        t = c_int()

        err = lib.vaal_parameter_info(
            self._handle, key.encode('utf-8'), byref(t), None, None)
        if err != 0:
            raise KeyError('parameter %s not found: %s' % (key, strerror(err)))

        return Type(t.value)

    @property
    def device(self):
        v = create_string_buffer(b'\000' * 5)
        err = lib.vaal_parameter_gets(
            self._handle, b'device', v, len(v), None)
        if err != 0:
            raise RuntimeError(
                'Failed to set context device: %s' % strerror(err))
        return v.value.decode('utf-8')

    @property
    def parameters(self):
        params = []
        name = create_string_buffer(b'\000' * 1024)
        for index in range(lib.vaal_parameter_count(self._handle)):
            size = c_size_t()

            if lib.vaal_parameter_name(
                    self._handle, index, name, len(name), byref(size)) != 0:
                continue

            if len(name) < size.value:
                name = create_string_buffer(b'\000' * size * 2)
                if lib.vaal_parameter_name(
                        self._handle, index, name, len(name), byref(size)) != 0:
                    continue

            params.append(name.value.decode('utf-8'))
        return params

    @property
    def labels(self):
        n_labels = self['label_count']
        if n_labels == 0:
            return []
        return [self.label(i) for i in range(n_labels)]

    @property
    def outputs(self):
        i = 0
        outputs = []
        while True:
            res = self.output(index=i)
            if res is not None:
                outputs.append(res)
                i += 1
            else:
                break
        return outputs

    def label(self, index, nofail=True):
        lbl = lib.vaal_label(self._handle, index)
        lbl = lbl.decode('utf-8') if lbl is not None else ''
        if lbl == '':
            if nofail:
                return str(index)
            else:
                raise ValueError('no label at index %d' % index)
        return lbl

    def tensor(self, name):
        try:
            ptr = lib.vaal_get_tensor_by_name(
                self._handle, name.encode('utf-8'))
        except Exception:
            raise ValueError("Unable to find tensor with name: %s" % name)
        if ptr is not None:
            from deepview.rt import Tensor, ffi
            return Tensor(wrap=ffi.cast('void*', ptr))
        return None

    def output(self, name=None, index=-1):
        if name is not None:
            return self.tensor(name)

        if index >= 0:
            ptr = lib.vaal_output_tensor(self._handle, index)
            if ptr is not None:
                from deepview.rt import Tensor, ffi
                return Tensor(wrap=ffi.cast('void*', ptr))
        return None

    def load_model(self, model):
        if isinstance(model, str):
            err = lib.vaal_load_model_file(self._handle, model.encode('utf-8'))
            if err != 0:
                raise RuntimeError('failed to load model: %s' % strerror(err))
        else:
            raise RuntimeError('load_model from memory currently unsupported')

    def unload_model(self):
        err = lib.vaal_unload_model(self._handle)
        if err != 0:
            raise RuntimeError('failed to unload model: %s' % strerror(err))

    def run_model(self):
        err = lib.vaal_run_model(self._handle)
        if err != 0:
            raise RuntimeError('failed to run model: %s' % strerror(err))

    def boxes(self, max_boxes=None):
        if max_boxes is None:
            max_boxes = self['max_detection']

        bxs = (VAALBox * max_boxes)()
        n_bxs = c_size_t()

        err = lib.vaal_boxes(self._handle, byref(bxs), len(bxs), byref(n_bxs))
        if err != 0:
            raise RuntimeError('failed to get boxes: %s' % strerror(err))
        if n_bxs.value > 0:
            return bxs[0:n_bxs.value]
        return []

    def keypoints(self, max_keypoints=None):
        if max_keypoints is None:
            max_keypoints = 30

        keypts = (VAALKeypoint * max_keypoints)()
        n_keypts = c_size_t()

        err = lib.vaal_keypoints(self._handle, byref(
            keypts), len(keypts), byref(n_keypts))
        if err != 0:
            raise RuntimeError('failed to get keypoints: %s' % strerror(err))
        if n_keypts.value > 0:
            return keypts[0:n_keypts.value]
        return []

    def eulers(self, max_eulers=None):
        if max_eulers is None:
            max_eulers = 10

        eulers = (VAALEuler * 1)()
        n_eulers = c_size_t()

        err = lib.vaal_euler(self._handle, byref(eulers), byref(n_eulers))
        if err != 0:
            raise RuntimeError(
                'failed to get euler angles: %s' % strerror(err))
        if n_eulers.value > 0:
            return eulers[0:n_eulers.value]
        return []

    def load_image(self, image, tensor=None, roi=None):
        if tensor is not None:
            import deepview.rt as rt
            tensor_ptr = rt.ffi.cast('intptr_t', tensor.ptr)
            tensor_ptr = cast(int(tensor_ptr), c_void_p)
        else:
            tensor_ptr = None

        c_roi = None
        if roi is not None:
            c_roi = (c_int32 * 4)(*roi)

        if isinstance(image, str):
            err = lib.vaal_load_image_file(
                self._handle, tensor_ptr, image.encode('utf-8'), c_roi, 0)
            if err != 0:
                raise RuntimeError('failed to load image: %s' % strerror(err))
            return
        elif hasattr(image, '__gtype__') and \
                image.__gtype__.name == 'GstSample':
            return self.load_gst_sample(image, tensor, c_roi)
        else:
            import numpy as np
            if isinstance(image, np.ndarray):
                buf = image.ctypes.data_as(c_void_p)
                fourcc = 0
                if len(image.shape) == 3:
                    if image.shape[2] == 4:
                        fourcc = int.from_bytes(
                            bytes('RGBA', 'utf-8'), byteorder='little')
                    elif image.shape[2] == 3:
                        fourcc = int.from_bytes(
                            bytes('RGB', 'utf-8'), byteorder='little')
                elif len(image.shape) == 4:
                    if image.shape[3] == 4:
                        fourcc = int.from_bytes(
                            bytes('RGBA', 'utf-8'), byteorder='little')
                    elif image.shape[3] == 3:
                        fourcc = int.from_bytes(
                            bytes('RGB', 'utf-8'), byteorder='little')
                width = image.shape[1]
                height = image.shape[0]
                err = lib.vaal_load_frame_memory(
                    self._handle, None, buf, fourcc, width, height, c_roi, 0)
                return err
        raise RuntimeError(
            'load_image called with unsupported type', type(image))

    def load_frame(self, width, height, fourcc, dmabuf=None, tensor=None, roi=None):
        if tensor is not None:
            import deepview.rt as rt
            tensor_ptr = rt.ffi.cast('intptr_t', tensor.ptr)
            tensor_ptr = cast(int(tensor_ptr), c_void_p)
        else:
            tensor_ptr = None

        if dmabuf is None:
            raise RuntimeError('load_frame must be called with a valid dmabuf')
        err = lib.vaal_load_frame_dmabuf(
            self._handle, tensor_ptr, dmabuf, fourcc, width, height, roi, 0)
        if err != 0:
            raise RuntimeError('failed to load frame: %s' % strerror(err))

    def load_gst_sample(self, sample, tensor=None, roi=None):
        import gi
        gi.require_version("GstAllocators", "1.0")
        from gi.repository import GstAllocators

        caps = sample.get_caps()

        buffer = sample.get_buffer()
        memory = buffer.get_all_memory()

        if not GstAllocators.is_dmabuf_memory(memory):
            raise RuntimeError('VAAL Requires DMA Buffers')

        dmabuf = GstAllocators.dmabuf_memory_get_fd(memory)

        width = caps.get_structure(0).get_value("width")
        height = caps.get_structure(0).get_value("height")
        format = caps.get_structure(0).get_value("format")
        fourcc = int.from_bytes(bytes(format, 'utf-8'), byteorder='little')

        self.load_frame(width, height, fourcc, dmabuf, tensor, roi)
