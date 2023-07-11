import base64
import logging
import os
import subprocess
import time
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

load_dotenv()
app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    # request_body = await request.json()
    logging.error(f"{request}: {exc_str} ")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.post("/v1/input")
@app.get("/v1/input")
async def completions(
    base64: Optional[str] = os.environ.get('TEST_MP3'),
):

    curTime = time.time()
    tempMp3 = f'/tmp/{curTime}.mp3'
    tempPcm = f'/tmp/{curTime}.pcm'
    tempSil = f'/tmp/{curTime}.sil'
    base64_to_mp3(base64, tempMp3)
    
    output = subprocess.check_output(f'ffmpeg -y -i {tempMp3} -acodec pcm_s16le -ar 24000 -ac 1 -f s16le {tempPcm}', shell=True)
    print(output.decode())
    output = subprocess.check_output(f'./encoder {tempPcm} {tempSil} -tencent', shell=True)
    print(output.decode())
    silBase64 = mp3_to_base64(tempSil)
    subprocess.run(f'rm -rf /tmp/{curTime}.*', shell=True)
    return silBase64



def mp3_to_base64(mp3_file):
    with open(mp3_file, 'rb') as file:
        audio_data = file.read()
        base64_data = base64.b64encode(audio_data).decode('utf-8')
        return base64_data

def base64_to_mp3(base64_data, output_file):
    # 将Base64数据解码为字节数据
    audio_data = base64.b64decode(base64_data)

    # 将字节数据写入MP3文件
    with open(output_file, 'wb') as file:
        file.write(audio_data)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
