import base64
import logging
import subprocess
import time
from typing import Optional

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

load_dotenv()
app = FastAPI()


class SilkParams(BaseModel):
    base64: Optional[str]
    url: Optional[int]


class SilkResponse(BaseModel):
    code: Optional[int] = 200
    message: str
    data: str


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    # request_body = await request.json()
    logging.error(f"{request}: {exc_str} ")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.post("/v1/encoder")
async def encoder(params: SilkParams):
    res = SilkResponse()
    if params.url is None and params.base64 is None:
        res.code = 400
        res.message = '❌ params must not be empty!'
        return JSONResponse(
            content=res.json(ensure_ascii=False),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    tempMp3, tempPcm, tempSil, curTime = getTmpFileName()

    if params.url is not None:
        download_file(params.url, tempMp3)
    else:
        base64_to_file(params.base64, tempMp3)

    output = subprocess.check_output(
        f'ffmpeg -y -i {tempMp3} -acodec pcm_s16le -ar 24000 -ac 1 -f s16le {tempPcm}',
        shell=True,
    )
    print(output.decode())

    output = subprocess.check_output(
        f'./encoder {tempPcm} {tempSil} -tencent', shell=True
    )
    print(output.decode())

    silBase64 = file_to_base64(tempSil)
    subprocess.run(f'rm -rf /tmp/{curTime}.*', shell=True)

    res.message = 'ok'
    res.data = silBase64

    response = JSONResponse(content=res.json(ensure_ascii=False))
    return response


@app.post("/v1/decoder")
async def decoder(params: SilkParams):
    res = SilkResponse()
    if params.url is None and params.base64 is None:
        res.code = 400
        res.message = '❌ params must not be empty!'
        return JSONResponse(
            content=res.json(ensure_ascii=False),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    tempSil, tempMp3, curTime = getTmpFileName()
    if params.url is not None:
        download_file(params.url, tempSil)
    else:
        base64_to_file(params.base64, tempSil)

    output = subprocess.check_output(f'sh converter.sh {tempSil} mp3', shell=True)
    print(output.decode())

    mp3Base64 = file_to_base64(tempMp3)
    subprocess.run(f'rm -rf /tmp/{curTime}.*', shell=True)

    res.message = 'ok'
    res.data = mp3Base64

    response = JSONResponse(content=res.json(ensure_ascii=False))
    return response


def file_to_base64(mp3_file):
    with open(mp3_file, 'rb') as file:
        audio_data = file.read()
        base64_data = base64.b64encode(audio_data).decode('utf-8')
        return base64_data


def base64_to_file(base64_data, output_file):
    audio_data = base64.b64decode(base64_data)
    with open(output_file, 'wb') as file:
        file.write(audio_data)


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


def getTmpFileName():
    curTime = time.time()
    tempMp3 = f'/tmp/{curTime}.mp3'
    tempPcm = f'/tmp/{curTime}.pcm'
    tempSil = f'/tmp/{curTime}.sil'
    return tempMp3, tempPcm, tempSil, curTime


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
