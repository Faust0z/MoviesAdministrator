FROM python:3.13

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        locales \
        python3-yaml \
        rsyslog systemd systemd-cron sudo \
    && apt-get clean

COPY . .

CMD ["streamlit", "run", "run.py"]
