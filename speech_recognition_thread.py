from __future__ import division

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
import threading
import time

import message

RATE = 44100
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# [END audio_stream]


class TimeInterrupt(threading.Thread):
    def __init__(self, length, result_text):
        threading.Thread.__init__(self)
        self.length = length
        self.text = result_text
        self.text2 = result_text
    
    def run(self):
        count = 0
        while True:
            if self.text == self.text2:
                count += 1
            else:
                self.text = self.text2
            if count > 1:
                self.length[0] = len(self.text)
                count = 0
            time.sleep(1)   

    def set_text(self, text):
        self.text2 = text


class SpeechRecognitionThread(threading.Thread):
    def __init__(self, message_queue):
        threading.Thread.__init__(self)
        self.message_queue = message_queue
    
    def run(self):
      # See http://g.co/cloud/speech/docs/languages
      # for a list of supported languages.
        while True:
            language_code = 'ko-KR'  # a BCP-47 language tag

            client = speech.SpeechClient()
            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=RATE,
                language_code=language_code)
            streaming_config = types.StreamingRecognitionConfig(
                config=config,
                interim_results=True)

            with MicrophoneStream(RATE, CHUNK) as stream:
                audio_generator = stream.generator()
                requests = (types.StreamingRecognizeRequest(audio_content=content)
                            for content in audio_generator)

                responses = client.streaming_recognize(streaming_config, requests)

                # Now, put the transcription responses to use.
                try:
                    self.__listen_print_loop(responses)
                except:
                    continue

    def __listen_print_loop(self, responses):
        num_chars_printed = [0]
        result_text = ""
        t = TimeInterrupt(num_chars_printed, result_text)
        t.start()
        for response in responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end of the
            # line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed[0] - len(transcript))
              
            result_text = transcript[num_chars_printed[0]:]
            print(result_text)
            if result_text.find("위쪽 불 켜 줘") != -1:
                self.message_queue.put(message.BUTTON_1_TURN_ON)
            elif result_text.find("아래쪽 불 켜 줘") != -1:
                self.message_queue.put(message.BUTTON_2_TURN_ON)
            elif result_text.find("위쪽 불 꺼 줘") != -1:
                self.message_queue.put(message.BUTTON_1_TURN_OFF)
            elif result_text.find("아래쪽 불 꺼 줘") != -1:
                self.message_queue.put(message.BUTTON_2_TURN_OFF)
            

            t.set_text(transcript)

