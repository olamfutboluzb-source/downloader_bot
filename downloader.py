import os
import yt_dlp

def download_video(url):
    outdir = '/tmp/downloads'
    os.makedirs(outdir, exist_ok=True)
    
    # Путь к кукам (должны лежать в корне проекта)
    base_path = os.path.dirname(os.path.abspath(__file__))
    cookies_path = os.path.join(base_path, 'cookies.txt')

    ydl_opts = {
        'cookiefile': cookies_path,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
        'outtmpl': f'{outdir}/%(id)s.%(ext)s', # Используем ID, чтобы не было ошибок в именах
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.youtube.com/',
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"❌ Downloader Error: {e}")
        return None
