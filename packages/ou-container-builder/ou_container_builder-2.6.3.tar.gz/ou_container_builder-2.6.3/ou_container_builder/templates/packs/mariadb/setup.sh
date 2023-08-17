#!/bin/bash

service mariadb start

sleep 5

# Check if the database exists and if not create it
echo "SHOW SCHEMAS;" | mariadb | grep "{{ database }}"
ret=$?
if [ $ret -ne 0 ];
then
  echo "CREATE DATABASE {{ database }}" | mariadb
fi

# Check if the user exists and if not create it
echo "SELECT user FROM mysql.user;" | mariadb | grep "{{ username }}"
ret=$?
if [ $ret -ne 0 ];
then
  echo "CREATE USER {{ username }} IDENTIFIED BY '{{ password }}';" | mariadb
fi

# Grant the user all privileges to the database
echo "GRANT ALL PRIVILEGES ON {{ database }}.* TO {{ username }};" | mariadb

service mariadb stop
