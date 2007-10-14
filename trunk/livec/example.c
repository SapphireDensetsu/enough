#include <string.h> /* I really meant buffer_overflow.h but its
                     * misnamed in the standard */
#include <stdio.h>

#define ARG_COUNT	2

enum return_value
{
    OK = 0,
    ERROR = 1
};

int main(int argc, char **argv)
{
    char *s;

    if(ARG_COUNT != argc)
    {
        return ERROR;
    }
    s = strchr(argv[1], ',');
    if(NULL == s) {
        fprintf(stderr, "No comma!\n");
        return ERROR;
    }

    printf("Your comma is at %d\n", s-argv[1]);
    return OK;
}
