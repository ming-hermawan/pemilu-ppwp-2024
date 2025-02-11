FROM python:3.11.11-bookworm

RUN pip install aiohttp aiofiles python-dotenv;

RUN mkdir -p /opt/pemilu-ppwp-2024;
RUN mkdir -p /opt/pemilu-ppwp-2024/src /opt/pemilu-ppwp-2024/out;
COPY "./src" "/opt/pemilu-ppwp-2024/src"
WORKDIR /opt/pemilu-ppwp-2024/src
COPY "./docker-entrypoint.sh" "/usr/bin/docker-entrypoint.sh"
RUN chmod +x /usr/bin/docker-entrypoint.sh;

CMD ["docker-entrypoint.sh"]
