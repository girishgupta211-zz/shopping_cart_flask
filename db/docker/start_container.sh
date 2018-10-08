#!/usr/bin/env sh
docker build . -t acorn-db
docker run -p 5432:5432 -d acorn-db