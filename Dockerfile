ARG BASE_IMAGE=python:3.10.6
FROM $BASE_IMAGE

# Install the packages
RUN apt-get update
 
# Set the working directory to /app
WORKDIR /scrapapi
COPY . /scrapapi
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 80
CMD ["sh", "-c", "scrapyrt & uvicorn manage:app --host 0.0.0.0 --port 80 --reload"]