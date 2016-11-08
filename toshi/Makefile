CC			= gcc
CFLAGS		= `pkg-config --cflags --libs opencv`
OBJS		= main.out

all:		header.h dct.c locate_char.c main.c
			$(CC) -o main.out main.c $(CFLAGS)


# Note:  The .bmp file we are analysing must be inside the 'chars' directory
do:			$(OBJS)
			rm -f ./chars/extracted_chars/*
			./main.out

clean:;		rm $(OBJS)
			
$(PROGRAM):	
