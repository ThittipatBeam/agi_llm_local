from module.receive_voice import receive_message
from module.converter_2 import convert_mp3_to_pcm
import time
import aiohttp
import asyncio
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import wave
import logging
import io

# from pythaiasr import asr


logging.basicConfig(
    filename='audio_playback.log', 
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s'  
)

audio_path = "voice/pcm/audio.pcm"
api_url = "https://api-dev.siam.ai"
# input_audio_path = "./voice/input.mp3"
input_audio_path = "./voice/audio.pcm"


def save_audio_to_file_mp3(audio_data, output_path):
    """Save audio data to an MP3 file asynchronously."""
    with open(output_path, 'wb') as fd:
        fd.write(audio_data)
    print(f"write {output_path} completed")


def play_audio(audio_data):
    """Play audio data asynchronously."""
    # PCM specific parameters
    sample_width = 2
    frame_rate = 16000
    channels = 1

    # Load the raw PCM audio data into an AudioSegment
    audio = AudioSegment.from_file(
        BytesIO(audio_data),
        format="mp3",
        sample_width=sample_width,
        frame_rate=frame_rate,
        channels=channels
    )

    play(audio)
    logging.info("Audio played successfully.")
    print("Audio played successfully.")


async def main():
    while True:
        if receive_message():
            st = time.time()


#------------------------------ Speech to speech ---------------------------------------------------------------------------------------------------

            async with aiohttp.ClientSession() as session:
                 audio_file = open(input_audio_path, "rb")
                 with open(input_audio_path, "rb") as audio_file:
                        files = {"file": audio_file,
                                # "model": "nemotron",
                                "model": "hf.co/openthaigpt/openthaigpt1.5-72b-instruct:latest",
                                # "model": "hf.co/openthaigpt/openthaigpt1.5-14b-instruct:latest",
                                # "model": "ollama.com/Kanoon/openthaigpt70b-q4:latest",
                                #"options":'"num_predict": 10',
                                # "histories":'[{"role":"system", "content": "Your name is มณี and Respond in Thai and keep the response to just one sentence short as much as possible. at last your gender is lady response with ค่ะ"}]'}

                                "histories":'[{"role":"system", "content": "ผมขอกำหนดให้คุณชื่อมณี เป็นผู้หญิง ที่สามารถตอบได้เป็นธรรมชาติ และอ่อนน้อม"}]'}

                        async with session.post(f"{api_url}/speechtospeech", data=files) as resp:
                                if resp.status == 200:

                                    audio_data = await resp.read()

                                    # audio = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
                                    # play(audio)
                                    # Start save tasks 
                                    # asyncio.create_task(save_audio_to_file_mp3(audio_data, "voice/output/output.mp3"))

                                    et = time.time()
                                    logging.info(f"Time until the audio playback is: {et - st} seconds")
                                    print(f"Time untill the audio playback is : {et - st} seconds")

                                    # audio = AudioSegment.from_wav(io.BytesIO(audio_data))
                                    # play(AudioSegment.from_wav('output.wav'))

                                    play_audio(audio_data)


                                else:
                                    print(f"Error: {resp.status}, {await resp.text()}")

#-------------------------------------  Speech to text for detect greeting ------------------------------------------------------------------------------------------------------------

                        # with open(input_audio_path, "rb") as audio_file:
                        #     files = {"file": audio_file}
                        #     async with session.post(f"{api_url}/speechtotext", data=files) as s2tres:
                        #         if s2tres.status == 200:
                        #             speech_to_text_response = await s2tres.text()
                        #             print(f"Transcribed text is: {speech_to_text_response}")
                        #         else:
                        #             print(f"Error: {s2tres.status}, {await s2tres.text()}")

#------------------------------Convert to pcm and send the interaction(motion_name,face_expression)-------------------------------------------------------------------

            # convert_mp3_to_pcm("./voice/output/output.mp3", "./voice/pcm/voice.pcm")
            # interaction(voice_message_text=speech_to_text_response , audio_path="voice/pcm/voice.pcm")
            et = time.time()
            print(f"Execution time is : {et - st} seconds")
            # time.sleep(0.5)

asyncio.run(main())
