#!/bin/bash

pid='32wmv'
basedir="osfstorage/tutorials"

function usage()
{
	echo "Usage: $(basename "$0") [-p proj] [-b basedir] [-h] filename" >&2
	echo "Download and decompress tutorial or test dataset file from OSF into current folder." >&2
	echo "Existing files may be overwritten." >&2
	fmt='  %-12s%s\n'
	printf "$fmt" 'filename' 'Full file name to download, e.g. trajectory-skin.tar.xz' >&2
	printf "$fmt" '-p proj' 'OSF project ID. Default: '"$pid" >&2
	printf "$fmt" '-b basedir' 'Base directory of file. Default: '"$basedir" >&2
	printf "$fmt" '-h' 'Display this help' >&2
	exit 1
}

#Parse arguments
while getopts ':p:b:h' o; do case "$o" in
	p)	pid="$OPTARG";;
	b)	basedir="$OPTARG";;
	:)	echo "Error: -${OPTARG} requires an argument." >&2;echo >&2;usage;;
	*)	usage;;
	esac
done
shift $((OPTIND-1))

set -eo pipefail

if [ "a$1" == "a" ] || [ "a$2" != "a" ]; then
	usage
fi

rm -f "$fname".* 

fs="$(osf -p "$pid" ls | grep "^$basedir$fname"'[.][0-9]*$')"

for f in $fs; do
	osf -p "$pid" fetch "$basedir/$f" "$f"
done
cat "$fname".* > "$fname"
tar xf "$fname"
rm "$fname" "$fname".*























#
