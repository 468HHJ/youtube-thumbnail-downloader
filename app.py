from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    thumbnails = None
    video_title = None
    mp4_link = None
    mp3_link = None

    if request.method == "POST":
        url = request.form.get("url")

        # Thumbnail logic (as before)
        # ...

        try:
            yt = YouTube(url)
            video_title = yt.title.replace("/", "_")  # filename safe

            # MP4 download
            stream_mp4 = yt.streams.get_highest_resolution()
            mp4_path = os.path.join(DOWNLOAD_FOLDER, f"{video_title}.mp4")
            if not os.path.exists(mp4_path):
                stream_mp4.download(output_path=DOWNLOAD_FOLDER, filename=f"{video_title}.mp4")
            mp4_link = f"/download/{video_title}.mp4"

            # MP3 download
            stream_audio = yt.streams.filter(only_audio=True).first()
            mp3_path = os.path.join(DOWNLOAD_FOLDER, f"{video_title}.mp3")
            if not os.path.exists(mp3_path):
                # Download audio
                temp_audio = stream_audio.download(output_path=DOWNLOAD_FOLDER, filename="temp_audio")
                # Convert to mp3 using ffmpeg (optional)
                try:
                    from moviepy.editor import AudioFileClip
                    audio_clip = AudioFileClip(temp_audio)
                    audio_clip.write_audiofile(mp3_path)
                    audio_clip.close()
                    os.remove(temp_audio)
                except:
                    # fallback if moviepy not installed
                    os.rename(temp_audio, mp3_path)

            mp3_link = f"/download/{video_title}.mp3"

        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("index.html", thumbnails=thumbnails, error=error,
                           video_title=video_title, mp4_link=mp4_link, mp3_link=mp3_link)

@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
