#/usr/bin/env bash

TODAY=$(date +%-d)
FULLDATE=$(date +%d.%m.%Y)
NUM=$(( $TODAY+170 ))
URL="https://vindil.no/storage/media/$NUM/conversions/Trekning-$FULLDATE-main.jpg"
TMPFILE="/tmp/vind-${TODAY}.jpg"
MYNUMBER=$1
IWON=0

if [[ -z $(which tesseract) ]]; then
  echo "$0: tesseract is not installed"
  exit 1
fi

function box() { local t="$1xxxx";local c="${2:-=}"; echo "${t//?/$c}"; echo "$c $1 $c"; echo "${t//?/$c}"; }

box "Vinnertall i Vind ILs julekalender $FULLDATE "
wget -q "$URL" -O $TMPFILE
if [[ -s $TMPFILE ]]; then
  WINNERS=$(tesseract $TMPFILE - quiet | grep -oE '^[0-9]{2,4}:' | tr -d ':')
  if [[ -n "$MYNUMBER" ]]; then
    echo "Ditt registrerte loddnummer er: $MYNUMBER"
    $(echo "$WINNERS" | grep -q $MYNUMBER) && IWON=1
  fi
else
  WINNERS='...ikke trukket enda...'
fi

echo "Dagens tall: ${WINNERS//$'\n'/ }"
if [[ $IWON -eq 1 ]]; then
  echo "Du vant!"
fi

if [ -f $TMPFILE ]; then
  rm $TMPFILE
fi
