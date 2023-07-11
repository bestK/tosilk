#!/bin/bash
ffmpeg -y -i input.mp3 -acodec pcm_s16le -ar 24000 -ac 1 -f s16le output.pcm
./encoder output.pcm output.sil -tencent