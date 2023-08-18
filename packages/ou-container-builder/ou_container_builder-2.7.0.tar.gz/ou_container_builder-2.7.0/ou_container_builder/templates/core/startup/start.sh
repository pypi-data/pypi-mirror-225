#!/bin/bash

set -e

sudo /bin/chown {{ image.user }}:100 /home/{{ image.user }}/{{ module.code }}-{{ module.presentation }}

{% if flags and flags.ou_container_content %}
ou-container-content startup
{% endif %}

if [[ ! -z "${JUPYTERHUB_API_TOKEN}" ]]; then
    export JUPYTERHUB_SINGLEUSER_APP='jupyter_server.serverapp.ServerApp'
    exec jupyterhub-singleuser
else
    exec jupyter server
fi

{% if flags and flags.ou_container_content %}
ou-container-content shutdown
{% endif %}
