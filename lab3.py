class Node:
    def __init__(self, element=None, next=None):
        self.element = element
        self.next = next
class MyChain:
    def __init__(self):
        self.first_node = None
        self.size = 0
    def add(self, element):
        new_node = Node(element)
        if self.first_node is None:
            self.first_node = new_node
        else:
            current = self.first_node
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1
    def __str__(self):
        elements = []
        current = self.first_node
        while current is not None:
            elements.append(current.element)
            current = current.next
        return str(elements)
    def toArray(self):
        array = []
        item = self.first_node
        while item is not None:
            array.append(item.element)
            item = item.next
        return array
    def addRange(self, elements):
        for x in elements:
            self.add(x)

    def intersection(self, chain):
        result_chain = MyChain()
        other_array = chain.toArray()
        current = self.first_node
        while current is not None:
            if current.element in other_array:
                result_chain.add(current.element)
            current = current.next
        return result_chain
    def union(self, chain):
        result_chain = MyChain()
        current = self.first_node
        while current is not None:
            result_chain.add(current.element)
            current = current.next

        other_array = chain.toArray()
        existing_elements = (result_chain.toArray())
        for elem in other_array:
            if elem not in existing_elements:
                result_chain.add(elem)
                existing_elements.append(elem)
        return result_chain

def main():
    chain1 = MyChain()
    chain2 = MyChain()

    print("=== ХОЛБООС ЖАГСААЛТЫН ТУРШИЛТ (LAB 2) ===")

    while True:
        print("\nСонголтууд:")
        print("1. Жагсаалт 1-д тоо нэмэх (addRange)")
        print("2. Жагсаалт 2-т тоо нэмэх (addRange)")
        print("3. Жагсаалтуудыг харах")
        print("4. Массив руу хөрвүүлэх (toArray)")
        print("5. Огтлолцол олох (intersection)")
        print("6. Нэгдэл олох (union)")
        print("0. Гарах")

        choice = input("\nСонголтоо хийнэ үү (0-6): ").strip()

        # Хоосон Enter дарвал юу ч хийхгүй дараагийн асуулт руу шилжинэ
        if not choice:
            continue

        if choice == "1":
            inp = input(
                "Жагсаалт 1-д нэмэх тоонуудыг зайгаар зааглан оруулна уу: "
            ).strip()
            if not inp:
                print("Анхаар: Ямар ч утга оруулсангүй.")
                continue

            items = []
            for x in inp.split():
                try:
                    items.append(int(x))
                except ValueError:
                    print(f"'{x}' нь бүхэл тоо биш тул орхилоо.")

            if items:
                chain1.addRange(items)
                print(f"Жагсаалт 1-д {items} амжилттай нэмэгдлээ.")
            else:
                print("Нэмэгдэх зөв тоо олдсонгүй.")

        elif choice == "2":
            inp = input(
                "Жагсаалт 2-т нэмэх тоонуудыг зайгаар зааглан оруулна уу: "
            ).strip()
            if not inp:
                print("Анхаар: Ямар ч утга оруулсангүй.")
                continue

            items = []
            for x in inp.split():
                try:
                    items.append(int(x))
                except ValueError:
                    print(f"'{x}' нь бүхэл тоо биш тул орхилоо.")

            if items:
                chain2.addRange(items)
                print(f"Жагсаалт 2-т {items} амжилттай нэмэгдлээ.")
            else:
                print("Нэмэгдэх зөв тоо олдсонгүй.")

        elif choice == "3":
            print(f"\nЖагсаалт 1: {chain1}")
            print(f"Жагсаалт 2: {chain2}")

        elif choice == "4":
            print(f"\nЖагсаалт 1 (Array): {chain1.toArray()}")
            print(f"Жагсаалт 2 (Array): {chain2.toArray()}")

        elif choice == "5":
            inter = chain1.intersection(chain2)
            print(f"\nОгтлолцол (intersection): {inter}")

        elif choice == "6":
            u = chain1.union(chain2)
            print(f"\nНэгдэл (union): {u}")

        elif choice == "0":
            print("Програм дууслаа.")
            break
        else:
            print("Буруу сонголт хийлээ. 0-6 хооронд сонгоно уу.")

if __name__ =="__main__":
    main()
