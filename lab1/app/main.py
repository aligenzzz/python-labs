from functions import my_func1, my_func2

# 1.)
print("Hello world!")

# 2.)
print(my_func1(3, 2, "add"))
print(my_func1(8, 2, "sub"))
print(my_func1(6, 4, "mul"))
print(my_func1(6, 0, "div"))
print(my_func1(7, 7, "zzzz"))
print(my_func1("ghgh", "l", "mul"))

# 3.)
list2 = my_func2([number for number in range(1, 20)])
print(list2)

