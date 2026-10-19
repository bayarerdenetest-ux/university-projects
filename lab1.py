def gpa_calculator():
    while True:
        try:
            n = int(input("Хичээлийн тоог оруулна уу: "))
            if n > 0:
                break
            print("Хичээлийн тоо заавал 1 эсвэл түүнээс дээш байх ёстой")
        except ValueError:
            print("Буруу утга! Заавал бүхэл тоо оруулна уу.")

    total_grad = 0.0
    total_credits = 0.0

    for i in range(1, n + 1):
        print(f"\n--- {i}-р хичээл ---")
        
        while True:
            try:
                credit = float(input(f"{i}-р хичээлийн кредит: "))
                if 6> credit > 0:
                    break
                print("Кредит 0-ээс их 6-аас бага эерэг тоо байх ёстой!")
            except ValueError:
                print("Буруу утга Кредитийг тоогоор оруулна уу.")

        while True:
            try:
                grad = float(input("Авсан дүн (%) [0-100]: "))
                if 0 <= grad <= 100:
                    break
                print("Авсан дүн заавал 0-ээс 100-гийн хооронд байх ёстой")
            except ValueError:
                print("Буруу утга Дүнг тоогоор оруулна уу.")

        if grad >= 95:
            gpa_point = 4.0
        elif grad >= 90:
            gpa_point = 3.7
        elif grad >= 87:
            gpa_point = 3.3
        elif grad >= 83:
            gpa_point = 3.0
        elif grad >= 80:
            gpa_point = 2.7
        elif grad >= 77:
            gpa_point = 2.3
        elif grad >= 73:
            gpa_point = 2.0
        elif grad >= 70:
            gpa_point = 1.7
        elif grad >= 65:
            gpa_point = 1.4
        elif grad >= 60:
            gpa_point = 1.0
        else:
            gpa_point = 0.0

        total_grad += credit * gpa_point
        total_credits += credit

    final_gpa = total_grad / total_credits
    print("\n=========================")
    print(f"Нийт кредит: {total_credits}")
    print(f"Таны GPA: {final_gpa:.2f}")
if __name__ == "__main__":
    gpa_calculator()