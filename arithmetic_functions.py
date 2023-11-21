#Exercise6:arithmetic_functions.py

def display_num(num1, num2):
  sum = num1 + num2
  difference = num1 - num2
  quotient = num1 / num2
  product = num1 * num2

  print("The sum of", num1 ,"and" ,num2, "is =", sum)
  print("The difference of", num1, "and", num2, "is =", difference)
  print("The quotient of", num1, "and", num2, "is =", quotient)
  print("The product of", num1, "and", num2, "is =", product)

num1 = int(input("Enter Num1: "))
num2 = int(input("Enter Num2: "))
display_num(num1, num2)
