#####################################################################################
dist_dir=$(CURDIR)/deploy
service=liepa-whisper
version=dev-liepa3
#####################################################################################
########### DOCKER ##################################################################
tag=$(service):$(version)

dbuild:
	docker buildx build -t $(tag) --build-arg BUILD_VERSION=$(version) --build-arg TOOLS_VERSION=$(version) \
		-f Dockerfile .

run:
	docker run --gpus all -it -v ${PWD}/models:/root/.cache/huggingface/ -v ${PWD}/audio-files:/app/audio-files liepa-whisper:dev-liepa3 -i audio-files/zinios.wav -r audio-files/zinios.res.fix.rttm

dpush: dbuild
	docker push $(tag)

dscan: dbuild
	docker scan --accept-license $(tag)	
#####################################################################################
.PHONY:
	clean copy build dbuild dpush
