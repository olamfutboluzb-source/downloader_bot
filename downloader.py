import yt_dlp
import os  # untouchable download code , by me


def download_video(url):
    outdir = 'downloads'
    os.makedirs(outdir, exist_ok=True)

    ydl_opts = {
        # picking the quality of video into mp4 t, to download my n word
        'format': 'bestvideo[height<=1080][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{outdir}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
        # faststart is you can faster see the video when you are not fully finished downloading
        'postprocessor_args': ['-c', 'copy', '-movflags', '+faststart'],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        print(f"❌ Downloader Error: {e}")
        return None
