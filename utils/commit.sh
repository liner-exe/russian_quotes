#!/bin/bash

git add .

if [ -z "$1" ]; then
	echo "No commit message passed."
	exit 1
fi

git commit -m "$1"

if [ $? -eq 0 ]; then
	echo "Succesfully commited with message: $1"
else
	echo "Commit error."
	exit 1
fi