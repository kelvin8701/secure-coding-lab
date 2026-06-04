#!/usr/bin/env bash
# setup.sh — Lab 2 environment setup for Ubuntu 22.04 LTS (VirtualBox VM)
# Run once before the first session. Requires sudo.

set -e

echo "=== Lab 2 environment setup ==="

# 1. Install required packages
echo "[1/4] Installing packages..."
sudo apt-get update -qq
sudo apt-get install -y \
    gcc \
    gcc-multilib \
    g++-multilib \
    gdb \
    make \
    python3 \
    binutils \
    elfutils \
    file \
    less

# 2. Verify 32-bit compilation
echo "[2/4] Verifying 32-bit toolchain..."
TMP=$(mktemp -d)
cat > "$TMP/hello.c" <<EOF
#include <stdio.h>
int main(void) { printf("32-bit OK\n"); return 0; }
EOF
gcc -m32 -o "$TMP/hello" "$TMP/hello.c"
"$TMP/hello"
rm -rf "$TMP"

# 3. Disable ASLR (Address Space Layout Randomization) — needed so addresses
#    are stable across runs while students learn exploitation. This is a
#    deliberate weakening for a teaching environment; never do this on a
#    production machine.
echo "[3/4] Disabling ASLR..."
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space > /dev/null
echo "    Current value: $(cat /proc/sys/kernel/randomize_va_space) (0 = disabled)"

# 4. Quick smoke test
echo "[4/4] Smoke test..."
gcc --version | head -1
gdb --version | head -1
python3 --version

echo ""
echo "=== Setup complete ==="
echo ""
echo "If you reboot, re-disable ASLR with:"
echo "  echo 0 | sudo tee /proc/sys/kernel/randomize_va_space"
echo ""
echo "Then build the lab programs with:"
echo "  make"
