/*
 * vuln.c
 *
 * Vulnerable program for Lab 2 — Part C
 * Demonstrates control flow hijacking via saved return address overwrite.
 * Contains a hidden win() function that is NEVER called from main(); the
 * student must redirect execution to it by overwriting the saved EIP.
 *
 * Compile (from project root):
 *   gcc -m32 -fno-stack-protector -z execstack -no-pie -g -O0 \
 *       -o vuln source/vuln.c
 *
 * Run normally:
 *   echo "hello" | ./vuln
 *
 * Exploit (after finding OFFSET and WIN_ADDR via gdb / objdump):
 *   python3 -c "import sys; sys.stdout.buffer.write(
 *       b'A'*OFFSET + bytes.fromhex('WIN_ADDR_LE'))" | ./vuln
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* The "secret" function — never called from main(). The student's job is
 * to make the program execute this anyway by hijacking control flow. */
void win(void) {
    printf("\n[!!!] CONGRATULATIONS — control flow hijacked!\n");
    printf("[!!!] Spawning a shell as proof of exploitation...\n");
    fflush(stdout);
    system("/bin/sh");
    exit(0);
}

void vulnerable(void) {
    char buffer[64];

    /* Diagnostic prints so the student knows where to aim */
    printf("[info] buffer is at %p\n", (void*)buffer);
    printf("[info] win()  is at %p\n", (void*)win);
    printf("Enter your input: ");
    fflush(stdout);

    /* UNSAFE: reads up to 200 bytes into a 64-byte buffer */
    ssize_t n = read(0, buffer, 200);
    (void)n;

    printf("You entered: %s\n", buffer);
}

int main(void) {
    vulnerable();
    printf("vulnerable() returned safely. (If you see this, the exploit FAILED.)\n");
    return 0;
}
