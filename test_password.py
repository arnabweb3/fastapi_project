from security import hash_password, verify_password

password = "Example-Password-123!"

hashed = hash_password(password)

print("Stored hash:", hashed)
print("Correct password:", verify_password(password, hashed))
print("Wrong password:", verify_password("wrong-password", hashed))

assert hashed != password
assert verify_password(password, hashed)
assert not verify_password("wrong-password", hashed)
