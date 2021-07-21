import hashlib

from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips

def to_video(script):
    clips = []
    hash_object = hashlib.sha256()
    for shot in script:
        hash_object.update(shot.audio_filename.encode('utf-8'))
        audioclip = AudioFileClip(shot.audio_filename)
        image_clip = ImageClip(
            img=shot.image_filename,
            duration=audioclip.duration)
        image_clip.audio = audioclip
        clips.append(image_clip)
    videoclip = concatenate_videoclips(clips)
    filename = "/tmp/{0}.mp4".format(hash_object.hexdigest())
    videoclip.write_videofile(filename, fps=15)
    return filename
