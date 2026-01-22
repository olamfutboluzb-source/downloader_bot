import yt_dlp
import os

def download_audio(url):
    outdir = '/tmp/downloads'
    os.makedirs(outdir, exist_ok=True)
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    cookies_path = os.path.join(base_path, 'cookies.txt')

    ydl_opts = {
        'cookiefile': cookies_path,
        'format': 'bestaudio/best',
        'outtmpl': f'{outdir}/%(id)s.%(ext)s', # Используем ID видео
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.youtube.com/',
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            # yt-dlp вернет путь с оригинальным расширением, но ffmpeg сделает .mp3
            final_path = os.path.splitext(file_path)[0] + ".mp3"
            return final_path
    except Exception as e:
        print(f"❌ Audio Error: {e}")
        return None
