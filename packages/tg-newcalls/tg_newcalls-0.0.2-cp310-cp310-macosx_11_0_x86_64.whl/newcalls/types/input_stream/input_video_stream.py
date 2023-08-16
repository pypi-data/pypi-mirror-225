from ..py_object import PyObject
from .video_parameters import VideoParameters


class InputVideoStream(PyObject):
    """The raw video stream (RAW_VIDEO) descriptor

    Attributes:
        path (``str``):
            The video file path
        parameters (:obj:`~newcalls.types.VideoParameters()`):
            The video parameters of the stream

    Parameters:
        path (``str``):
            The video file path (RAW_VIDEO format only)
        parameters (:obj:`~newcalls.types.VideoParameters()`):
            The video parameters of the stream, can be used also
            :obj:`~newcalls.types.HighQualityVideo()`,
            :obj:`~newcalls.types.MediumQualityVideo()` or
            :obj:`~newcalls.types.LowQualityVideo()`
    """

    def __init__(
        self,
        path: str,
        parameters: VideoParameters = VideoParameters(),
        header_enabled: bool = False,
    ):
        self.path: str = path
        self.parameters: VideoParameters = parameters
        self.header_enabled: bool = header_enabled
