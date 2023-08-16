git log|grep Author| awk -F: '{print $2;}' | sed 's%\([ ]*\)\(.*\)<.*>\([ ]*\)%\2%g' |sort|uniq | \
  (
    while read; do
	n=$(git log | grep Author | grep "$REPLY" | wc | awk '{print $1;}' )
	echo "'$REPLY' $n"
    done
  )
