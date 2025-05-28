import asyncio
import pathlib
import os
from speed_changer import config
from speed_changer.speed import Speed
from speed_changer.mp3_speed_changer import MP3SpeedChanger


async def main():
    """速度変更処理のメイン関数"""
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

    # 処理対象のファイル数を表示
    print(f"{len(input_files)}個のファイルを処理します...")

    tasks = []
    # 各ファイルの処理を非同期タスクとして追加
    for input_file in input_files:
        print(f"{input_file}の処理を開始...")
        output_dir = config.OUTPUT_DIR
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(output_dir, exist_ok=True)

        # 拡張子なしのファイル名を取得
        basename = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f"{basename}_{config.SPEED}x.mp3")

        # 速度変更処理を非同期タスクとして追加
        tasks.append(
            asyncio.create_task(speed_changer.change_speed(input_file, output_file))
        )
        print(f"{input_file}の処理が完了しました。出力先: {output_file}")

    # 全てのタスクを実行
    await asyncio.gather(*tasks)
    print("全ての処理が完了しました。")


if __name__ == "__main__":
    asyncio.run(main())
