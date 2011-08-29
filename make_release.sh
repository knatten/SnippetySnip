#!/bin/bash

set -e

if [[ $# -ne 1 ]]; then
	echo "USAGE: $0 <version>"
	exit
fi

git co $1
tar zcf SnippetySnip-$1.tgz * --exclude *.pyc --exclude *.swp --exclude *.tgz --exclude make_release.sh --exclude set_version.sh
git co master
