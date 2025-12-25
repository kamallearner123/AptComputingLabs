#include <stdio.h>
int main() {
    int x = 1 << 31;  // Left shift into sign bit
    printf("%d\n", x);
    return 0;
}
