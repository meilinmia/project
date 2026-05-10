#include <stdio.h>

int check(char *input) {
    if (input[0] == 's' &&
        input[1] == 'e' &&
        input[2] == 'c' &&
        input[3] == 'r' &&
        input[4] == 'e' &&
        input[5] == 't') {
        return 1;
    } else {
        return 0;
    }
}

int main() {
    char input[8];

    printf("Input: ");
    scanf("%7s", input);

    if (check(input)) {
        printf("Good\n");
    } else {
        printf("Bad\n");
    }

    return 0;
}