#include <stdio.h>
#include <pthread.h>

void *mfunc() 
{
	printf("haha!\n");
	
};

int main() 
{
	printf("hello world\n");
	fopen("./test.txt", "r");
	mfunc();
    pthread_t tid;
    pthread_create(&tid, NULL, mfunc, NULL);
    pthread_join(tid, NULL);
	return 0;
}
