# Makefile — Secure Coding Lab 3: Countermeasures
#
# The whole point of this lab: SAME source, DIFFERENT flags.
# Each target below builds auth_demo / vuln with one protection turned on or
# off, so you can re-run your Lab 2 payload and watch the defense react.
#
# Usage:
#   make unprotected   # Lab 2 baseline — every defense OFF (exploit works)
#   make canary        # Part B — stack canary (SSP) ON
#   make nx            # Part C — NX/DEP ON (stack non-executable)
#   make pie           # Part D — PIE ON (works with runtime ASLR)
#   make all
#   make clean

CC      = gcc
COMMON  = -m32 -g -O0
SRC     = source

# ---- Part A: Lab 2 baseline. All defenses disabled. ----
# -fno-stack-protector : no canary
# -z execstack         : stack is executable (shellcode runs)
# -no-pie              : fixed load address (hardcoded addresses are stable)
UNPROT  = $(COMMON) -fno-stack-protector -z execstack -no-pie

# ---- Part B: Stack canary (SSP) ON, everything else still off ----
# -fstack-protector-all : place a canary in every function
CANARY  = $(COMMON) -fstack-protector-all -z execstack -no-pie

# ---- Part C: NX/DEP ON (no -z execstack), canary still off ----
# Omitting -z execstack lets the linker mark the stack non-executable (NX).
NX      = $(COMMON) -fno-stack-protector -no-pie

# ---- Part D: PIE ON so the loader can apply full ASLR to the binary ----
# (PIE is the binary-side requirement; ASLR itself is the kernel sysctl.)
PIE     = $(COMMON) -fno-stack-protector -z execstack -fpie -pie

.PHONY: all clean unprotected canary nx pie

all: unprotected canary nx pie

unprotected:
	$(CC) $(UNPROT) $(SRC)/auth_demo.c -o auth_demo_unprot
	$(CC) $(UNPROT) $(SRC)/vuln.c      -o vuln_unprot

canary:
	$(CC) $(CANARY) $(SRC)/auth_demo.c -o auth_demo_canary
	$(CC) $(CANARY) $(SRC)/vuln.c      -o vuln_canary

nx:
	$(CC) $(NX) $(SRC)/auth_demo.c -o auth_demo_nx
	$(CC) $(NX) $(SRC)/vuln.c      -o vuln_nx

pie:
	$(CC) $(PIE) $(SRC)/auth_demo.c -o auth_demo_pie
	$(CC) $(PIE) $(SRC)/vuln.c      -o vuln_pie

clean:
	rm -f auth_demo_* vuln_*
