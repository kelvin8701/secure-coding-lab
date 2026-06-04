/*
 * heap_demo.c
 *
 * Heap overflow demonstration for Lab 2 — Part D (instructor demo).
 * Mirrors the user/adminuser example from Aspinall's Lecture 4.
 *
 * Note: chunks are sized to 32 bytes so the adjacent buffer's data
 * region (not its glibc metadata) is the corruption target. Modern
 * glibc detects header corruption and aborts immediately.
 *
 * Compile:
 *   gcc -m32 -fno-stack-protector -no-pie -g -O0 \
 *       -o heap_demo source/heap_demo.c
 *
 * Normal run:
 *   ./heap_demo frank
 *
 * Heap corruption (overflows user buffer into adminuser data):
 *   ./heap_demo $(python3 -c "print('A'*48 + 'EVIL')")
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUF_SIZE 32

int main(int argc, char *argv[]) {
    char *user      = (char*)malloc(BUF_SIZE);
    char *adminuser = (char*)malloc(BUF_SIZE);

    if (!user || !adminuser) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    }

    /* Set the admin first — it represents a privileged identity */
    strcpy(adminuser, "root");

    /* Then copy user input into the lower-priority buffer */
    if (argc > 1) {
        strcpy(user, argv[1]);   /* UNSAFE — no length check */
    } else {
        strcpy(user, "guest");
    }

    printf("user      is at %p, contains: %s\n", user,      user);
    printf("adminuser is at %p, contains: %s\n", adminuser, adminuser);
    printf("distance  = %ld bytes\n", adminuser - user);

    /* Intentionally no free() — modern glibc detects heap corruption on
     * free() and aborts. The demo's point is the data corruption above. */
    return 0;
}
