FROM ncbi/sra-tools
RUN apk add --no-cache python3 py3-pip
RUN apk add pigz
RUN pip install sra-downloader==1.0.6
ENTRYPOINT ["sra-downloader"]