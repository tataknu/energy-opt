FROM python:3.9

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]