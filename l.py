import random, string

length = 12

stringg = "".join(random.choices(string.ascii_letters + string.digits, k=length))
print(stringg)