FROM python:3.10

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /app/data /data
COPY /app/img /img
COPY /app/sound /sound
COPY /app font.otf
COPY /app head.png
COPY /app main.py

CMD [ "python", "main.py" ]