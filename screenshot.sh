#!/bin/bash
# A quick and dirty script to take a screenshot, upload it via scp
# and put a link to it in the clipboard for easy pasting to i.e. IRC.
# It assumes a lot of things, e.g. that ssh to the target host has
# been set up with a working private key, and that xclip and
# gnome-screenshot is installed.
#
# If all you have is a hammer, everything looks like a nail.

# Shamlessly stolen from Einar at git.slaskete.net all credit goes to him.
# I'll buy him a beer
# Slightly modified to my needs and config. Added RemotePort, and the creation of LocalPath
# if it is non-existent

# Settings
RemoteUser="larserik"
RemoteHost="larserikp.com"
RemotePort=12222
RemotePath="/srv/pic.laserskip.cloud/screenshots"
LocalPath="${HOME}/screenshots/"
UrlBase="https://pic.laserskip.cloud/img"

function errcho() {
  >&2 echo -e "$@"
}

function take_screenshot() {
  if [ ! -d "${LocalPath}" ]; then
    mkdir "${LocalPath}"
  fi
  FileName="$(tr -dc 'a-zA-Z0-9' < /dev/urandom | fold -w 6 | head -n 1).png"
  if [ "$*" = "clipboard" ]; then
    xclip -out -selection clipboard -t image/png > "/tmp/${FileName}" 2>/dev/null
    if [ "$(file -b --mime-type "/tmp/${FileName}")" == "image/png" ]; then
      mv "/tmp/${FileName}" "${LocalPath}/"
    else
      rm "/tmp/${FileName}"
      notify-send -i applets-screenshooter "screenshot.sh" "Tried to post image from clipboard, but found no image there."
    fi
  else
    gnome-screenshot -f "${LocalPath}/${FileName}" -p "$@"
  fi
  if [ -f "${LocalPath}/${FileName}" ]; then
    scp -q -P ${RemotePort} "${LocalPath}/${FileName}" "${RemoteUser}@${RemoteHost}:${RemotePath}"
    echo -n "${UrlBase}/${FileName}"|xclip -selection p
    echo -n "${UrlBase}/${FileName}"|xclip -selection c
    notify-send -i applets-screenshooter "screenshot.sh" "Screenshot published to ${UrlBase}/${FileName}"
  fi
}

function show_error() {
  errcho "Please use one of: -w, --window, -a, --area, -s, --selection,"
  errcho "                   -f, --full or no argument at all."
  exit 1
}

case ${1} in
  -w|--window)
    take_screenshot -w -b -e shadow
    ;;
  -a|--area|-s|--selection)
    sleep 0.2
    take_screenshot -a
    ;;
  ""|-f|--full)
    take_screenshot
    ;;
  -c|--clipboard|-p|--paste)
    take_screenshot clipboard
    ;;
  *)
    show_error
    ;;
esac

