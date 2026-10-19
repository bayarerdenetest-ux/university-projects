from lab1 import gpa_calculator
from MyArrayLinearList import run_array_list
from lab3 import main


def main_menu():
    print("сайн байна уу? \n та үндсэн цэсэд холбогдлоо")
    while True:
        print(
            "\n таны сонгох боломжтой сонголтууд. \n 1. голч дүн тооцоологч \n 2. array_linear_list функц \n 3. гинжин холбоос Mychain \n 0. гарах \n /дугаарыг оруулна/"
        )
        try:
            user_input = int(input("ашиглахыг хүсэж буй функцаа сонгон уу: "))
            if user_input == 1:
                gpa_calculator()
            elif user_input == 2:
                run_array_list()
            elif user_input == 3:
                main()
            elif user_input == 0:
                print("үйлдэл дууслаа баяртай")
                break
            else:
                print("Сонгох боломжтой сонголтоос дугаарыг нь оруулна уу.")
        except ValueError:
            print("\n буруу утга байна. Сонголтоо зөв хийнэ үү")


if __name__ == "__main__":
    main_menu()