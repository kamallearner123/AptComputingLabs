#include <stdio.h>
#include <unistd.h>
#include <setjmp.h>

#define STACK_SIZE 1024 * 64

typedef struct Fiber {
    jmp_buf context;
    void (*function)(void);
    char stack[STACK_SIZE];
} Fiber;

Fiber* current_fiber = NULL;

void fiber_create(Fiber* fiber, void (*function)(void)) {
    if (setjmp(fiber->context) == 0) {
        fiber->function = function;
        // Manually adjust the stack pointer (not portable, depends on the platform)
        asm volatile ("mov %0, %%rsp" : : "r" (fiber->stack + STACK_SIZE));
        function();
    }
}

void fiber_switch(Fiber* next_fiber) {
    if (setjmp(current_fiber->context) == 0) {
        current_fiber = next_fiber;
        longjmp(current_fiber->context, 1);
    }
}

void fiber1() {
	while(1) {
		sleep(1);
    printf("Fiber 1: Running...\n");
	}
}

void fiber2() {
	while(1) {
		sleep(1);
    printf("Fiber 2: Running...\n");
	}
}

int main() {
    Fiber fiber1_struct, fiber2_struct;
    current_fiber = &fiber1_struct;

    fiber_create(&fiber1_struct, fiber1);
    fiber_create(&fiber2_struct, fiber2);

    while(1) {
	sleep(10);
    	fiber_switch(current_fiber);
    }
    //fiber_switch(&fiber2_struct); // Switch to fiber 2

    return 0;
}

