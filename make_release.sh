#!/bin/bash

set -e

if [[ $# -ne 1 ]]; then
	echo "USAGE: $0 <version>"
	exit
fi

git co $1
tar zcf SnippetySnip-$1.tgz python plugin --exclude *.pyc --exclude *.swp
git co master
