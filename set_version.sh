#!/bin/bash

set -e

if [[ $# -ne 1 ]]; then
	echo "USAGE: $0 <version>"
	exit
fi

VERSION_STRING="Version:     "$1
DATE_STRING="Last change: "`date +%Y-%m-%d`
SCRIPT=plugin/SnippetySnip/SnippetySnip.vim
sed "s/Version:.*/$VERSION_STRING/" $SCRIPT > $SCRIPT".tmp"
sed "s/Last change:.*/$DATE_STRING/" $SCRIPT".tmp" > $SCRIPT
rm $SCRIPT".tmp"

echo "Tagged version "$1
echo "Now commit and do"
echo "git tag "$1
