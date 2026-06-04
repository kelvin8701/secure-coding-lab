/* vuln.c  —  Secure Coding Lab 3 (carried over from Lab 2)
 *
 * Same return-address-overwrite target you exploited in Lab 2. In Lab 3 you
 * keep this source UNCHANGED and only vary the build flags. The hidden win()
 * function is never called by main(); in Lab 2 you redirected execution to it
 * by overwriting the saved return address. Now you will see how the canary,
 * NX, and ASLR each interfere with that same payload.
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win(void) {
    printf("[+] win() reached — spawning shell\n");
    system("/bin/sh");
}

void vulnerable(void) {
    char buf[64];
    printf("Enter data: ");
    gets(buf);                   /* no bounds check: overflow reaches saved EIP */
    printf("You entered: %s\n", buf);
}

int main(void) {
    vulnerable();
    printf("Returned normally — no redirect occurred.\n");
    return 0;
}
