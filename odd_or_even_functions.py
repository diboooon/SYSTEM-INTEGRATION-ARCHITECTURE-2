#Exercise7: Odd_or_even_functions.py

def even_or_odd():
    value = input("Enter a Number: ")
    if int(value) % 2 == 0:
        print(f"{value} is an even number")
    else:
        print(f"{value} is an odd number")
even_or_odd()
