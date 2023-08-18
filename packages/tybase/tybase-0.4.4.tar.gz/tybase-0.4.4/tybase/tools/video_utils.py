import json
import os
import subprocess
import tempfile


def split_video(video_url: str, save_path: str, frames: int):
    """
    from tybase.tools.video_utils import split_video
    将视频拆分成图片帧，并保存到指定的目录。
    :param video_url: 视频url
    :param save_path: 保存的目录
    :param frames: 需要拆分的帧数
    """
    # 使用ffmpeg命令将视频分割成帧
    cmd = f'ffmpeg -i {video_url} -vf fps={frames} {save_path}/frame_%04d.png'
    subprocess.call(cmd, shell=True)

    # 使用ffmpeg命令将视频中的音频分离出来
    cmd = f'ffmpeg -i {video_url} -vn -acodec copy {save_path}/audio.aac'
    subprocess.call(cmd, shell=True)


def get_video_resolution(video_file_path):
    """
    # from tybase.tools.video_utils import get_video_resolution
    # 获取视频的分辨率(本地), 用于视频加水印的时候会用到

    :param video_file_path: 本地的视频的路径
    :return: (width, height)
    """
    command = ["ffprobe",
               "-v", "error",
               "-select_streams", "v:0",
               "-show_entries", "stream=width,height",
               "-of", "json",
               video_file_path]

    output = subprocess.check_output(command).decode("utf-8")
    video_info = json.loads(output)

    width = video_info['streams'][0]['width']
    height = video_info['streams'][0]['height']

    return width, height


def merge_images_and_audio(images_folder: str, audio_path: str, save_path: str, framerate: int = 15) -> str:
    """
    from tybase.tools.video_utils import merge_images_and_audio
        合并图像序列和音频文件以创建视频。

        参数:
            images_folder (str): 存放图像序列的文件夹路径。图像应按照 "frame_%04d.png" 的格式命名。
            audio_path (str): 音频文件的路径。
            save_path (str): 合并后的视频文件的保存路径。
            framerate (int, 可选): 视频的帧率。默认为 30 帧每秒。

        返回:
            str: 合并后的视频文件的路径。

        异常:
            FileNotFoundError: 如果图像文件夹或音频文件不存在。
            Exception: 如果合并过程中发生错误。

        使用示例:
            from tybase.tools.video_utils import merge_images_and_audio
            merge_images_and_audio("user_swapper_face_frames/md5_timestamp", "audio.mp3", "output.mp4", 24)
        """
    # 检查图片所在的文件夹路径
    if not os.path.exists(images_folder):
        raise FileNotFoundError(f"图片文件夹不存在: {images_folder}")

    # 检查音频文件的路径
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")

    # 确定图片的命名模式
    images_pattern = os.path.join(images_folder, "frame_%04d.png")

    # 创建ffmpeg命令
    cmd = [
        "ffmpeg",
        "-framerate", str(framerate),  # 输入的帧率
        "-i", images_pattern,
        "-i", audio_path,
        "-c:v", "libx264",
        "-r", str(framerate),  # 输出的帧率
        "-strict", "experimental",
        save_path
    ]

    # 执行ffmpeg命令
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 检查命令是否成功执行
    if result.returncode != 0:
        raise Exception(f"合并视频和音频时出错: {result.stderr.decode('utf-8')}")

    return save_path


def get_frame_rate(video_path):
    cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 {video_path}'
    frame_rate_str = subprocess.getoutput(cmd).strip()
    numerator, denominator = map(int, frame_rate_str.split('/'))
    return numerator / denominator


def convert_and_split_video(video_url: str, target_frame_rate: int, save_path: str, frame_name: str = "frame_%04d.png",
                            qv: int = 5):
    """
    from tybase.tools.video_utils import convert_and_split_video

    convert_and_split_video(
        "https://ty-huanlian.oss-cn-shanghai.aliyuncs.com/videos/20230628/74011b30c0cd50cd4a7dd1fa29a6368f_final.mp4",
        15,
        save_path="/root/autodl-tmp/roopapi/res"
    )
    转换并拆分视频为指定帧率的图片帧和音频文件。

    :param video_url: 视频文件的路径或URL。可以是本地文件路径，也可以是远程URL。
    :param target_frame_rate: 目标帧率。如果视频的当前帧率与目标帧率不同，将会转换视频的帧率。
    :param save_path: 图片帧和音频文件的保存目录。函数会确保该目录存在。
    :param frame_name: 图片帧的命名模式。默认为 "frame_%04d.png"。
    :param qv: 图片帧的质量。默认为 5。 0-31，值越小，图片质量越高。
    :return: 保存目录的路径。包含已拆分的图片帧和音频文件。

    """
    # 确保保存路径存在
    os.makedirs(save_path, exist_ok=True)

    # 获取视频的当前帧率
    current_frame_rate = get_frame_rate(video_url)

    tmp_video_path = None  # 初始化为 None

    # 判断当前帧率是否等于目标帧率
    if current_frame_rate != target_frame_rate:
        print("开始转换帧率,...")
        tmp_video_path = tempfile.mktemp(suffix=".mp4")

        # 使用ffmpeg命令将视频转换到目标帧率
        cmd_convert = f'ffmpeg -i {video_url} -r {target_frame_rate} {tmp_video_path}'
        subprocess.call(cmd_convert, shell=True)

        video_url = tmp_video_path  # 更新视频路径为转换后的视频路径

    # 使用ffmpeg命令将视频分割成帧
    # 如果图片是png,采用下面的这个命令,如果是jpg,则采用另外一套命令
    if frame_name.endswith(".png"):
        cmd_split = f'ffmpeg -i {video_url} -vf fps={target_frame_rate} {save_path}/{frame_name}'
    else:
        # 用 ffmpeg -i input_video.mp4 -vf "fps=1" -q:v 15 out%d.jpg 这个方式
        cmd_split = f'ffmpeg -i {video_url} -vf "fps={target_frame_rate}" -q:v {qv} {save_path}/{frame_name}'
    subprocess.call(cmd_split, shell=True)

    # 使用ffmpeg命令将视频中的音频分离出来
    cmd_audio = f'ffmpeg -i {video_url} -vn -acodec copy {save_path}/audio.aac'
    subprocess.call(cmd_audio, shell=True)

    if tmp_video_path and os.path.exists(tmp_video_path):  # 检查文件是否存在
        os.remove(tmp_video_path)  # 删除临时转换后的视频文件

    return save_path


def synthesize_video(image_directory, audio_path, output_path, frame_rate, crf=20, frame_name="frame_%04d.png"):
    '''
    from tybase.tools.video_utils import synthesize_video

    :param image_directory: 图片帧的目录
    :param audio_path:  音频文件的路径
    :param output_path:  输出视频的路径
    :param frame_rate: 视频的帧率
    :param crf:  视频的质量,最佳是23,18-20是无损的,数字越小,质量越高,但是文件越大
    :param frame_name: 需要合成的图片帧的命名格式
    :return: 视频合成以后的路径
    '''
    # from tybase.tools.video_utils import synthesize_video
    # 构建图像文件路径，按照给定的命名格式
    input_images = image_directory + f'/{frame_name}'

    # 使用 ffmpeg 命令合成视频
    command = ['ffmpeg',
               '-framerate', str(frame_rate),  # 设置帧率
               '-i', input_images,  # 输入图片文件路径
               '-i', audio_path,  # 输入音频文件路径
               '-c:v', 'libx264',  # 视频编码格式
               '-pix_fmt', 'yuv420p',  # 设置像素格式
               '-crf', f'{crf}',  # 设置质量，数字越小质量越高
               '-strict', 'experimental',
               '-y', output_path]  # 输出视频文件路径

    # 执行命令
    subprocess.run(command)
    return output_path
