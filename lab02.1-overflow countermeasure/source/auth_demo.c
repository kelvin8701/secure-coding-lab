/* auth_demo.c  —  Secure Coding Lab 3 (carried over from Lab 2)
 *
 * Same vulnerable program you exploited in Lab 2. In Lab 3 you will NOT
 * change this code at all. You will only change the COMPILER FLAGS used to
 * build it, and observe how the countermeasures react to the very same
 * exploit input you already crafted.
 *
 * Vulnerability: gets() writes into buf[] with no bounds check, so an
 * over-long input overflows buf and overwrites the adjacent 'authenticated'
 * flag (and, if long enough, the saved return address).
 */
#include <stdio.h>
#include <string.h>

int authenticate(void) {
    char buf[64];
    int  authenticated = 0;      /* 0 = denied, anything else = granted */

    printf("Password: ");
    gets(buf);                   /* <-- the classic vulnerable call */

    if (strcmp(buf, "s3cr3t") == 0)
        authenticated = 1;

    return authenticated;
}

int main(void) {
    if (authenticate()) {
        printf("*** ACCESS GRANTED ***\n");
    } else {
        printf("Access denied.\n");
    }
    return 0;
}
