import bcrypt

# User ka input password (yeh normally user se form input ya API se aata hai)
input_password = "admin123"

# Hashed password jo database mein store kiya gaya hai
stored_hashed_password = b"$2b$12$FETzpaBDw53aEmcTLnQDIOPCDynabplz/lbcKGcb6A56uIxbBXPCi"

# Verify karein ke user ka input password correct hai ya nahi
if bcrypt.checkpw(input_password.encode(), stored_hashed_password):
    print("Password match!")
else:
    print("Incorrect password!")
