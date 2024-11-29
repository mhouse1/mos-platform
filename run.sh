#!/bin/bash
# Usage: ./run.sh -x console-image -c -b
# where -c specify clean , -b means build
source sources/poky/oe-init-build-env build

OPTSTRING="cbx:"
while getopts ${OPTSTRING} opt; do
  case ${opt} in
    b)
      echo "Building: $IMAGE_NAME"
      bitbake $IMAGE_NAME
      ;;
    c)
        echo "cleaning image: $IMAGE_NAME"
        # -c cleans the output directory , -fc  does a complete clean including sstate-cache and download files
        bitbake -fc cleanall $IMAGE_NAME
        # clean the files from the build folder , since  -fc cleanall misses some
        rm -rf tmp/
        rm -rf sstate-cache/
        rm -rf downloads/
        ;;
    x)
      echo "Image name specified: ${OPTARG}"
      IMAGE_NAME=${OPTARG}
      echo "Image name : $IMAGE_NAME"
      ;;

    :)
      echo "Option -${OPTARG} requires an argument."
      exit 1
      ;;
    ?)
      echo "Invalid option: -${OPTARG}."
      exit 1
      ;;
  esac
done