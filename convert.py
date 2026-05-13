from pathlib import Path
import subprocess

NAS_PATH = Path('Z:/Movies')

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

def convert(input_file, output_file):
    try:
        subprocess.run(
            ['ffmpeg', '-i', str(input_file), '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', str(output_file)],
            check=True
        )
        print(f"Converted {input_file} to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file}: {e}")

def main():
    mp4_hevc_files = [file.name for file in NAS_PATH.rglob('*.mp4') if is_hevc(file)]
    print(mp4_hevc_files)
    print(len(mp4_hevc_files))

if __name__ == '__main__':
    main()