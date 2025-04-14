FROM python:3

# Copy your existing files
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY main.py .
COPY faceit ./faceit

CMD ["fastapi", "run"]