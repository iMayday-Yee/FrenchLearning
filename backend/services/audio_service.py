import os

def validate_audio(filepath):
    """验证音频文件有效性"""
    from pydub import AudioSegment
    from pydub.exceptions import CouldntDecodeError

    try:
        audio = AudioSegment.from_file(filepath)
        duration = len(audio) / 1000.0

        if duration < 0.3:
            return False, "音频时长不足"

        if audio.dBFS < -60:
            return False, "音频音量过低"

        return True, "有效"
    except CouldntDecodeError:
        return False, "无法解码音频格式"
    except Exception as e:
        return False, f"检测失败: {str(e)}"