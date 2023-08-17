# Copyright 2022 by Au-Zone Technologies.  All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
#
# This source code is provided solely for runtime interpretation by Python.
# Modifying or copying any source code is explicitly forbidden.

from enum import Enum


class CameraType(Enum):
    Image = 0
    Video = 1
    Stream = 2


class Camera:
    def __init__(self, source, source_type, width=None, height=None):
        self.source = source
        self.source_type = source_type
        self.video_capture = None
        self.image_index = -1
        self.width = width
        self.height = height

        if isinstance(self.source, str) and \
                self.source_type == CameraType.Image:
            self.source = [self.source]

    def __iter__(self):
        import cv2

        if self.source_type in [CameraType.Video, CameraType.Stream]:
            self.video_capture = cv2.VideoCapture(self.source)
            if self.width is not None:
                self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            if self.height is not None:
                self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        return self

    def __next__(self):
        import cv2
        if self.source_type == CameraType.Image:
            self.image_index += 1
            if self.image_index >= len(self.source):
                raise StopIteration
            frame = cv2.imread(self.source[self.image_index])
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            return frame

        else:
            ret, frame = self.video_capture.read()
            if not ret:
                raise StopIteration
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            return frame
