from pytube import YouTube
import subprocess


def download_by_link(link) -> None:
    yt = YouTube(link)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()  # скачиваем видео
    yt.streams.filter(only_audio=True, file_extension="webm").order_by('abr').desc().first().download()  # скачиваем аудио


def convert_webm_to_wav(input_file, output_file) -> None:
    command = ['ffmpeg', '-i', input_file, output_file]  # здесь для работы нужно установить ffmpeg
    subprocess.run(command)
