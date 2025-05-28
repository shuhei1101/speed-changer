import os
import subprocess
from pydub import AudioSegment

from speed_changer import config
from speed_changer.speed import Speed


class MP3SpeedChanger:
    def __init__(self, speed: Speed):
        self.speed = speed

    async def change_speed(self, input_file, output_file):
        # 中間ファイル名（WAV）
        tmp_wav = f"{config.TMP_DIR}_tmp.wav"

        # MP3 → WAV に変換
        sound = AudioSegment.from_file(input_file)
        sound.export(tmp_wav, format="wav")

        # ffmpeg コマンド実行
        subprocess.call(
            ["ffmpeg", "-y", "-i", tmp_wav, "-filter:a", str(self.speed), output_file]
        )

        # 中間ファイル削除
        os.remove(tmp_wav)
