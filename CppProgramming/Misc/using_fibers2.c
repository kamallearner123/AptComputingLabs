#include <stdio.h>
#include <setjmp.h>

typedef struct Fiber {
    jmp_buf context;
    void (*function)(void);
    struct Fiber *next;
} Fiber;

Fiber *current_fiber = NULL;

void fiber_create(Fiber *fiber, void (*function)(void), Fiber *next_fiber) {
    fiber->function = function;
    fiber->next = next_fiber;

    if (setjmp(fiber->context) == 0) {
        return;
    } else {
        function();
    }
}

void fiber_switch(Fiber *next_fiber) {
    if (setjmp(current_fiber->context) == 0) {
        current_fiber = next_fiber;
        longjmp(current_fiber->context, 1);
    }
}

void fiber1() {
    printf("Fiber 1: Running...\n");
    fiber_switch(current_fiber->next);
    printf("Fiber 1: Resumed...\n");
}

void fiber2() {
    printf("Fiber 2: Running...\n");
    fiber_switch(current_fiber->next);
    printf("Fiber 2: Resumed...\n");
}

int main() {
    Fiber fiber1_struct, fiber2_struct;

    current_fiber = &fiber1_struct;

    fiber_create(&fiber1_struct, fiber1, &fiber2_struct);
    fiber_create(&fiber2_struct, fiber2, &fiber1_struct);

    fiber_switch(&fiber2_struct); // Start execution with fiber2
    fiber_switch(&fiber1_struct); // Start execution with fiber2
    fiber_switch(&fiber2_struct); // Start execution with fiber2
    fiber_switch(&fiber1_struct); // Start execution with fiber2

    return 0;
}

