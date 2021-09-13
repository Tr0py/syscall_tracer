# syscall_tracer

Idea: Compile source code statically, so `syscall` instructions are in the binary file. Then generate a call graph.

## Run the demo

This demo generates a full call graph, and traverse the graph from function `<main>` as a demo.

```
git clone https://github.com/Tr0py/syscall_tracer.git
cd syscall_tracer
make
```

### Expected Output
```
➜  syscall-call-graph git:(master) make
clang -g3 -static hello.c -o hello -pthread
objdump -dSl hello > hello.dis
./extract_syscall.py
Showing the call graph for main:
main->__pthread_join->_IO_printf->__stack_chk_fail->__fortify_fail_abort->__libc_message-->sys_not a detemined syscall
main->__pthread_join->_IO_printf->__stack_chk_fail->__fortify_fail_abort->__libc_message->__mmap64-->sys_mmap
main->__pthread_join->_IO_printf->__stack_chk_fail->__fortify_fail_abort->__libc_message->__mmap64-->sys_not a detemined syscall
main->__pthread_join->_IO_printf->__stack_chk_fail->__fortify_fail_abort->__libc_message->__mmap64->__munmap-->sys_munmap
Error: function not in call graph (not implemented): .plt+0xa0
main->__pthread_join->_IO_printf->__stack_chk_fail->__fortify_fail_abort->__libc_message->__mmap64->__munmap->__open64_nocancel-->sys_openat
```
