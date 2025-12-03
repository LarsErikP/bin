#/usr/bin/env bash

TODAY=$(date +%-d)
FULLDATE=$(date +%d.%m.%Y)
URL="https://www.vindil.no/wp-content/uploads/2025/12/Trekning-$TODAY.12.2025-1080x675.jpg"
TMPFILE="/tmp/vind-${TODAY}.jpg"
MYNUMBER=$1
IWON=0

if [[ -z $(which tesseract) ]]; then
  echo "$0: tesseract is not installed"
  exit 1
fi

echo "Vinnertall i Vind ILs julekalender $FULLDATE er:"
wget -q "$URL" -O $TMPFILE
if [[ -s $TMPFILE ]]; then
  WINNERS=$(tesseract $TMPFILE - | grep -oE '^[0-9]{4}')
  if [[ -n "$MYNUMBER" ]]; then
    echo "Ditt registrerte loddnummer er: $MYNUMBER"
    $(echo "$WINNERS" | grep -q $MYNUMBER) && IWON=1
  fi
else
  WINNERS='...ikke trukket enda...'
fi

echo $WINNERS
if [[ $IWON -eq 1 ]]; then
  echo "Du vant!"
fi

rm $TMPFILE
