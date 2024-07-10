#! /bin/bash

# For URL structure reasons, our "api/" directory has a mixture of "root" files
# that must exist (the ones for each module) and other files that live in
# version control but are generated by the automodapi system. In order to
# refresh the latter files, they must be deleted before running a doc build.
# This script does that, while leaving the "root" files.

apidir=$(dirname $0)/api

cd "$apidir"

for f in *.rst; do
    case "$f" in
    wwt_api_client.rst|\
    wwt_api_client.communities.rst|\
    wwt_api_client.constellations.rst|\
    wwt_api_client.constellations.data.rst|\
    wwt_api_client.constellations.handles.rst|\
    wwt_api_client.constellations.images.rst|\
    wwt_api_client.constellations.scenes.rst|\
    wwt_api_client.enums.rst) ;;

    *) rm -f "$f"
    esac
done