# Makefile — Lab 2 Stack Overflow Exploitation
#
# Builds all vulnerable programs with security features disabled, exactly
# as needed for the lab exercises. DO NOT use these flags in real software.

CC      = gcc
CFLAGS  = -m32 -fno-stack-protector -z execstack -no-pie -g -O0 -w
SRCDIR  = source

PROGS = auth_demo vuln heap_demo

all: $(PROGS)

auth_demo: $(SRCDIR)/auth_demo.c
	$(CC) $(CFLAGS) -o $@ $<

vuln: $(SRCDIR)/vuln.c
	$(CC) $(CFLAGS) -o $@ $<

heap_demo: $(SRCDIR)/heap_demo.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGS)

.PHONY: all clean
