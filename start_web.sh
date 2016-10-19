#!/bin/bash

# one-liners for serving static data on a folder:
# https://gist.github.com/willurd/5720255



if command -v static >/dev/null 2>&1
then
    static -a 0.0.0.0 -p 8100 www/
    exit 0;
fi

echo >&2 "Please install node-static from node.js:: sudo npm install -g node-static";


if command -v python3 >/dev/null 2>&1
then
    echo >&2 "WARN: Sometimes Python hagns up if some packets won't get delivered."
    cd www/; python3 -m http.server 8100
    exit 0;
fi

if test -f /c/nginx*/nginx.exe
then
	tail -f /c/nginx*/logs/access.log &
TAILPID=$!
	(cd /c/nginx*/ ; ./nginx.exe )
	kill $TAILPID
fi

echo >&2 "ERROR: No HTTP-SERVER one-liners known found. Either install Python3 or Node.js"; exit 1;
