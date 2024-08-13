# Dockerfile for Fluentd with Elasticsearch plugin
FROM fluent/fluentd:v1.17.0-debian-amd64-1.0

USER root
RUN gem install fluent-plugin-elasticsearch --no-document
#Install fluentd for logging use.

USER fluent


