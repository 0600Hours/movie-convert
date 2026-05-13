from pathlib import Path
import subprocess
import sys

def is_hevc(file_path):
    try:
        codec = subprocess.check_output(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', str(file_path)],
            text=True
        )
        return codec.strip() == 'hevc'
    except Exception as e:
        print(f"Error checking codec for {file_path}: {e}")
        return False

def convert(input_file):
    try:
        output_file = input_file.with_suffix('.mkv')
        subprocess.run(
            ['ffmpeg', '-i', str(input_file), '-map', '0', '-c', 'copy', str(output_file)],
            stdout=subprocess.DEVNULL,
            check=True
        )
        print(f"Converted {input_file} to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file}: {e}")

def main(args):
    path = Path(args[0] if args else '.')
    print(f"Scanning for mp4 files in {path}...")
    mp4_files = [file for file in path.rglob('*.mp4')]
    hevc_files = [file for file in mp4_files if is_hevc(file)]
    print(f"Found {len(mp4_files)} mp4 files, {len(hevc_files)} of which are hevc.")
    # for hevc_file in hevc_files:
    #     output_file = hevc_file.with_suffix('.converted.mp4')
    #     convert(hevc_file, output_file)\
    first = hevc_files[0] if hevc_files else None
    print(first.name)
    convert(first)

if __name__ == '__main__':
    main(sys.argv[1:])