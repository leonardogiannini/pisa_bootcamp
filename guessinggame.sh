#!/bin/bash 
echo ":_:_:_:_:_:_:_:_:_:_:_"
echo "Hello and welcome to this guessing game"
echo ":_:_:_:_:_:_:_:_:_:_:_"
echo ""
sleep 2
echo -ne "The big question is\r"
sleep 0.6
echo -ne "The big question is: how many files\r"
sleep 0.6
echo -ne "The big question is: how many files are there\r"
sleep 0.6
echo -ne "The big question is: how many files are there in the current directory?"
echo ""
sleep 2

function fff {
  echo "HAHAHA";
}

function fcounter {
  echo $(ls | wc -l);

}

aaa=1

while [[ $aaa -eq 1 ]]
do
	echo "enter some figure"
	read response
	echo "You entered: $response"
	if [[ $response -eq `eval fcounter` ]]
	then
		sleep 2
		echo "BIG YES!!!"
		aaa=0
        elif  [[ $response -lt `eval fcounter` ]]
	then
		echo "your answer is too low: less than the # of files"
	elif [[ $response -gt `eval fcounter` ]]
	then
		echo "your answer is too high: greater than the # of files"
	fi
done
fff
