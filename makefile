all: mycommands


mycommands: guessinggame.sh
	echo '# Project: "Guessing the number of files" ' > README.md
	echo '## a game worth your time!!! ^_^' >> README.md
	echo ''>> README.md
	echo -n 'generating this file on  ' >> README.md 
	date -u  +"%Y-%m-%d %T UTC" >> README.md
	echo ''>> README.md
	echo -n 'not a short game: the file lines are ' >> README.md
	cat guessinggame.sh | wc -l >> README.md
	echo '\nsee you next time -- Ciao!!! ' >> README.md

