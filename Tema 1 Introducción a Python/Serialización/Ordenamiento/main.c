#include <stdio.h>
#include <stdlib.h>

int main(void)
{
	unsigned int value = 0x1;
	char *r = (char *) &value;
	
        char *line = (*r == 1) ? "Little Endian" : "Big Endian";

	fprintf(stdout, "Your sistem is... %s\n", line);
	return EXIT_SUCCESS;
}
