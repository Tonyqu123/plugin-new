FROM python:2-alpine

LABEL maintainer="Pike" \
      io.daocloud.dce.plugin.name="Jobs" \
      io.daocloud.dce.plugin.description="应用作业" \
      io.daocloud.dce.plugin.categories="container-tool" \
      io.daocloud.dce.plugin.vendor="DaoCloud" \
      io.daocloud.dce.plugin.required-dce-version=">=2.6.0" \
      io.daocloud.dce.plugin.nano-cpus-limit="500000000" \
      io.daocloud.dce.plugin.memory-bytes-limit="1048576000"

WORKDIR /usr/src/app/

ENV AGENT_PUBLISHED_PORT 12374
ENV DCE_JOBS_PLUGIN_LOG_STORE_PATH "/root"

COPY ./requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt \
  && apk add --update --no-cache nginx supervisor \
  && rm -rf /usr/src/python ~/.cache \
  && rm -rf /var/cache/apk/*

EXPOSE 80

COPY ./certs /etc/ssl/private
COPY ./plugin.json /usr/src/app/plugin.json
COPY ./nginx /etc/nginx/jobs
COPY ./bin /jobs

COPY ./root/dist /usr/src/app/ui
COPY ./jobs /usr/src/app/jobs

CMD ["/jobs/server.sh"]
