all : 
	clear
	gcc -Ofast bbc.c -o bbc 
	# x86_64-w64-mingw32-gcc -OFast bbc.c -o bbc.exe
debug : 
	gcc bbc.c -o bbc
	# x86_64-w64-mingw32-gcc bbc.c -o bbc.exe