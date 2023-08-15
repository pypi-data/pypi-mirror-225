from typing import List
from moviepy.editor import VideoClip


def split_clip(clip: VideoClip, num: int) -> List[VideoClip]:
    """分割视频

    Args:
        clip (VideoClip): 实例对象
        num (int): 分割数量

    Returns:
        List[VideoClip]: [clip1, clip2, ...] 数量为 num
    """
    start = 0
    subclip_duration = int(clip.duration) // num
    clips = []
    for i in range(num):
        end = start + subclip_duration
        clips.append(clip.subclip(t_start=start, t_end=end))
        start = end
    return clips
