
ONES = {0: "", 1: "нэг", 2: "хоёр", 3: "гурав", 4: "дөрөв", 5: "тав", 6: "зургаа", 7: "долоо", 8: "найм", 9: "ес"}
TENS = {0: "", 1: "арав", 2: "хорин", 3: "гучин", 4: "дөчин", 5: "тавин", 6: "жаран", 7: "далсан", 8: "наян", 9: "ерөн"}

MONTHS = {
    1: "нэгдүгээр", 2: "хоёрдугаар", 3: "гуравдугаар", 4: "дөрөвдүгээр",
    5: "тавдугаар", 6: "зургадугаар", 7: "долоодугаар", 8: "наймдугаар",
    9: "есдүгээр", 10: "аравдугаар", 11: "арван нэгдүгээр", 12: "арван хоёрдугаар"
}

DAYS_SUFFIX = {
    1: "нэгний", 2: "хоёрны", 3: "гуравны", 4: "дөрөвний", 5: "тавны",
    6: "зургааны", 7: "долооны", 8: "наймны", 9: "есний", 10: "арвны",
    20: "хорины", 30: "гучны"
}

def number_to_mongolian(num):
    if num == 0:
        return "тэг"
    
    words = []
    
    billions = num // 1000000000
    num %= 1000000000
    
    millions = num // 1000000
    num %= 1000000
    
    thousands = num // 1000
    num %= 1000
    
    hundreds = num // 100
    num %= 100
    
    tens = num // 10
    ones = num % 10
    
    if billions > 0:
        words.append(f"{number_to_mongolian(billions)} тэрбум")
    if millions > 0:
        words.append(f"{number_to_mongolian(millions)} сая")
    if thousands > 0:
        words.append(f"{number_to_mongolian(thousands)} мянга")
    if hundreds > 0:
        words.append(f"{ONES[hundreds]} зуун")
        
    if tens > 0:
        words.append(TENS[tens])
    if ones > 0:
        words.append(ONES[ones])
        
    return " ".join([w for w in words if w]).strip()

def convert_date_to_mongolian(date_str):
    date_str = date_str.replace(".", "-").replace("/", "-").replace(" ", "-")
    parts = date_str.split("-")
    
    if len(parts) == 3:
        try:
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
            
            year_word = number_to_mongolian(year)
            year_word = year_word.replace("гурав ", "гурван ")
            year_word = year_word.replace("дөрөв ", "дөрвөн ")
            year_word = year_word.replace("тав ", "таван ")
            year_word = year_word.replace("зургаа ", "зургаан ")

            if year_word.endswith("зургаа"): year_word = year_word[:-1] + "ан"
            elif year_word.endswith("дөрөв"): year_word = year_word[:-2] + "вөн"
            elif year_word.endswith("гурав"): year_word = year_word[:-2] + "ван"
            elif year_word.endswith("хоёр"): year_word = year_word[:-1] + "рон"
            elif year_word.endswith("нэг"): year_word = year_word + "ийн"
            elif year_word.endswith("арав"): year_word = year_word[:-2] + "вны"
            elif year_word.endswith("тав"): year_word = year_word + "н"
            else: year_word += " оны"
            
            if not year_word.endswith("оны"):
                year_word += " оны"
                
            month_word = MONTHS.get(month, f"{month} дугаар") + " сарын"
            
            if day in DAYS_SUFFIX:
                day_word = DAYS_SUFFIX[day]
            else:
                d_tens = (day // 10) * 10
                d_ones = day % 10
                day_word = f"{TENS[day // 10]} {DAYS_SUFFIX[d_ones]}" if d_tens > 0 else DAYS_SUFFIX[d_ones]
            
            day_word += " өдөр"
            
            return f"{year_word} {month_word} {day_word}"
        except ValueError:
            return None
    return None

def main():
    print("Хөрвүүлэх утгаа оруулна уу:")
    user_input = input().strip()
    
    if not user_input:
        return

    # 1. ТЭМДЭГТҮҮДИЙГ ЦЭВЭРЛЭЖ, ТАНИХ БЭЛТГЭЛ ХИЙХ
    clean_input = user_input.replace("+", "").strip() # Урд талын + тэмдгийг хасах
    is_negative = clean_input.startswith("-")
    if is_negative:
        clean_input = clean_input[1:].strip() # Хасах тэмдгийг түр салгах

    # 2. ХУВЬ ШАЛГАХ (Жишээ нь: 100%, 99.9%)
    if clean_input.endswith("%"):
        val_str = clean_input[:-1].strip()
        try:
            val_float = float(val_str)
            val_int = int(val_float)
            # Хэрэв бутархай хэсэг нь 0 бол бүхэл тоогоор уншина
            num_word = number_to_mongolian(val_int) if val_float == val_int else f"{number_to_mongolian(val_int)} зууны {number_to_mongolian(int(round((val_float-val_int)*10)))}"
            prefix = "хасах " if is_negative else ""
            print(f"{prefix}{num_word} хувь")
            return
        except ValueError:
            pass

    # 3. МӨНГӨН ДҮН ШАЛГАХ (Жишээ нь: ₮123456789)
    if clean_input.startswith("₮"):
        val_str = clean_input[1:].strip()
        try:
            val = int(float(val_str)) # Бутархай байвал бүхэл болгоно
            money_word = number_to_mongolian(val)
            
            #  Төгсгөл нь "ес", "найм", "долоо", "зургаа" зэргээр төгсвөл "н" залгах дүрэм:
            if money_word.endswith("нэг"): money_word += "ний"  # нэгний төгрөг биш, нэг төгрөг гэх тул үүнийг алгасэж болно. Шаардлагатай бол:
            elif money_word.endswith("хоёр"): money_word += "н"
            elif money_word.endswith("гурав"): money_word = money_word[:-2] + "ван"
            elif money_word.endswith("дөрөв"): money_word = money_word[:-2] + "вөн"
            elif money_word.endswith("тав"): money_word += "н"
            elif money_word.endswith("зургаа"): money_word = money_word[:-1] + "ан"
            elif money_word.endswith("долоо"): money_word += "н"
            elif money_word.endswith("найм"): money_word += "ан"
            elif money_word.endswith("ес"): money_word += "өн"
            elif money_word.endswith("арав"): money_word = money_word[:-2] + "вны"
            # Хэрэв "хорь", "гуч" гэх мэт аравтууд байвал угаасаа зөв уншигдана (хорин төгрөг, гучин төгрөг)

            prefix = "хасах " if is_negative else ""
            print(f"{prefix}{money_word} төгрөг")
            return
        except ValueError:
            pass
    # 4. ЦАГ ХУГАЦАА ШАЛГАХ (Жишээ нь: 12:34, 00:00)
    if ":" in clean_input and clean_input.count(":") == 1:
        time_parts = clean_input.split(":")
        try:
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                hour_word = "нойл" if hour == 0 else number_to_mongolian(hour)
                min_word = "нойл" if minute == 0 else number_to_mongolian(minute)
                print(f"{hour_word} цаг {min_word} минут")
                return
        except ValueError:
            pass

    # 5. ОН-САР-ӨДӨР ШАЛГАХ (Жишээ нь: 2026-06-02, 2026 06 02)
    if ("-" in clean_input or "." in clean_input or "/" in clean_input or " " in clean_input) and len(clean_input) >= 8:
        # Утасны дугаар биш эсэхийг давхар шалгана (Зөвхөн хоосон зайтай 8 оронтой тоо байх тохиолдлоос хамгаалах)
        if not (clean_input.replace(" ", "").isdigit() and len(clean_input.replace(" ", "")) in [8, 10]):
            date_result = convert_date_to_mongolian(clean_input)
            if date_result:
                prefix = "хасах " if is_negative else ""
                print(f"{prefix}{date_result}")
                return

    # 6. УТАСНЫ ДУГААР ШАЛГАХ (Жишээ нь: 99112233 эсвэл 9911223344)
    phone_digits = clean_input.replace(" ", "")
    if phone_digits.isdigit() and (len(phone_digits) == 8 or len(phone_digits) == 10):
        pairs = [phone_digits[i:i+2] for i in range(0, len(phone_digits), 2)]
        phone_words = []
        
        for pair in pairs:
            val = int(pair)
            if val == 0:
                word = "нойл нойл"
            elif val < 10 and pair[0] == '0':
                word = f"нойл {number_to_mongolian(val)}"
            else:
                # Үндсэн хөрвүүлэлтийг хийнэ
                word = number_to_mongolian(val)
                
                # 👇 ХЭРЭВ ХОЁР ОРОНТОЙ ТОО НЬ БҮТЭН АРАВТ БАЙВАЛ (20, 30, 40, 50, 70, 80, 90)
                # Зөвхөн энэ үед л ярианы хэлбэрээр богиносгож уншина.
                if pair in ["20", "30", "40", "50", "60", "70", "80", "90"]:
                    if pair == "20": word = "хори"
                    elif pair == "30": word = "гучи"
                    elif pair == "40": word = "дөчи"
                    elif pair == "50": word = "тави"
                    elif pair == "60": word = "жара"
                    elif pair == "70": word = "дала"
                    elif pair == "80": word = "ная"
                    elif pair == "90": word = "ер"
            
            phone_words.append(word)
        
        # Нийлүүлээд суурь зөв бичих дүрмийн алдааг засна
        result_phone = " ".join(phone_words)
        result_phone = result_phone.replace("далсан", "далан")
        result_phone = result_phone.replace("ерөн", "ерэн")
        result_phone = result_phone.replace("наясан", "наян")
        result_phone = result_phone.replace("арав тав", "арван тав")
        result_phone = result_phone.replace("арва тав", "арван тав")
        print(result_phone)
        return
    # 7. ЕРӨНХИЙ БҮХЭЛ БОЛОН БУТАРХАЙ ТОО ШАЛГАХ
    try:
        # Хэрэв цэвэр тоо бол (Жишээ нь: 001, 12345, -100, 0.001)
        # Урд талын илүүдэл нойлуудыг цэвэрлэхийн тулд float болгоно
        val_float = float(clean_input)
        
        # Хэрэв бутархай тоо байвал (Жишээ нь: 0.1, 123456.789)
        if "." in clean_input and not clean_input.endswith(".0") and val_float != int(val_float):
            parts = clean_input.split(".")
            whole_part = int(parts[0])
            frac_part_str = parts[1]
            
            # Бутархай орны нэрийг олох (аравны, зууны, мянганы...)
            frac_len = len(frac_part_str)
            arr = ["", "аравны", "зууны", "мянганы", "арван мянганы", "зуун мянганы", "саяны"]
            frac_name = arr[frac_len] if frac_len < len(arr) else f"10^{frac_len}-ны"
            
            frac_val = int(frac_part_str)
            
            whole_word = "нойл" if whole_part == 0 else number_to_mongolian(whole_part)
            frac_word = "нойл" if frac_val == 0 else number_to_mongolian(frac_val)
            
            prefix = "хасах " if is_negative else ""
            print(f"{prefix}{whole_word} бүхэл {frac_name} {frac_word}")
            return
        else:
            # Зүгээр л бүхэл тоо бол
            val_int = int(val_float)
            word = "нойл" if val_int == 0 else number_to_mongolian(val_int)
            prefix = "хасах " if is_negative else ""
            print(f"{prefix}{word}")
            return
            
    except ValueError:
        pass

    # 8. ДЭЭРХИЙН АЛЬ НЬ Ч БИШ БОЛ
    print("Уучлаарай, форматыг таньсангүй. Та зөв утга оруулна уу.")
if __name__ == "__main__":
    main()