#!/bin/bash
for demo in code_server code_server_pinned custom_apt_key_dearmor jupyterlab/v3 jupyterlab/v4 mariadb nbclassic openrefine tutorial_server
do
    ./demo-tests.sh $demo
    if [ ! $? == "0" ]
    then
        exit 1
    fi
done
