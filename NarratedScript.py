from google.cloud import texttospeech
import hashlib
import os.path

class NarratedScript:
    def __init__(self, script):
        self.script = script
        self.client = texttospeech.TextToSpeechClient()
    def __iter__(self):
        return self
    def __next__(self):
        scripted_shot = self.script.__next__()
        hash_object = hashlib.sha256(scripted_shot.text.encode('utf-8'))
        filename = "/tmp/{0}.wav".format(hash_object.hexdigest())
        if not os.path.isfile(filename):
            response = self.client.synthesize_speech(
                input=texttospeech.SynthesisInput(text=scripted_shot.text),
                voice=texttospeech.VoiceSelectionParams(
                    language_code="en-US",
                    name="en-US-Wavenet-G"),
                audio_config=texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                    pitch=0,
                    speaking_rate= 1),
            )
            with open(filename, 'wb') as f:
                f.write(response.audio_content)
        scripted_shot.audio_filename = filename
        return scripted_shot