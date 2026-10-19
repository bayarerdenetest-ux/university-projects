# class Oyutan:
#     pass
# o1 = Oyutan()
# o2 = Oyutan()
# print(type(o1))
# print(o1 is o2)

# class Oyutan:
#     def __init__ (self, ner, nas, dundaj):
#         self.ner = ner 
#         self.nas = nas
#         self.dundaj = dundaj
#     def tanilts(self):
#         return f"sainuu , namaig {self.ner} gedeg, {self.nas} nastai"
# o = Oyutan("bold", 21, 3.1)
# print(o.tanilts())

# class Oyutan:
#     surguuli = "SHUTIS"
#     def __init__(self, ner):
#         self.ner = ner
# a = Oyutan("saraa")
# b = Oyutan("dorj")
# print(a.surguuli, b.surguuli)
# Oyutan.surguuli = "MUIS"
# print(a.surguuli)
# print(a.surguuli, b.surguuli)

# class Toolur:
#     too = 0
#     def __init__(self):
#         Toolur.too += 1
#     def instance_method(self):
#         return f"obect: {self}"
#     @classmethod
#     def heden_object(cls):
#         return f"niit {cls.too} obect uusne"
#     @staticmethod
#     def tuslamj():
#         return"ene bol function"
# Toolur(); Toolur()
# print(Toolur.heden_object())
# print(Toolur.tuslamj())

# class Dans:
#     def __init__(self, uldegdel):
#         self.__uldegdel = uldegdel
#     def nemeh(self, dun):
#         if dun <= 0:
#             raise ValueError("dun eyreg garah")
#         self.__uldegdel += dun
#     def harah(self):
#         return self.__uldegdel
# d = Dans(1000)
# d.nemeh(500)
# print(d.harah())
# print(d._Dans__uldegdel)

# class Temperatur:
#     def __init__(self, celsius=0):
#         self.celsius = celsius
    
#     @property
#     def celsius(self):
#         return self._celsius
#     @celsius.setter
#     def celsius(self, utga):
#         if utga < - 273.15:
#             raise ValueError("unemlehui tegees baga")
#         self._celsius = utga

#     @property
#     def fahrenheit(self):
#         return self._celsius * 9/5 + 32
# t = Temperatur(25)
# print(t.fahrenheit)
# t.celsius = 30

# class Amitan:
#     def __init__(self, ner):
#         self.ner = ner

#     def duu_garga(self):
#         return "..."
# class Nohoi(Amitan):
#     def duu_garga(self):
#         return "hov hov"
# class Muur(Amitan):
#     def __init__(self, ner, ongo):
#         super().__init__(ner)
#         self.ongo = ongo
#     def duu_garga(self):
#         return "Miaw"
# amitad = [Nohoi("banhar"), Muur("miis", "har")]
# for a in amitad:
#     print(a.ner, "_", a.duu_garga())
# print(isinstance(amitad[0], Amitan))
# print(issubclass(Nohoi, Amitan))
    
# class Toolur:
#     too = 0
#     def  __init__(self):
#         Toolur.too +=1
#     def instance_method(self):
#         return f"obect: {self}"
#     @classmethod
#     def heden_object(cls):
#         return f"niit {cls.too} object uussen"
#     @staticmethod
#     def tuslamj():
#         return "ene bol tuslamj"
# Toolur(); Toolur()
# print(Toolur.heden_object())
# print(Toolur.tuslamj())

# class Ognoo:
#     def __init__(self, jil, sar, odor):
#         self.jil, self.sar, self.odor = jil, sar, odor 
#     @classmethod
#     def string_ees(cls, s):
#         jil, sar, odor = map(int, s.split("-"))
#         return cls(jil, sar, odor)
# d= Ognoo.string_ees("2026-06-10")
# print(d.jil)

# class Vector:
#     def __init__(self, x, y):
#         self.x, self.y = x, y
#     def __repr__(self):
#         return f"Vector({self.x}, {self.y})"
#     def __add__(self, other):
#         return Vector(self.x + other.x, self.y + other.y)
#     def __mul__(self, k):
#         return Vector(self.x * k, self.y * k)
#     def __eq__(self, other):
#         return(self.x, self.y) == (other.x, other.y)
#     def __abs__(self):
#         return (self.x ** 2 + self.y ** 2) **0.5
# v = Vector(1, 2) + Vector(3, 4)
# print(v, abs(v), v == Vector(4, 6))

# class Vector:
#     def __init__(self, x, y):
#         self.x, self.y = x, y
#     def __repr__(self):
#         return f"Vector({self.x}, {self.y})"
#     def __add__(self, other):
#         return Vector(self.x + other.x, self.y + other.y)
#     def __mul__(self, k): # скаляр үржвэр
#         return Vector(self.x * k, self.y * k)
#     def __eq__(self, other):
#         return (self.x, self.y) == (other.x, other.y)
#     def __abs__(self):
#         return (self.x ** 2 + self.y ** 2) ** 0.5
# v = Vector(1, 2) + Vector(3, 4)
# print(v, abs(v), v == Vector(4, 6))

# class Shelf:
#     def __init__(self, books):
#         self.books = books
#     def __len__(self):
#         return len(self.books)
#     def __getitem__(self, index):
#         return self.books[index]
#     def __contains__(self, book_name):
#         return book_name in self.books
# minii_taviur = Shelf(["Tungalag Tamir", "Nogoon mori", "Ulemjiin chanar"])
# print(len(minii_taviur))
# print(minii_taviur[0])
# print(minii_taviur[1])
# baigaa_uu = "Nogoon mori" in minii_taviur
# print(baigaa_uu)

# class A:
#     def hello(self):
#         return "A"
# class B(A):
#     def hello(self):
#         return "B"
# class C(A):
#     def hello(self):
#         return "C"
# class D(B,C):
#     pass
# print(D().hello())
# print(D.__mro__)

# class Amitan:
#     def __init__(self, ner):
#         self.ner = ner

#     def duu_garga(self):
#         return "..."
# class Nohoi(Amitan):
#     def duu_garga(self):
#         return "hov hov"
# class Muur(Amitan):
#     def __init__(self, ner, ongo):
#         super().__init__(ner)
#         self.ongo = ongo 
#     def duu_garga(self):
#         return "miau"
# amitad = [Nohoi("banhar"), Muur("miis", "har")]
# for a in amitad:
#     print (a.ner, "-", a.duu_garga())
# print(isinstance(amitad[0], Amitan))
# print(issubclass(Nohoi, Amitan))




# class Product:
#     def __init__(self, name, price):
#         self.name = name
#         self.price = price

#     def __eq__(self, other):
#         if not isinstance(other, Product):
#             return NotImplemented
#         return self.price == other.price

#     def __lt__(self, other):
#         if not isinstance(other, Product):
#             return NotImplemented
#         return self.price < other.price


# inventory = [
#     Product("Laptop", 1200),
#     Product("Mouse", 25),
#     Product("Monitor", 300)
# ]

# sorted_inventory = sorted(inventory)

# for prod in sorted_inventory:
#     print(f"{prod.name}: ${prod.price}")

import json
class JsonMixin:
    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)
    
class Hereglegch(JsonMixin):
    def __init__(self, ner, email):
        self.ner, self.email = ner, email
print(Hereglegch("Oyun", "o@must.edu.mn").to_json())