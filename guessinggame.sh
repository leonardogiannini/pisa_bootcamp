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

function fffi2 {
  s1=":_:_:_:_:_:_:_:_:_:_:_\r"
  s2="_:_:_:_:_:_:_:_:_:_:_:\r"
  s3="-:-:-:-:-:-:-:-:-:-:-:\r"
  s4="/:/:/:/:/:/:/:/:/:/:/:\r"
  s5=":/:/:/:/:/:/:/:/:/:/:/\r"
  

  for i in $(seq 0 1 9)
  do
	  echo -ne $s1
	  sleep 0.1
	  echo -ne $s2
	  sleep 0.1
	  echo -ne $s1
	  sleep 0.1
	  echo -ne $s2
	  sleep 0.1
	  echo -ne $s1
	  sleep 0.1
	  echo -ne $s2
	  echo ""
	  
  done
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
	fi
done

fff

echo ""

fffi2

echo ""

fff
