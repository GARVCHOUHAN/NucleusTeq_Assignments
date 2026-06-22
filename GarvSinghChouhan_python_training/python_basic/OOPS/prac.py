# # num = int(input("Enter a number: "))
# # try:
# #     x= 10/num
# # except Exception as e:
# #     print("Error occured", e)    


# # raise is generally used to validate the input and raise an error if the input is not valid. It is also used to raise an error when a certain condition is not met.

# # lst = [1, 2, 3, 4, 5]

# # it = iter(lst)

# # print(next(it))
# # print(next(it))
# # print(next(it))
# # print(it)
# # print(next(it))

# # list = [x*x for x in range(3)]

# # g = (x*x for x in range(3))
# # print(list)
# # print(next(g))
# # print(next(g))
# # print(next(g))


# # add = lambda x,y: x+y
# # subtract = lambda x,y : x-y

# # nums = [1,2,3,4,5]
# # squared =  map(lambda x: x**2 , nums)
# # print(list(squared))
# # print(squared)

# from functools import reduce
# nums = [1, 2, 3, 4, 5]
# sum_all = reduce(lambda x,y: x+y,nums)
# print(sum_all)

# filtered = filter(lambda x:x%2 == 0,nums)
# print(list(filtered))

# #  if we want to create a test file make sure it starts with test_ and 
# # the function name also starts with test_ and we can use assert statement
# # to check the expected output with the actual output. We can run the test 
# # file using pytest command in the terminal.
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
ones = np.ones((2,3))
maxi = arr.max()
print(maxi)
