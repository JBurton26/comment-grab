import os
import bcrypt
da = os.getcwd()+"/test.txt"
try:
    f = open(da, "x")
    f.close()
except Exception as ex:
    print(ex)
print("Done")
