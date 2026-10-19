class MyArrayLinearList:
    def __init__(self):
        self.element = []
    def add(self, val):
        self.element.append(val)
    def __str__(self):
        return str(self.element)
    def max(self):
        if len(self.element) == 0:
            print ("жагаалт хоосон байна")
            return None
        largest = self.element[0]
        for num in self.element:
            if num > largest:
                largest = num
        return largest
    def min(self):
        if len(self.element) == 0:
            print ("жагсаалт хоосон байна")
            return None
        return min(self.element)
    def sum(self):
        total = 0
        for num in self.element:
            total += num
        return total
    def average(self):
        if len(self.element) == 0:
            print ("жагсаалт хоосон байна")
            return None
        return self.sum() / len(self.element)
    def sort(self):
        self.element.sort()
    def removeOdd(self):
        removedOdd_numbers = []
        for num in self.element:
            if num % 2 ==0:
                removedOdd_numbers.append(num)
        self.element = removedOdd_numbers
    
def run_array_list():
    my_list = MyArrayLinearList()
    while True:
        print("\n таны сонгож болох сонголтууд")
        print("\n 1. тоо нэмэх \n 2. жагсаалт харах \n 3. хамгийн их (max) олох \n 4. хамгийн бага (min) олох \n 5. нийлбэр (sum) олох \n 6. дундаж (average) олох \n 7. эрэмбэлэх (sort) \n 8. сондгой тоог устгах (removeOdd) \n 0. гарах")
        choice = input("songoltoo hiine uu 0-8 dugaariin hoorond: ").strip()
        if choice == "":
            continue
        elif choice == "1":
            inputs = input("нэмэх тоонуудаа зайгаар тусгаарлан оруулна уу:").split()
            if not inputs:
                print("хоосон утга орууллаа")
                continue
            added = []
            for item in inputs:
                try:
                    val = int(item)
                    my_list.add(val)
                    added.append(val)
                except ValueError:
                    print(f"'{item}' n бүхэл тоо биш тул хаслаа")
            if added:
                print(f"{added} амжилттай боллоо")
        elif choice == "2":
            print (f"жагсаалт {my_list}")
        elif choice == "3":
            print (f"хамгийн их утгэ: {my_list.max()}")
        elif choice == "4":
            print (f"хамгийн бага утга {my_list.min()}")
        elif choice == "5":
            print (f"нийлбэр: {my_list.sum()}")
        elif choice == "6":
            print (f" дундаж: {my_list.average()}")
        elif choice == "7":
            my_list.sort()
            print (f"эрэмбэлэгдсэн: {my_list}")
        elif choice == "8":
            my_list.removeOdd()
            print(f"сондгой тоонуудыг устгасан: {my_list}")
        elif choice == "0":
            print("program дууслаа")
            break
        else: 
            print ("бураа сонголт хийлээ 0-8 ийн хооронд хийнэ үү")
if __name__=="__main__":
    run_array_list()

