USER=$1
ANNOTATEDFRAMEPATH=/root/vatic/data/frames_in
TURKOPS="--offline --title Hello!"
LABELS="person car"




for i in $( ls $ANNOTATEDFRAMEPATH); do
	ID=$USER"_"$i
	turkic load $ID $ANNOTATEDFRAMEPATH/$i $LABELS $TURKOPS
done