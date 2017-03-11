#!/bin/bash
#
# Author: Carson Gee <x@carsongee.com>
#
# Initializes the passed in folder as a new git repo
# and pushes it to the specified remote

PATH="/sbin:/usr/sbin:/bin:/usr/bin" 

DEFAULT_GIT_SERVER="git@git.carsongee.com"


EXPECTED_ARGS=1
E_BADARGS=65

progname=$(basename $0) 
usage()
{

	cat <<EOF
Usage: git-new-repo [options] DIRECTORY

Initialize, add, commit and push the specified
directory to the specified remote system

Options:
 --help print this help message
 -r, --remote=STRING git remote string [ $DEFAULT_GIT_SERVER ]

EOF
}

SHORTOPTS="r:"
LONGOPTS="help,remote:"

if $(getopt -T >/dev/null 2>&1) ; [ $? = 4 ] ; then # New longopts getopt.
 OPTS=$(getopt -o $SHORTOPTS --long $LONGOPTS -n "$progname" -- "$@")
else # Old classic getopt.
 # Special handling for --help on old getopt.
 case $1 in --help) usage ; exit 0 ;; esac
 OPTS=$(getopt $SHORTOPTS "$@")
fi

if [ $? -ne 0 ]; then
 echo "'$progname --help' for more information" 1>&2
 exit 1
fi

eval set -- "$OPTS"

remote="$DEFAULT_GIT_SERVER"

while [ $# -gt 0 ]; do
	: debug: $1
	case $1 in
		--help)
			usage
			exit 0
			;;
		-r|--remote)
			remote=$2
			shift 2
			;;
		--)
			shift
			break
			;;
		*)
			echo "Internal Error: option processing error: $1" 1>&2
			exit 1
			;;
	esac
done

if [ $# -ne $EXPECTED_ARGS ] ; then
	echo "$EXPECTED_ARGS arguments were expected" >&2
	usage
	exit $E_BADARGS
fi

# Begin script
REPO_NAME=`basename $1`
echo "Initializing repo $REPO_NAME"
cd $1
git init
git remote add origin $remote:$REPO_NAME.git

# Check if there are any files in the repo
# if not, create one so the commit isn't empty
NUM_FILE=`ls -l | grep -v total | wc -l`
if [ $NUM_FILE -eq 0 ] ; then
	echo "Initial repo file: delete me." >  init
fi
git add . 
git commit -a -m "Initial repository commit"
git push origin master:refs/heads/master

# Helpfully set the master branch to the new remote
cat >> .git/config <<EOF
[branch "master"]
        remote = origin
        merge = refs/heads/master
EOF
exit 0
