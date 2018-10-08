#!/usr/bin/env sh
docker build . -t shopping-db
docker run -p 5432:5432 -d shopping-db
