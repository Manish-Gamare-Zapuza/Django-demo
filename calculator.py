def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error is created. Division by zero."
    return a / b


def modulus(a, b):
    if b == 0:
        return "Error! Division by zero."
    return a % b


def power(a, b):
    return a ** b


while True:
    print("\n===== PYTHON CALCULATOR =====")
    print(" Addition")
    print(" Subtraction")
    print(" Multiplication")
    print(" Division")
    print(" Modulus")
    print(" Power")
    print(" Exit")

    choice = input("Enter your choice upto 7: ")

    if choice == "7":
        print("Thank you for using the calculator ")
        break



    if choice in ["1", "2", "3", "4", "5", "6"]:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        if choice == "1":
            print("Result:", add(num1, num2))


        elif choice == "2":
            print("Result:", subtract(num1, num2))
        elif choice == "3":
            print("Result:", multiply(num1, num2))
        elif choice == "4":
            print("Result:", divide(num1, num2))
        elif choice == "5":
            print("Result:", modulus(num1, num2))
        elif choice == "6":
            print("Result:", power(num1, num2))





    else:
        print("Invalid choice! Please enter a number between 1 and 7 ")