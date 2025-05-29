import asyncio
import pathlib
import os
from speed_changer import config
from speed_changer.speed import Speed
from speed_changer.mp3_speed_changer import MP3SpeedChanger


async def main():
    """速度変更処理のメイン関数"""
    print("速度変更処理を開始します。")
    print("準備中...")

    # targetディレクトリからファイルを読み込む(mp3, mp4)
    input_files = pathlib.Path(config.INPUT_DIR).glob("*.mp3")

    # 入力ファイルが存在するかチェック
    input_files = list(input_files)
    if not input_files:
        print(
            f"警告: inputディレクトリ内にMP3ファイルが見つかりません。: {config.INPUT_DIR}"
        )
        return

    # 速度を変更する
    speed_changer = MP3SpeedChanger(Speed(config.SPEED))

    completed = 0

    def on_success(output: str):
        nonlocal completed
        completed += 1
        print(f"進捗: {completed}/{total}, ファイル: {output}")

    def on_error(error: Exception, input_file: str):
        print(f"進捗: {completed}/{total}, ファイル: {input_file}, エラー: {error}")

    tasks = []
    # 各ファイルの処理を非同期タスクとして追加
    for input_file in input_files:
        output_dir = config.OUTPUT_DIR
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(output_dir, exist_ok=True)

        # 拡張子なしのファイル名を取得
        basename = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f"{basename}_{config.SPEED}x.mp3")

        if os.path.exists(output_file):
            print(f"スキップ: 出力ファイル {output_file} は既に存在します。")
            continue

        # 速度変更処理を非同期タスクとして追加
        tasks.append(
            asyncio.create_task(
                speed_changer.change_speed(
                    input_file, output_file, on_success, on_error
                )
            )
        )
    total = len(tasks)

    # 全てのタスクを実行
    _ = await asyncio.gather(*tasks)
    print("全ての処理が完了しました。")


if __name__ == "__main__":
    asyncio.run(main())
