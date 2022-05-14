#!/bin/bash
n=$1
i=1
x=0
# your code here
while [[ "$i" -le "$n" ]]
do
x=$(($x + $i))
i=$(($i + 1))
echo $x
done
echo $x

#!/bin/bash
i=1
countToTwenty() {
  while [ "$i" -le "20" ]
  do
  echo "Count: $i"
  i=$(( $i + 1 ))
  done
}
countToTwenty