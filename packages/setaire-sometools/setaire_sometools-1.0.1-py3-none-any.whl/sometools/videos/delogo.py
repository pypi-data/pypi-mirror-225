'''
 # @ Author: tuweifeng
 # @ Create Time: 2023-03-02 14:57:35
 # @ Modified by: tuweifeng
 # @ Modified time: 2023-03-02 15:00:30
 # @ Description:
 '''

from typing import Tuple
import functools
import numpy as np
import random
import cv2
from moviepy.editor import VideoClip, VideoFileClip
from ..utils.decorator import Command
import logging

logger = logging.getLogger(__name__)


class LogoAreaTooLargeException(Exception):
    pass


def create_filter(img: cv2.Mat, min_rgb: Tuple[int, int, int], max_rgb: Tuple[int, int, int]) -> cv2.Mat:
    """过滤像素

    Args:
        img (cv2.Mat): 3维数组
        min_rgb (Tuple[int, int, int]): 最小rgb
        max_rgb (Tuple[int, int, int]): 最大rgb

    Returns:
        cv2.Mat: 2维数组
    """

    def filter(rgb):
        if np.greater_equal(rgb, min_rgb).all() and np.less_equal(rgb, max_rgb).all():
            return 1
        return 0

    mask = np.apply_along_axis(filter, 2, img).astype(np.uint8)
    return mask


def create_logo_mask(clip: VideoClip, min_rgb: Tuple[int, int, int] = (160, 160, 160), max_rgb: Tuple[int, int, int] = (255, 255, 255), max_logo_area_rate: float = 0.005) -> Tuple[cv2.Mat, int]:
    """生成水印遮罩
        只对静态水印有效

    Args:
        clip (VideoClip): 一个 VideoClip 实例对象
        min_rgb (Tuple[int, int, int], optional): 最小rgb
        max_rgb (Tuple[int, int, int], optional): 最大rgb
        max_logo_area_rate (float, optional): 水印占画面最大比例

    Raises:
        LogoAreaTooLargeException: 水印面积过大时报错

    Returns:
        Tuple[cv2.Mat, int]: 返回遮罩(2维数组)和面积
    """
    end = int(clip.duration)
    mask = np.ones(clip.size[::-1], dtype=np.uint8)

    rate = 1

    seconds = list(range(end+1))
    random.shuffle(seconds)
    for i, second in enumerate(seconds):
        img = clip.get_frame(second)
        mask = mask & create_filter(img, min_rgb, max_rgb)
        rate = mask.sum() / mask.size
        logger.info(f"{i}/{end} logo rate: {rate:.4f}")
        if rate < max_logo_area_rate / 2:
            break

    if rate > max_logo_area_rate:
        raise LogoAreaTooLargeException(
            f"logo {rate:.4f} > {max_logo_area_rate}")

    mask[mask > 0] = 255

    # 膨胀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.dilate(mask, kernel, iterations=2)
    return mask, rate


def delogo_clip(clip: VideoClip, output_mask: str = None, min_rgb: Tuple[int, int, int] = (160, 160, 160), max_rgb: Tuple[int, int, int] = (255, 255, 255), max_logo_area_rate: float = 0.005) -> VideoClip:
    """去除水印

    Args:
        clip (VideoClip): 一个 VideoClip 实例对象
        output_mask (str, optional): 保存水印遮罩图片的位置, 为空则不保存
        min_rgb (Tuple[int, int, int], optional): 最小rgb
        max_rgb (Tuple[int, int, int], optional): 最大rgb
        max_logo_area_rate (float, optional): 水印占画面最大比例

    Raises:
        LogoAreaTooLargeException: 水印面积过大时报错

    Returns:
        VideoClip: 返回实例对象
    """
    mask, logo_rate = create_logo_mask(
        clip, min_rgb, max_rgb, max_logo_area_rate)

    if output_mask:
        cv2.imwrite(output_mask, mask)

    if logo_rate <= 0:
        return clip

    image_func = functools.partial(
        cv2.inpaint, inpaintMask=mask, inpaintRadius=8, flags=cv2.INPAINT_TELEA)
    return clip.fl_image(image_func=image_func)


@Command
def delogo_video(filepath: str, output: str = None, output_mask: str = None, fps: int = None, min_rgb: str = "160,160,160", max_rgb: str = "255,255,255", max_logo_area_rate: float = 0.005):
    """视频去静态水印

    Args:
        filepath (str): 原始视频
        output (str): 视频保存为该文件, 为空则不保存
        output_mask (str, optional): 保存水印遮罩图片的位置, 为空则不保存
        fps (int, optional): 帧率.
        min_rgb (str, optional): 最小rgb
        max_rgb (str, optional): 最大rgb
        max_logo_area_rate (float, optional): 水印占画面最大比例

    """
    min_rgb = tuple(int(i) for i in min_rgb.split(","))
    max_rgb = tuple(int(i) for i in max_rgb.split(","))
    clip = VideoFileClip(filepath)
    clip = delogo_clip(clip, output_mask, min_rgb, max_rgb, max_logo_area_rate)
    if output:
        clip.write_videofile(output, fps=fps)
