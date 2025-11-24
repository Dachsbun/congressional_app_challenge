from fastapi import FastAPI, Request, WebSocket, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
import pitchtools

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


import aubio
import numpy as num
import pyaudio
import sys

# Some constants for setting the PyAudio and the
# Aubio.
BUFFER_SIZE             = 2048
CHANNELS                = 1
FORMAT                  = pyaudio.paFloat32
METHOD                  = "default"
SAMPLE_RATE             = 44100
HOP_SIZE                = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME    = HOP_SIZE

#constants i need
high_pitch=0

# Initiating PyAudio object. 
pA = pyaudio.PyAudio()
# Open the microphone stream.
mic = pA.open(format=FORMAT, channels=CHANNELS,
    rate=SAMPLE_RATE, input=True,
    frames_per_buffer=PERIOD_SIZE_IN_FRAME)

# Initiating Aubio's pitch detection object.
pDetection = aubio.pitch(METHOD, BUFFER_SIZE,
    HOP_SIZE, SAMPLE_RATE)
# Set unit.
pDetection.set_unit("Hz")
# Frequency under -40 dB will considered
# as a silence.
pDetection.set_silence(-40)


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="item.html", context={}
    )

@app.get("/start/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="start_page.html", context={}
    )
    
@app.get("/pitch-find/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="pitch_find.html", context={}
    )
'''
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        # Convert into number that Aubio understand.
        samples = num.fromstring(data,
            dtype=aubio.float_type)
        # Finally get the pitch.
        pitch = pDetection(samples)[0]

        # Finally print the pitch
        print(str(pitch))
'''

@app.get("/pitch-select/", response_class=HTMLResponse)
async def form_post(request: Request):
    low_pitch = "what frequency"
    high_pitch = ""
    return templates.TemplateResponse(
        request=request, name="pitch_select.html", context={'lower': low_pitch, 'higher': high_pitch}
    )

@app.post("/pitch-select/")
async def form_post(request: Request, lower: Annotated[str, Form()], higher: Annotated[str, Form()]):
    global high_pitch
    global low_pitch
    high_pitch = pitchtools.n2f(higher)
    low_pitch = pitchtools.n2f(lower)
    return templates.TemplateResponse(
        request=request, name="pitch_select_submit.html", context={'lower': low_pitch, 'higher': high_pitch}
    )

@app.get("/arppegios/", response_class=HTMLResponse)
async def read_item(request: Request):
    global high_pitch
    global low_pitch
    return templates.TemplateResponse(
        request=request, name="arppegios.html", context={'highPitch': high_pitch, 'lowPitch': low_pitch}
    )