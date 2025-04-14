#!/bin/bash


docker run --gpus all -it -v ${PWD}/models:/root/.cache/huggingface/ -v ${PWD}/audio-files:/app/audio-files liepa-whisper:dev-liepa3 -i audio-files/zinios.wav -r audio-files/zinios.res.fix.rttm
