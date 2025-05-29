import asyncio
from asyncio import subprocess
import os
from typing import Callable
from pydub import AudioSegment

from speed_changer import config
from speed_changer.speed import Speed


class MP3SpeedChanger:
    def __init__(self, speed: Speed):
        self.speed = speed

    async def change_speed(
        self,
        input_file,
        output_file,
        on_success: Callable[[str], None],
        on_error: Callable[[Exception, str], None],
    ):
        # 中間ファイル名（WAV）
        tmp_wav = os.path.join(
            config.TMP_DIR, f"{os.path.splitext(os.path.basename(input_file))[0]}.wav"
        )
        try:

            # MP3 → WAV に変換（非同期化）
            def convert_to_wav():
                sound = AudioSegment.from_file(input_file)
                sound.export(tmp_wav, format="wav")

            await asyncio.to_thread(convert_to_wav)

            # ffmpeg コマンド実行
            process = await asyncio.create_subprocess_exec(
                "ffmpeg",
                "-y",
                "-i",
                tmp_wav,
                "-filter:a",
                str(self.speed),
                output_file,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            await process.wait()

            # 中間ファイル削除
            os.remove(tmp_wav)

            # 成功時のコールバック
            on_success(output_file)

        except Exception as e:
            # エラー時のコールバック
            on_error(e, input_file)
        finally:
            # 中間ファイルが存在する場合は削除
            if os.path.exists(tmp_wav):
                os.remove(tmp_wav)
