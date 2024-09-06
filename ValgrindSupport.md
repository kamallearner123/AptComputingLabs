1. Basic Valgrind Command:

This command checks for memory errors, leaks, and invalid memory usage.

    valgrind --leak-check=full ./your_program

*--leak-check=full: Provides detailed information about memory leaks.

2. Check for Uninitialized Memory Usage:

Use the memcheck tool (default Valgrind tool) to detect uninitialized memory usage, invalid memory reads/writes, etc.
    valgrind --tool=memcheck --track-origins=yes ./your_program

*--track-origins=yes: Helps to track where uninitialized values come from, making debugging easier.


Detect Memory Leaks:

This command checks for memory leaks and summarizes them.
    valgrind --leak-check=full --show-leak-kinds=all ./your_program

*--show-leak-kinds=all: Displays detailed information about all types of memory leaks, including definitely, indirectly, possibly, and reachable lost memory.

