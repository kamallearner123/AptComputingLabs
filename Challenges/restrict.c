#include <stdio.h>

void add(int *restrict a, int *restrict b, int n) {
    for (int i = 0; i < n; i++) {
        a[i] = a[i] + b[i];  // OK
    }
}

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    add(arr, arr, 5);  // BUG: same pointer violates restrict!
    for (int i = 0; i < 5; i++) printf("%d ", arr[i]);
    return 0;
}
