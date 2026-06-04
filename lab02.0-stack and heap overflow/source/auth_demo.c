/*
 * auth_demo.c
 *
 * Vulnerable authentication program for Lab 2 — Part B
 * Demonstrates adjacent local variable corruption via stack buffer overflow.
 *
 * Compile (from project root):
 *   gcc -m32 -fno-stack-protector -z execstack -no-pie -g -O0 \
 *       -o auth_demo source/auth_demo.c
 *
 * Run normally:
 *   echo "alice" | ./auth_demo
 *
 * Exploit:
 *   python3 -c "import sys; sys.stdout.buffer.write(b'A'*OFFSET + b'\x01\x00\x00\x00')" | ./auth_demo
 *   (replace OFFSET with the value you find via gdb)
 */

#include <stdio.h>
#include <string.h>
#include <unistd.h>

int authenticate(void) {
    int  authenticated = 0;   /* auth flag — must remain zero unless password OK */
    char buffer[64];          /* log buffer — DELIBERATELY UNSAFE size */

    /* Diagnostic prints so students can see what is happening on the stack */
    printf("[info] buffer        is at %p\n", (void*)buffer);
    printf("[info] &authenticated is at %p\n", (void*)&authenticated);
    printf("[info] distance       = %ld bytes\n",
           (long)((char*)&authenticated - buffer));

    printf("Enter username: ");
    fflush(stdout);

    /* UNSAFE: reads up to 200 bytes into a 64-byte buffer.
     * Echoes the same class of mistake as CVE-2013-6462 (libXfont sscanf %s). */
    ssize_t n = read(0, buffer, 200);
    (void)n;

    return authenticated;
}

int main(void) {
    if (authenticate()) {
        printf("\n*** ACCESS GRANTED ***\n");
        return 0;
    } else {
        printf("\n*** ACCESS DENIED ***\n");
        return 1;
    }
}
