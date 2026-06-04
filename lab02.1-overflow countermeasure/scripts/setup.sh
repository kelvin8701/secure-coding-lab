#!/usr/bin/env bash
# setup.sh — Secure Coding Lab 3 environment preparation
#
# Run ONCE before the session (pre-lab). Builds on the Lab 1/Lab 2 setup;
# the only genuinely new tool is `checksec`, which reports at a glance which
# protections a binary was compiled with.
set -e

echo "=== Lab 3 setup: verifying toolchain ==="

# --- 1. Core toolchain (already present from Lab 1/2, verified here) ---
NEED="gcc gdb objdump readelf python3 make"
for t in $NEED; do
    if ! command -v "$t" >/dev/null 2>&1; then
        echo "[!] Missing: $t  — install with: sudo apt install build-essential gdb binutils python3"
        exit 1
    fi
done
echo "[ok] core toolchain present"

# --- 2. 32-bit support (needed for -m32) ---
if ! dpkg -l | grep -q gcc-multilib; then
    echo "[*] Installing gcc-multilib for 32-bit builds..."
    sudo apt update && sudo apt install -y gcc-multilib
fi
echo "[ok] 32-bit build support present"

# --- 3. checksec (the one new tool for this lab) ---
if ! command -v checksec >/dev/null 2>&1; then
    echo "[*] Installing checksec..."
    sudo apt update && sudo apt install -y checksec
fi
echo "[ok] checksec present:  $(checksec --version 2>&1 | head -n1 || echo installed)"

# --- 4. Show current ASLR state (do NOT change it here; the lab does that) ---
echo ""
echo "=== Current ASLR state ==="
state=$(cat /proc/sys/kernel/randomize_va_space)
case "$state" in
  0) echo "randomize_va_space = 0  (ASLR OFF — this is the Lab 2 baseline)";;
  1) echo "randomize_va_space = 1  (partial ASLR)";;
  2) echo "randomize_va_space = 2  (full ASLR — default on a fresh boot)";;
esac
echo ""
echo "Reminder — the lab will toggle ASLR with these commands:"
echo "  Disable: echo 0 | sudo tee /proc/sys/kernel/randomize_va_space"
echo "  Enable : echo 2 | sudo tee /proc/sys/kernel/randomize_va_space"
echo "(Either setting resets to the kernel default on reboot.)"

echo ""
echo "=== Building all four protection configurations ==="
make all
echo ""
echo "[ok] Setup complete. Binaries built:"
ls -1 auth_demo_* vuln_*
