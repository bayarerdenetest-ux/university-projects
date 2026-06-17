# 1
# class Oyutan:
#     def __init__(self, ner, nas, dundaj_onoo):
#         self.ner =ner 
#         self.nas = nas
#         self.dundaj_onoo = nas
#     def medeelel(self):
#         return f"{self.ner} {self.nas} {self.dundaj_onoo}"
# oyutnuud = [Oyutan("bold", 20, 4.0), Oyutan("oyun", 21, 3.4), Oyutan("temuulen", 24, 3.1)]
# for o in oyutnuud:
#     print(o.medeelel())

# 2
# class Calculator:
#     def nemeh(self, a, b):
#         return a + b
#     def hasah(self, a, b):
#         return a - b
#     def urjih(self, a, b):
#         return a *b
#     def huvaah(self, a, b):
#         if b == 0:
#             return "huvaagdahgui"
#         return a/b
# if __name__ == "__main__":
#     bodogch = Calculator()
#     x, y = 12, 4
#     print(f"{x} + {y} = {bodogch.nemeh(x, y)}")   
#     print(f"{x} - {y} = {bodogch.hasah(x, y)}")   
#     print(f"{x} * {y} = {bodogch.urjih(x, y)}")   
#     print(f"{x} / {y} = {bodogch.huvaah(x, y)}")

# 3
# class Rectangle:
#     def __init__(self, urt, orgon):
#         self.urt = urt 
#         self.orgon = orgon
#     def talbai(self):
#         return self.urt *self.orgon
#     def perimetr(self):
#         return 2 * (self.urt + self.orgon)
#     def kvadrat_mon_uu(self):
#         if self.urt == self.orgon:
#             return True
#         else:
#             return False
# if __name__ == "__main__":
#     ts1 = Rectangle(5, 3)
#     print(f"ts1 (урт: {ts1.urt}, өргөн: {ts1.orgon}) -> Квадрат мөн үү?: {ts1.kvadrat_mon_uu()}") 

#     ts2 = Rectangle(4, 4)
#     print(f"ts2 (урт: {ts2.urt}, өргөн: {ts2.orgon}) -> Квадрат мөн үү?: {ts2.kvadrat_mon_uu()}")

# 4
# class Dans:
#     def __init__(self, ehnii_uldegdel):
#         self.uldegdel = ehnii_uldegdel
#     def oruulah(self, dun):
#         self.uldegdel += dun
#         print(f"dansand {dun} orloo. odoonii uldegdel {self.uldegdel} bain")
#     def avah(self, dun):
#         if dun > self.uldegdel:
#             print(f"anhaaruulga: dansnii uldegdel hureltsehgui bain. uldegdel{self.uldegdel}")
#         else:
#             self.uldegdel -= dun
#             print(f"dansand {dun} avah. odoonii uldegdel {self.uldegdel} bain")
# if __name__ == "__main__":
#     minii_dans = Dans(5000)
#     minii_dans.oruulah(1000)
#     minii_dans.avah(2000)
#     minii_dans.avah(10000)

# 5
# class Mashin:
#     Mashin_niit = 0
#     def __init__(self):
#         Mashin.Mashin_niit += 1
#     @classmethod
#     def heden_mashin(cls):
#         return f"niit {cls.Mashin_niit} mashin bain"
# Mashin(); Mashin()
# print(Mashin.heden_mashin())

# 6
# class Nom:
#     def __init__(self, ner, zohiogch, une):
#         self.ner = ner 
#         self.zohiogch = zohiogch
#         self.une = une 
#     def __str__(self):
#         return f"<<{self.ner}>>, zohiogch {self.zohiogch}, une {self.une}"

# nom = Nom("lambaguian nulmis", "Hen negen mongol zohiolch", 45000)
# print(nom)

# 7
# class Tseg:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#     def shiljuuleh(self, dx, dy):
#         self.x += dx
#         self.y += dy
#     def zai(self, busad_tseg):
#         zaur_x_kvadrat = (self.x - busad.x - self.x)**2
#         zaur_y_kvadrat = (self.y - busad.y - self.y)**2

#         butsah_zai = math.sqrt(zaur_x_kvadrat + zaur_y_kvadrat)
#         return butsah_zai
#     def __str__(self):
#         return f"({self.x}, {self.y})"

# if __name__ == "__main__":
#     A = Tseg(1, 2)
#     B = Tseg(4, 6)
    
#     print(f"anhnii A tseg: {A}")  # Цэг(1, 2)
#     print(f"anhnii b tseg: {B}")  # Цэг(4, 6)
    
#     print(f"a b hoorondiin zai: {A.zai(B)}")  # Үр дүн: 5.0
    
#     A.shiljuuleh(2, 3)
#     print(f"shiljsen a zai : {A}")

# 8
# class Baraa:
#     def __init__(self, ner, une, too):
#         self.ner = ner 
#         self.une = une
#         self.too = too
#     def niit_une(self):
#         return self.une * self.too
#     def hyamdrah(self, huvi):
#         return self.une * huvi / 100
# if __name__ == "__main__":
#     zahialga = Baraa("talh", 1500, 5)
#     print(f"baraa {zahialga.ner}, niit une {zahialga.niit_une()}, hymdral {zahialga.hyamdrah(15)}")

# 9
# class Utas:
#     def __init__(self):
#         self.jagsaalt: list[dict[str, str]] = []
#     def nemeh(self, ner: str, dugaar:str):
#         self.jagsaalt.append({"ner": ner, "dugaar": dugaar})
#     def haih(self, ner:str):
#         for item in self.jagsaalt:
#             if item["ner"].lower() == ner.lower():
#                 return item["dugaar"]
#         return None
#     def ustgah(self, ner: str):
#         for i, item in enumerate(self.jagsaalt):
#             if item["ner"].lower() == ner.lower():
#                 del self.jagsaalt[i]
#                 return True
#         return False
# if __name__ == "__main__":
#     mini_utas = Utas()

#     print("--- 1. Дугаар нэмэх ---")
#     mini_utas.nemeh("Bold", "99111122")
#     mini_utas.nemeh("Saraa", "85554433")
    
#     shalgah_ner = "Saraa"
#     oldson_dugaar = mini_utas.haih(shalgah_ner)
#     if oldson_dugaar:
#         print(f"{shalgah_ner}-iin dugaar: {oldson_dugaar}")
#     else:
#         print(f"{shalgah_ner} oldsongui.")

#     print(f"dorjiig haih ur dun: {mini_utas.haih('Dorj')}")

# 10
# class tsag:
#     def __init__(self, tsag, minut):
#         self.tsag = tsag
#         self.minut = minut
        
#     def minut_nemeh(self, m):
#         self.minut += m 
#         self.tsag += self.minut
#         self.minut %= 60
#         self.tsag %= 24

#     def __str__(self):
#         return f"{self.tsag:02d}:{self.minut:02d}"
# t= tsag(9, 5)
# print(t)

# t.minut_nemeh(70)
# print (t)
# t.minut_nemeh(840)
# print(t)

# 11
# class Ajiltan:
#     def __init__(self, ner, tsalin):
#         self.ner = ner
#         self.tsalin = tsalin
#     def tsalin_bodoh(self):
#         return self.tsalin
# class Meneger(Ajiltan):
#     def tsalin_bodoh(self):
#         return self.tsalin *1.2
# class Zahiral(Ajiltan):
#     def tsalin_bodoh(self):
#         return self.tsalin *1.5
# a = Ajiltan("Bat", 1000000)
# m = Meneger("bold", 1000000)
# z = Zahiral("zaraa", 1000000)
# print(a.tsalin_bodoh())
# print(m.tsalin_bodoh())
# print(z.tsalin_bodoh())

# 12
# class Dans:
#     def __init__(self, ehnii_uldegdel):
#         self.uldegdel = ehnii_uldegdel
#     def oruulah(self, dun):
#         self.uldegdel += dun
#         print(f"dansand {dun} orloo. odoonii uldegdel {self.uldegdel} bain")
#     def avah(self, dun):
#         if dun > self.uldegdel:
#             print(f"anhaaruulga: dansnii uldegdel hureltsehgui bain. uldegdel{self.uldegdel}")
#         else:
#             self.uldegdel -= dun
#             print(f"dansand {dun} avah. odoonii uldegdel {self.uldegdel} bain")
# if __name__ == "__main__":
#     minii_dans = Dans(5000)
#     minii_dans.oruulah(1000)
#     minii_dans.avah(2000)
#     minii_dans.avah(10000)

# class Dans:
#     def __init__(self, ehnii_uldegdel):
#         self.__uldegdel = ehnii_uldegdel

#     @property
#     def uldegdel(self):
#         return self.__uldegdel
    

#     def oruulah(self, dun):
#         if dun < 0:
#             raise ValueError("dun eyreg garah ystoi")
        
#         self.__uldegdel += dun
#         print(f"dansnd {dun} orloo. odoonii uldegdel {self.__uldegdel} bain")

#     def avah(self, dun):
#         if dun > self.__uldegdel:
#             print(f"anhaaruulga: dansnii uldegdel hureltsehgui bain. uldegdel{self.__uldegdel}")
#         else:
#             self.__uldegdel -= dun
#             print(f"dansand {dun} avah. odoonii uldegdel {self.__uldegdel} bain")
# if __name__ == "__main__":
#     minii_dans = Dans(5000)
#     minii_dans.oruulah(1000)
#     minii_dans.avah(2000)
#     minii_dans.avah(10000)

# 13
# class Duurs:
#         def talbai(self):
#             raise NotImplementedError("talbai() methodiig oveeride hii")
    
# class Toirog(Duurs):
#     def __init__(self, radius):
#         self.radius = radius

#     def talbai(self):
#         return self.radius **2 *3.14

# class Tegsh_ontsogt(Duurs):
#     def __init__(self, urt, urgun):
#         self.urt = urt
#         self.urgun = urgun

#     def talbai(self):
#         return self.urt * self.urgun 

# class Gurvaljin(Duurs):
#     def __init__(self, suuri, undur):
#         self.suuri = suuri
#         self.undur = undur
#     def talbai(self):
#         return self.suuri * self.undur / 2 
# d1 = Toirog(5)
# d2 = Tegsh_ontsogt(4, 6)
# d3 = Gurvaljin(8, 3)
# print(d1.talbai())  
# print(d2.talbai())  
# print(d3.talbai())

# 14
# class hereglegch:
#     def __init__(self, ner, email):
#         self.ner, self.email = ner, email
#     @classmethod
#     def cvs_ees(cls, mor):
#         ner, email = map(str, mor.split(","))
#         return cls(ner, email)
    
#     @staticmethod
#     def email_zov_uu(email):
#         return "@" in email
# d = hereglegch.cvs_ees("Болд,bold@must.edu.mn")
# print(f"hereglegchiin ner {d.ner}, hereglegchiin email {d.email}")
# print(hereglegch.email_zov_uu(d.email))

# 15
# class Butarhai:
#     def __init__(self, huvaari, huvaagch):
#         self.huvaari , self.huvaagch = huvaari, huvaagch
#     def __str__(self):
        
#         if self.huvaagch == 1:
#             return f"{self.huvaari}"
#         return f"{self.huvaari}/{self.huvaagch}"

#     def __add__(self, other):
#         shine_huvaari = (self.huvaari * other.huvaagch) + (other.huvaari * self.huvaagch)
#         shine_huvaagch = self.huvaagch * other.huvaagch
#         return Butarhai(shine_huvari, shine_huvaagch) if 'shine_huvari' in locals() else Butarhai(shine_huvaari, shine_huvaagch)

#     def __sub__(self, other):
#         shine_huvaari = (self.huvaari * other.huvaagch) - (other.huvaari * self.huvaagch)
#         shine_huvaagch = self.huvaagch * other.huvaagch
#         return Butarhai(shine_huvaari, shine_huvaagch)

#     def __mul__(self, other):
#         shine_huvaari = self.huvaari * other.huvaari
#         shine_huvaagch = self.huvaagch * other.huvaagch
#         return Butarhai(shine_huvaari, shine_huvaagch)

#     def __eq__(self, other):
        
#         return (self.huvaari, self.huvaagch) == (other.huvaari, other.huvaagch)


# b1 = Butarhai(1, 4)  
# b2 = Butarhai(2, 4)  

# print(f"b1 бутархай: {b1}")
# print(f"b2 бутархай: {b2}")


# print(f"Нэмэх: {b1} + {b2} = {b1 + b2}")

# print(f"Хасах: {b1} - {b2} = {b1 - b2}")

# print(f"Үржих: {b1} * {b2} = {b1 * b2}")

# b3 = Butarhai(2, 8)  
# print(f"Шалгах ({b1} == {b3}): {b1 == b3}")

# 16
# class Toglogch:
#     def __init__(self, ed_zuils):
#         self.ed_zuils = ed_zuils
#     def __len__(self):
#         return len(self.ed_zuils)
#     def __contains__(self, item_name):
#         return item_name in self.ed_zuils
#     def __getitem__(self, index):
#         return self.ed_zuils[index]
# hund_baigaa_zuils = Toglogch(["Sword", "gutal", "sheld", "samar"])
# print(len(hund_baigaa_zuils))
# print(hund_baigaa_zuils[1])
# baigaa_yu = "Sword" in hund_baigaa_zuils
# print(baigaa_yu)

# 17
# class Hun:
#     def __init__(self, ner):
#         self.ner = ner
# class Oyutan(Hun):
#     def __init__(self, ner, angi):
#         super().__init__(ner)
#         self.angi = angi
# class Master(Oyutan):
#     def __init__(self, ner, angi, sudalgaanii_sedev):
#         super().__init__(ner, angi)
#         self.sudalgaanii_sedev = sudalgaanii_sedev

# m = Master("Болд", "Мэдээллийн систем", "Гүнзгий суралцахуй")

# print(f"Нэр: {m.ner}")   
# print(f"Анги: {m.angi}")                
# print(f"Судалгаа: {m.sudalgaanii_sedev}")

# class Hun:
#     def __init__(self, ner):
#         self.ner = ner

#     def tanilts(self):
#         return f"Намайг {self.ner} гэдэг."

# class Oyutan(Hun):
#     def __init__(self, ner, angi):
#         super().__init__(ner)
#         self.angi = angi

#     def tanilts(self):
#         эцэг_танилцуулга = super().tanilts()
#         return f"{эцэг_танилцуулга} Би {self.angi} ангийн оюутан."

# class Master(Oyutan):
#     def __init__(self, ner, angi, sudalgaanii_sedev):
#         super().__init__(ner, angi)
#         self.sudalgaanii_sedev = sudalgaanii_sedev

#     def tanilts(self):
#         оюутан_танилцуулга = super().tanilts()
#         return f"{оюутан_танилцуулга} Миний судалгааны сэдэв: '{self.sudalgaanii_sedev}'."


# m = Master("Болд", "Мэдээллийн систем", "Гүнзгий суралцахуй")

# print(m.tanilts())

# 18
# class Oyutan:
#     def __init__(self, ner, onoo):
#         self.ner, self.onoo = ner, onoo
#     def __eq__(self, other):
#         return self.onoo == other.onoo
#     def __lt__(self, other):
#         return self.onoo < other.onoo
# jagsaalt = [
#     Oyutan("Baldan", 93),
#     Oyutan("Dolgor", 91),
#     Oyutan("Dash", 98)
# ]
# sorted_jagsaalt = sorted(jagsaalt)
# for ner in sorted_jagsaalt:
#     print(f"{ner.ner}, {ner.onoo}")

# 19
# class Product:
#     def __init__(self, name, price):
#         self.name = name
#         self.price = price

# class Sags:
#     def __init__(self):
#         self.buh_baraa = {}

#     def nemeh(self, baraa, too):
#         if not isinstance(baraa, Product):
#             print("zuvhun product  classiin baraa nemeh bolomjtoi")
#             return
            
#         if baraa in self.buh_baraa:
#             self.buh_baraa[baraa] += too
#         else:
#             self.buh_baraa[baraa] = too
#         print(f"sagsand {too} shirheg '{baraa.name}' nemegdlee.")

#     def hasah(self, baraa):
#         if baraa in self.buh_baraa:
#             del self.buh_baraa[baraa]
#             print(f" sagsand '{baraa.name}'iig haslaa")
#         else:
#             print(f"sagsand '{baraa.name}' baraa alga")

#     def niit_dun(self):
#         dun = 0
#         for baraa, too in self.buh_baraa.items():
#             dun += baraa.price * too  
#         return dun

#     def __iter__(self):
#         for baraa in self.buh_baraa.keys():
#             yield baraa

# laptop = Product("Laptop", 1200)
# mouse = Product("Mouse", 25)
# monitor = Product("Monitor", 300)

# mini_sags = Sags()

# mini_sags.nemeh(laptop, 1)  
# mini_sags.nemeh(mouse, 2)   
# mini_sags.nemeh(monitor, 1) 

# print("-" * 40)

# print("sagsandahi baraanuud:")
# for b in mini_sags:
#     shirheg = mini_sags.buh_baraa[b]
#     print(f"- {b.name}: ${b.price} x {shirheg}ш")
# print("-" * 40)
# print(f"niit dun: ${mini_sags.niit_dun()}")
# print("-" * 40)
# mini_sags.hasah(mouse)
# print(f"hassanii daraah niit dun: ${mini_sags.niit_dun()}")

# 20
# import json
# class JsonMixin:
#     def to_json(self):
#         return json.dumps(self.__dict__, ensure_ascii = False)
    
# class LogMixin:
#     def log(self, uildel_ner):
#         print(f"LOG:[{self.__class__.__name__}] -> '{uildel_ner} method duudagdlaa")

# class Hereglegch(LogMixin, JsonMixin):
#     def __init__(self, ner, email):
#         self.ner, self.email = ner, email
#         self.log("__init__ (herelegch uuslee)")

#     def medeelel_shinchleh(self, shine_email):
#         self.email = shine_email
#         self.log("medeelel_shinchleh")
# print("1. obect uusgeh uye")
# h = Hereglegch("Oyun", "o@must.edu.mn")
# print("\n 2. method duudah uye")
# h.medeelel_shinchleh("oyun.shine@must.edu.mn")
# print("\n 3. Json formatruu hurvuuleh")
# json_zurvas = h.to_json()
# print(json_zurvas)

#21
# class Matrix:
#     def __init__(self, data):
#         self.data = data
#         self.rows = len(data)
#         self.cols = len(data[0]) if self.rows > 0 else 0
#     def __getitem__(self, index):
#         return self.data[index]
#     def __add__(self, other):
#         if self.rows != other.rows or self.cols != other.cols:
#             raise ValueError(f"hemjees tohirohgui bain: {self.rows}x{self.cols} matritsiig {other.rows}x{other.cols} matritstai nemeh bolomjgui")
#         result = [
#             [self[i][j] + other[i][j] for j in range(self.cols)]
#             for i in range(self.rows)
#         ]
#         return Matrix(result)
#     def __matmul__(self, other):
#         if self.cols != other.rows:
#             raise ValueError(f"martitsiig urjver hemjees tohirohgui bain:{self.rows}x{self.cols} matritsiig {other.rows}x{other.cols} matritstai urjuuleh bolomjgui")
        
#         result = []
#         for i in range(self.rows):
#             row_result = []
#             for j in range(other.cols):
#                 element_sum = sum(self[i][k] * other[k][j] for k in range(self.cols))
#                 row_result.append(element_sum)
#             result.append(row_result)
            
#         return Matrix(result)
    
#     def __eq__(self, other):
#         if not isinstance(other, Matrix):
#             return False
#         if self.rows != other.rows or self.cols != other.cols:
#             return False
#         return self.data == other.data
#     def __repr__(self):
#         return "\n".join([str(row) for row in self.data])

# m1 = Matrix([[1, 2], [3,4]])
# m2 = Matrix([[5, 6], [7, 8]])
# print(m1)
# print(m1 + m2)
# print(m1 @ m2)
# m3 = Matrix([[1, 2, 3]])
# try:
#     print(m1+m3)
# except ValueError as e:
#     print(f"aldaa: {e}")

#22
# class Ajiltan:
#     def __init__(self, ner, nas, alban_tushaal):
#         self.ner = ner
#         self.nas = nas
#         self.alban_tushaal = alban_tushaal
#     @property
#     def ner(self):
#         return self._ner
#     @ner.setter
#     def ner(self, value):
#         if not (2 <= len(value) <= 20):
#             raise ValueError("ner zaaval 2-oos 20 usegtei bain")
#         self._ner = value
#     @property
#     def nas(self):
#         return self._nas
#     @nas.setter
#     def nas(self, value):
#         if value <= 0:
#             raise ValueError("nas zaaval too baih ystoi")
#         self._nas = value
#     @property
#     def alban_tushaal(self):
#         return self._alban_tushaal
#     @alban_tushaal.setter
#     def alban_tushaal(self, value):
#         zuv_songoltuud = ["zahiral", "manager", "hugjuulegch"]
#         if value not in zuv_songoltuud:
#             raise ValueError(f"buruu alban tushaal! songoltuud: {zuv_songoltuud}")
#         self._alban_tushaal = value
# try:
#     a1 = Ajiltan("bold", 25, "hugjuulegch")
#     print(f"ajiltan uuslee: {a1.ner}, {a1.nas} nastai, {a1.alban_tushaal}")
# except ValueError as e:
#     print(f"aldaa garlaa: {e}")   

#23
# import datetime

# class SingletonMeta(type):
#     _instances = {}

#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super().__call__(*args, **kwargs)
        
#         return cls._instances[cls]


# class Logger(metaclass=SingletonMeta):
#     def __init__(self, file_name="log.txt"):
#         self.file_name = file_name
#         print(f" [Logger] shine system ajillaj ehellee. ner: {self.file_name}")

#     def butchih(self, msg):
#         odoogiin_tsag = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
#         with open(self.file_name, "a", encoding="utf-8") as f:
#             f.write(f"[{odoogiin_tsag}] {msg}\n")
#         print(f"log bichigdlee: {msg}")


# log1 = Logger()
# log2 = Logger()


# ijil_eseh = (log1 is log2)
# print(f"log1 log2 ijilhen uu?: {ijil_eseh}")

# if ijil_eseh:
#     print(" Test Amjilttai ajilj bain")
# else:
#     print(" Test aldaa garav")

# print("\nmedeelel turshih")
# log1.butchih("system amjilttai ajillaa")
# log2.butchih("hereglegch nevterlee")

#24
# class Model:
#     @classmethod
#     def create_table_sql(cls):
#         table_name = cls.__name__.lower()
        
#         sql_fields = []
        
#         for field_name, field_type in cls.fields.items():
#             if field_type == "int":
#                 sql_fields.append(f"{field_name} INTEGER")
#             elif field_type.startswith("str:"):
#                 max_length = field_type.split(":")[1]
#                 sql_fields.append(f"{field_name} VARCHAR({max_length})")
        
#         fields_str = ", ".join(sql_fields)
        
#         return f"CREATE TABLE {table_name} ({fields_str});"

# class Oyutan(Model):
#     fields = {
#         "ner": "str:50",  
#         "nas": "int"     
#     }

# sql_query = Oyutan.create_table_sql()
# print("--- Үүссэн SQL Хүснэгт ---")
# print(sql_query)

#25
# import sys
# import tracemalloc

# class TsegЖирийн:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

# class TsegSlots:
#     __slots__ = ['x', 'y']
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

# def memory_test():
#     OBEKT_TOO = 1_000_000

#     print("=== САНАХ ОЙН ШИЛЖИЛТИЙГ ХЭМЖИХ СИСТЕМ АЖИЛЛАЖ ЭХЭЛЛЭЭ ===\n")

#     tracemalloc.start() 
#     tsguud_jiriin = [TsegЖирийн(i, i+1) for i in range(OBEKT_TOO)]
    
#     current, peak = tracemalloc.get_traced_memory()
#     jiriin_total_mb = current / (1024 * 1024)  
#     jiriin_one_obj_bytes = sys.getsizeof(tsguud_jiriin[0]) + sys.getsizeof(tsguud_jiriin[0].__dict__)
    
#     tracemalloc.stop()  
#     del tsguud_jiriin   

#     tracemalloc.start()
    
#     tsguud_slots = [TsegSlots(i, i+1) for i in range(OBEKT_TOO)]
    
#     current, peak = tracemalloc.get_traced_memory()
#     slots_total_mb = current / (1024 * 1024)
#     slots_one_obj_bytes = sys.getsizeof(tsguud_slots[0])
    
#     tracemalloc.stop()
#     del tsguud_slots


#     print(f" Ганц объектын хэмжээ (sys.getsizeof):")
#     print(f"   - Жирийн объект (+ __dict__): {jiriin_one_obj_bytes} байт")
#     print(f"   - Slots-той объект:           {slots_one_obj_bytes} байт")
#     print("-" * 50)
#     print(f" 1,000,000 объект үүсгэхэд зарцуулсан нийт санах ой:")
#     print(f"   - Жирийн хувилбар: {jiriin_total_mb:.2f} MB")
#     print(f"   - Slots-той хувилбар: {slots_total_mb:.2f} MB")
#     print("-" * 50)
    
#     hemnej_chadsan_mb = jiriin_total_mb - slots_total_mb
#     huvi = (hemnej_chadsan_mb / jiriin_total_mb) * 100
#     print(f" ХЭМНЭЛТ: Бүрэн хэмнэж чадсан санах ой: {hemnej_chadsan_mb:.2f} MB")
#     print(f" ҮР ДҮН: Санах ойг {huvi:.1f}%-иар ухаалаг хэмнэж чадлаа!")

# if __name__ == "__main__":
#     memory_test()

#26
# import os

# class TurZuuriinFail:
#     def __init__(self, fail_ner):
#         self.fail_ner = fail_ner

#     def __enter__(self):
#         with open(self.fail_ner, "w", encoding="utf-8") as f:
#             f.write("Түр зуурын өгөгдөл...")
#         print(f" [Класс] '{self.fail_ner}' файл амжилттай үүслээ.")
#         return self.fail_ner  
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if os.path.exists(self.fail_ner):
#             os.remove(self.fail_ner)
#             print(f" [Класс] '{self.fail_ner}' файлыг автоматаар устгалаа.")
#         return False
# def test_ajiluulah():
#     fail_1 = "test_class.txt"
#     print("=== ТЕСТ: Класс ашиглан алдаа гаргаж турших ===")
#     try:
#         with TurZuuriinFail(fail_1) as f_ner:
#             print("-> Блок доторх код ажиллаж байна. Одоо зориуд алдаа гаргана...")
            
#     except ZeroDivisionError:
#         print(" Алдааг барьж авлаа. Одоо файл устсан эсэхийг шалгая.")
#         print(f"Файл байна уу?: {os.path.exists(fail_1)}")
# if __name__ == "__main__":
#     test_ajiluulah()

# from contextlib import contextmanager
# import os

# @contextmanager
# def tur_zuuriin_fail_manager(fail_ner):
#     with open(fail_ner, "w", encoding="utf-8") as f:
#         f.write("Түр зуурын өгөгдөл...")
#     print(f" [Декоратор] '{fail_ner}' файл амжилттай үүслээ.")
    
#     try:
#         yield fail_ner  
#     finally:
#         if os.path.exists(fail_ner):
#             os.remove(fail_ner)
#             print(f" [Декоратор] '{fail_ner}' файлыг автоматаар устгалаа.")

#27
# import itertools

# class Fibonacciinterrator:
#     def __init__(self):
#         self.a = 0
#         self.b = 1

#     def __iter__(self):
#         return self

#     def __next__(self):
#         угтах_утга = self.a
#         self.a, self.b = self.b, self.a + self.b
#         return угтах_утга


# class Fibonaccigenerator:
#     def __iter__(self):
#         a, b = 0, 1
#         while True:
#             yield a
#             a, b = b, a + b


# if __name__ == "__main__":
    
#     print("--- (а) Классик interratorоор эхний 10-ыг авах ---")
#     fib1 = Fibonacciinterrator()
#     ehni_10_ital = list(itertools.islice(fib1, 10))
#     print(ehni_10_ital)

#     print("\n--- (б) generator ашиглан эхний 10-ыг авах ---")
#     fib2 = Fibonaccigenerator()
#     ehni_10_gen = list(itertools.islice(fib2, 10))
#     print(ehni_10_gen)

#28

# class Delgets:
#     def medegdel(self, utga):
#         print(f" [Дэлгэц] Мэдрэгчийн шинэ утгыг харуулж байна: {utga}°C")

# class Doohiolol:
#     def medegdel(self, utga):
#         if utga > 40:
#             print(f" [Дохиолол] АНХААР! Хэт халлаа! Одоогийн утга: {utga}°C")
#         else:
#             print(f" [Дохиолол] Систем хэвийн байна. ({utga}°C)")


# class Sensor:
#     def __init__(self):
#         self._observers = []  
#         self._utga = None     

#     def nemeh(self, observer):
#         if observer not in self._observers:
#             self._observers.append(observer)
#             print(f" Шинэ ажиглагч амжилттай бүртгэгдлээ.")

#     def hasah(self, observer):
#         if observer in self._observers:
#             self._observers.remove(observer)
#             print(f" Нэг ажиглагчийг хаслаа.")

#     def _buhнд_мэдэгдэх(self):
#         for observer in self._observers:
#             observer.medegdel(self._utga)

#     @property
#     def utga(self):
#         return self._utga

#     @utga.setter
#     def utga(self, shine_utga):
#         self._utga = shine_utga
#         print(f"\n [Мэдрэгч] Утга өөрчлөгдлөө -> {shine_utga}")
#         self._buhнд_мэдэгдэх()

# if __name__ == "__main__":
    
#     termo_sensor = Sensor()
#     delgets = Delgets()
#     doohiolol = Doohiolol()

#     print("--- 1. Ажиглагчдыг мэдрэгчид холбох ---")
#     termo_sensor.nemeh(delgets)
#     termo_sensor.nemeh(doohiolol)

#     print("\n--- 2. Мэдрэгчийн утга 25 болоход (Хэвийн үе) ---")
#     termo_sensor.utga = 25

#     print("\n--- 3. Мэдрэгчийн утга 50 болоход (Дохиолол ажиллах үе) ---")
#     termo_sensor.utga = 50

#     print("\n--- 4. Дохиоллыг хасаад, утгыг дахин өөрчлөх ---")
#     termo_sensor.hasah(doohiolol)  
#     termo_sensor.utga = 30

#29
# from dataclasses import dataclass, field
# import math

# @dataclass(frozen=True)
# class Vector:
#     coords: tuple[float, ...] = field(default_factory=tuple)

#     def __init__(self, *coords):
#         object.__setattr__(self, 'coords', coords)

#     def __add__(self, other):
#         if not isinstance(other, Vector):
#             raise TypeError("Векторыг зөвхөн өөр Вектортой нэмж болно.")
#         if len(self.coords) != len(other.coords) :
#             raise ValueError("Векторуудын хэмжээс (координатын тоо) ижил байх ёстой.")
        
#         shine_coords = tuple(x + y for x, y in zip(self.coords, other.coords))
#         return Vector(*shine_coords)

#     def __mul__(self, scalar):
#         if not isinstance(scalar, (int, float)):
#             raise TypeError("Векторыг зөвхөн тоогоор (скаляр) үржүүлж болно.")
        
#         shine_coords = tuple(x * scalar for x in self.coords)
#         return Vector(*shine_coords)

#     def __abs__(self):
#         return math.sqrt(sum(x**2 for x in self.coords))

#     def __repr__(self):
#         return f"Vector{self.coords}"

# if __name__ == "__main__":
    
#     v1 = Vector(3.0, 4.0)
#     v2 = Vector(1.0, 2.0)
#     v3 = Vector(1.0, 2.0, 3.0)  
#     print("--- 1. Үндсэн үйлдлүүд шалгах ---")
#     print(f"v1-ийн координатууд: {v1}")
#     print(f"Нэмэх үйлдэл (v1 + v2): {v1 + v2}")
#     print(f"Үржүүлэх үйлдэл (v1 * 3): {v1 * 3}")
#     print(f"Векторын урт (|v1|): {abs(v1)}")  

#     print("\n--- 2. Өөрчлөгдөшгүй (Frozen) чанарыг шалгах ---")
#     try:
#         v1.coords = (10, 20)  
#     except Exception as e:
#         print(f"Хамгаалалт ажиллалаа (Утга өөрчлөх боломжгүй): {type(e).__name__}")

#     print("\n--- 3. Set болон Dict-ийн түлхүүр болгож ашиглах ---")
#     vektor_set = {v1, v2, v1}  
#     print(f"Set-ийн хэмжээ (Давхцлыг хассан): {len(vektor_set)}")

#     vektor_dict = {
#         v1: "А цэг рүү чиглэсэн вектор",
#         v3: "Гурван хэмжээст орон зайн вектор"
#     }
#     print(f"Dict-ээс v1 түлхүүрээр дуудахад: '{vektor_dict[v1]}'")
