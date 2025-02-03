import vqsx

# Test program for builder

b = vqsx.Builder()
for _ in range(9):
    b.nop()
print(f"u {b.dump().decode('utf-8')}")
print(f"h {b.dump().hex()}")