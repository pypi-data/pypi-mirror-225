import os
from . delogo import delogo_clip
from . audio import add_loop_audio_clip
from .split import split_clip
from moviepy.tools import find_extension
from moviepy.editor import VideoClip


def _gen_temp_audiofile(filename, audio_codec):
    name, _ = os.path.splitext(os.path.basename(filename))
    audio_ext = find_extension(audio_codec)
    temp_audiofile = name + "wvf_snd.%s" % audio_ext
    return temp_audiofile


def my_write_videofile(clip: VideoClip, filename: str, remove_files: tuple = (), **kwargs):
    audio_codec = "aac"
    temp_audiofile = _gen_temp_audiofile(filename, audio_codec)
    all_remove_files = [temp_audiofile, *remove_files]
    kwargs["temp_audiofile"] = temp_audiofile
    kwargs["audio_codec"] = audio_codec
    kwargs["ffmpeg_params"] = [
        "-qscale:v", "2",
        "-qscale:a", "2",
    ]
    kwargs["fps"] = 24
    try:
        clip.write_videofile(filename, **kwargs)
    except Exception as e:
        raise e
    finally:
        for file in all_remove_files:
            if os.path.exists(file):
                os.remove(file)


def patch_moviepy():
    VideoClip.delogo = delogo_clip
    VideoClip.add_loop_audio = add_loop_audio_clip
    VideoClip.my_write_videofile = my_write_videofile
    VideoClip.split = split_clip
