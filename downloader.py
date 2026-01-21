import os
import yt_dlp

def download_video(url):
    outdir = 'downloads'
    os.makedirs(outdir, exist_ok=True)

    # Важно: ydl_opts должен быть внутри функции с правильным отступом!
    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
        'outtmpl': f'{outdir}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'addmetadata': True,
        
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.youtube.com/', # Добавили, чтобы YouTube не злился
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['web'], 
                'skip': ['dash', 'hls']
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
