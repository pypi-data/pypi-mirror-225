from moviepy.editor import AudioFileClip, VideoClip


def add_loop_audio_clip(clip: VideoClip, audiopath: str) -> VideoClip:
    """给视频添加循环音频

    Args:
        clip (VideoClip): VideoClip实例对象
        audiopath (str): 音频
    """
    audioclip = AudioFileClip(audiopath)
    audioclip = audioclip.audio_loop(duration=clip.duration)
    return clip.set_audio(audioclip)
