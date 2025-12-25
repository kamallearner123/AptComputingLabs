#include <stdio.h>
int main() {
    int x = 5;
    int y = x++ + x++;
    printf("%d %d", x, y);
    return 0;
}
