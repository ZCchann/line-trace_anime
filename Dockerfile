FROM python:3.6-alpine

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000/TCP
ENTRYPOINT ["python"]
CMD ["./run.py"]