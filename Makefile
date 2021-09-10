CC=clang

all: hello hello.dis 

# Compile binary file
hello: hello.c
	$(CC) -g3 -static $< -o $@ -pthread

# Disassemble 
hello.dis: hello
	objdump -dSl $< > $@
	
# This is the LLVM IR
hello.ll:
	clang -S -emit-llvm 

clean:
	rm -rf hello hello.dis hello.ll
