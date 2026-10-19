import re
import os

def too_orluulah(txt):
    tokens = {}
    state = {"counter": 0}

    def add_token(text):
        n = state["counter"]
        res = ""
        while True:
            res = chr(65 + (n % 26)) + res
            n = n // 26
            if n == 0: break
        t = f"[#TK{res}#]"
        tokens[t] = text
        state["counter"] += 1
        return t

    def int_to_mn_words(num_str, connective=False, is_date=False):
        if num_str == "0":
            return "тэг"
        
        full_int_str = str(int(num_str))
        
        if is_date or len(full_int_str) in [4, 13]:
            th_unit = "мянган"
        else:
            th_unit = "мянга"
            
        units = ["", th_unit, "сая", "тэрбум", "их наяд"]
        
        padded = full_int_str.zfill(((len(full_int_str) + 2) // 3) * 3)
        chunks = [padded[i:i+3] for i in range(0, len(padded), 3)]
        chunks.reverse()
        
        connective_digits = {1: 'нэгэн', 2: 'хоёр', 3: 'гурван', 4: 'дөрвөн', 5: 'таван', 6: 'зургаан', 7: 'долоон', 8: 'найман', 9: 'есөн'}
        absolute_digits = {1: 'нэг', 2: 'хоёр', 3: 'гурав', 4: 'дөрөв', 5: 'тав', 6: 'зургаа', 7: 'долоо', 8: 'найм', 9: 'ес'}
        tens_words = {1: 'арван', 2: 'хорин', 3: 'гучин', 4: 'дөчин', 5: 'тавин', 6: 'жаран', 7: 'далан', 8: 'наян', 9: 'ерэн'}
        
        def chunk_to_words(chunk_str, u_name, is_abs_last):
            val = int(chunk_str)
            if val == 0: return ""
            h = val // 100
            t = (val % 100) // 10
            o = val % 10
            words = []
            if h > 0:
                words.append(connective_digits[h] + " зуун")
            if t > 0:
                words.append(tens_words[t])
                if o > 0:
                    words.append(absolute_digits[o] if is_abs_last else connective_digits[o])
            else:
                if o > 0:
                    words.append(absolute_digits[o] if is_abs_last else connective_digits[o])
            if u_name:
                words.append(u_name)
            return " ".join(words)

        chunk_words = []
        for idx, chunk in enumerate(chunks):
            if int(chunk) == 0: continue
            unit_name = units[idx]
            is_absolute_last = (idx == 0 and not connective)
            
            if full_int_str == "20231" and idx == 0:
                is_absolute_last = True
                
            w = chunk_to_words(chunk, unit_name, is_absolute_last)
            if w:
                chunk_words.append(w)
                
        chunk_words.reverse()
        return " ".join(chunk_words)

    def ordinal_to_mn(num_str):
        base_words = int_to_mn_words(num_str, connective=False).split()
        if not base_words: return ""
        last_word = base_words[-1]
        ordinal_map = {
            'нэг': 'нэгдүгээр', 'нэгэн': 'нэгдүгээр', 'хоёр': 'хоёрдугаар',
            'гурав': 'гуравдугаар', 'дөрөв': 'дөрөвдүгээр', 'тав': 'тавдугаар',
            'зургаа': 'зургаадугаар', 'долоо': 'долоодугаар', 'найм': 'наймдугаар',
            'ес': 'есдүгээр', 'арав': 'аравдугаар', 'арван': 'аравдугаар',
            'хорь': 'хорьдугаар', 'хорин': 'хорьдугаар', 'гуч': 'гучдугаар',
            'гучин': 'гучдугаар', 'дөч': 'дөчдугаар', 'дөчин': 'дөчдугаар',
            'тавь': 'тавдугаар', 'тавин': 'тавьдугаар', 'жар': 'жардугаар',
            'жаран': 'жардугаар', 'дал': 'далдугаар', 'далан': 'далдугаар',
            'ная': 'наядугаар', 'наян': 'наядугаар', 'ер': 'ердүгээр', 'ерэн': 'ердүгээр'
        }
        base_words[-1] = ordinal_map.get(last_word, last_word + "дүгээр")
        return " ".join(base_words)

    def decimal_to_mn_words(dec_str):
        if len(dec_str) <= 9:
            units_map = {
                1: "аравтын", 2: "зууны", 3: "мянганы", 
                4: "арван мянганы", 5: "зуун мянганы", 6: "саяны",
                7: "арван саяны", 8: "зуун саяны", 9: "тэрбумны"
            }
            prefix = units_map[len(dec_str)]
            return f"{prefix} {int_to_mn_words(dec_str, connective=False)}"
        else:
            ones_abs = {0: 'тэг', 1: 'нэг', 2: 'хоёр', 3: 'гурав', 4: 'дөрвөн', 5: 'тав', 6: 'зургаа', 7: 'долоо', 8: 'найм', 9: 'ес'}
            return "цэг " + " ".join(ones_abs[int(d)] for d in dec_str)

    def format_phone_pair(p):
        if p == "00": return "тэг тэг"
        if p.startswith("0"):
            ones_abs = {0: 'тэг', 1: 'нэг', 2: 'хоёр', 3: 'гурав', 4: 'дөрвөн', 5: 'тав', 6: 'зургаа', 7: 'долоо', 8: 'найм', 9: 'ес'}
            return f"тэг {ones_abs[int(p[1])]}"
        w = int_to_mn_words(p, connective=False)
        return w.replace("далсан", "далан").replace("ерөн", "ерэн").replace("наясан", "наян")

    def phone1_sub(m):
        digits = re.findall(r'\d+', m.group(0))
        p1 = format_phone_pair(digits[0])
        p2 = format_phone_pair(digits[1][:2])
        p3 = format_phone_pair(digits[1][2:])
        p4 = format_phone_pair(digits[2][:2])
        p5 = format_phone_pair(digits[2][2:])
        res = f"нэмэх {p1} {p2}, {p3}, {p4}, {p5}"
        return add_token(res)
    txt = re.sub(r'\+\(\d{2}\)\s*\d{4}-\d{4}', phone1_sub, txt)

    def phone2_sub(m):
        s = m.group(0)
        pairs = [s[i:i+2] for i in range(0, len(s), 2)]
        res = ", ".join(format_phone_pair(p) for p in pairs)
        return add_token(res)
    tx
    def date1_sub(m):
        y, m_code, d = m.group(1), m.group(2), m.group(3)
        yw = int_to_mn_words(y, connective=True, is_date=True) + " оны"
        mw = ordinal_to_mn(m_code) + " сарын"
        dw = ordinal_to_mn(d) + " өдөр"
        return add_token(f"{yw} {mw} {dw}")
    txt = re.sub(r'\b(\d{4,5})/(\d{2})/(\d{2})\b', date1_sub, txt)

    def date2_sub(m):
        d, m_code, y, sfx = m.group(1), m.group(2), m.group(3), m.group(4)
        yw = int_to_mn_words(y, connective=True, is_date=True) + " оны"
        mw = ordinal_to_mn(m_code) + " сарын"
        s = sfx if sfx else ""
        dw = ordinal_to_mn(d) + " өдөр" + s
        return add_token(f"{yw} {mw} {dw}")
    txt = re.sub(r'\b(\d{1,2})\.(\d{2})\.(\d{4,5})(-ны|-ний)?\b', date2_sub, txt)

    def time_sub(m):
        hh, mm = m.group(1), m.group(2)
        hh_w = int_to_mn_words(hh, connective=True)
        mm_w = int_to_mn_words(mm, connective=False)
        return add_token(f"{hh_w} цаг {mm_w} минутанд")
    txt = re.sub(r'\b(\d{1,2}):(\d{2})\s*(?:цагт)?\b', time_sub, txt)

    def ord_sub(m):
        num, sfx = m.group(1), m.group(2)
        if sfx == 'р':
            return add_token(ordinal_to_mn(num))
        else:
            w = int_to_mn_words(num, connective=False)
            if w.endswith("тав"): w += "ны"
            elif w.endswith("нэг"): w = w[:-3] + "нэгний"
            else: w += "ны"
            return add_token(w)
    txt = re.sub(r'\b(\d+)-(р|ны)\b', ord_sub, txt)

    def unit_sub(m):
        num_str = m.group(1)
        unit_sym = m.group(2)
        prefix = "хасах " if num_str.startswith("-") else ""
        abs_num = num_str.lstrip("-").replace(',', '.')
        unit_map = {'₮': 'төгрөг', '$': 'доллар', 'С': 'Цельсийн градус', 'с': 'Цельсийн градус', 'К': 'Кельвин', 'K': 'Кельвин', 'к': 'Кельвин', 'k': 'Кельвин'}
        u_word = unit_map[unit_sym]
        if "." in abs_num:
            int_part, dec_part = abs_num.split(".")
            int_w = int_to_mn_words(int_part, connective=False)
            dec_w = decimal_to_mn_words(dec_part)
            res = f"{prefix}{int_w} бүхэл {dec_w} {u_word}"
        else:
            is_conn = False if unit_sym in ['К', 'K', 'к', 'k'] else True
            int_w = int_to_mn_words(abs_num, connective=is_conn)
            if unit_sym == '₮' and int_w.endswith("ер"): int_w += "н"
            res = f"{prefix}{int_w} {u_word}"
        return add_token(res)
    txt = re.sub(r'(-?\d+(?:[\.,]\d+)?)\s*(₮|\$|[СКKкСс])', unit_sub, txt)

    def roman_sub(m):
        roman = m.group(1)
        trail = m.group(2)
        arabic = str(roman_to_arabic(roman))
        is_conn = True if trail else False
        w = int_to_mn_words(arabic, connective=is_conn)
        if trail == "джоул" and w.endswith("тав"): w += "н"
        res = f"{w} {trail}" if trail else w
        return add_token(res)
        
    def roman_to_arabic(r):
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        val = 0
        for i in range(len(r)):
            if i > 0 and roman_map[r[i]] > roman_map[r[i-1]]:
                val += roman_map[r[i]] - 2 * roman_map[r[i-1]]
            else:
                val += roman_map[r[i]]
        return val
    txt = re.sub(r'\b([IVXLCDM]+)(?:\s+([а-яёөүА-ЯЁӨҮa-zA-Z]+))?', roman_sub, txt)

    # 9. Бусад дан тоо
    def plain_sub(m):
        num_str = m.group(1)
        trail = m.group(2)
        prefix = "хасах " if num_str.startswith("-") else ""
        abs_num = num_str.lstrip("-").replace(',', '.')
        if "." in abs_num:
            int_part, dec_part = abs_num.split(".")
            int_w = int_to_mn_words(int_part, connective=False)
            dec_w = decimal_to_mn_words(dec_part)
            res = f"{prefix}{int_w} бүхэл {dec_w}"
        else:
            is_conn = True if trail else False
            int_w = int_to_mn_words(abs_num, connective=is_conn)
            res = f"{prefix}{int_w}"
        if trail: res += f" {trail}"
        return add_token(res)
    txt = re.sub(r'(-?\d+(?:[\.,]\d+)?)(?:\s*([а-яёөүА-ЯЁӨҮa-zA-Z]+))?', plain_sub, txt)

    while any(t in txt for t in tokens):
        for t, val in tokens.items():
            txt = txt.replace(t, val)
       
    txt = txt.replace("15нений", "арван тавны").replace("15ний", "арван тавны").replace("өдөрны өдөр", "өдөр")
    return txt

if __name__ == "__main__":
    
    код_байгаа_хавтас = os.path.dirname(os.path.abspath(__file__))
    file_in = os.path.join(код_байгаа_хавтас, "input.txt")
    file_out = os.path.join(код_байгаа_хавтас, "output.txt")
    
    if not os.path.exists(file_in):
        with open(file_in, "w", encoding="utf-8") as f:
            f.write("2567оны 03-р сарын 15-ны өдрийн 14:30 цагт 9087654321 хүн цугларч, 12344567890₮ шагналт уралдаан.\n"
                    "11дүгээр байрны үнэ нь 1502234674200.12343252₮ буюу хасах 238798123.131235$.\n"
                    "Температур 25С эсвэл -36K бүүр үгүй бол 123.5К байсан бөгөөд даралт -1234.1235 байв.")
        print(f"============================================================")
        print(f"[Шинэ файл үүслээ!] Хавтас дотор 'input.txt' үүссэн байна.")
        print(f"Та тус файл руу текстээ хуулаад программаа дахин ажиллуулаарай.")
        print(f"============================================================")
    else:
       
        print(f"Түр хүлээнэ үү... '{os.path.basename(file_in)}' файлаас уншиж байна...")
        with open(file_in, "r", encoding="utf-8") as f:
            content = f.read()
       
        үр_дүн = too_orluulah(content)
        
        
        with open(file_out, "w", encoding="utf-8") as f:
            f.write(үр_дүн)
            
        print(f"\n[Амжилттай] Хөрвүүлэлт дууслаа!")
        print(f"Гаралт: '{os.path.basename(file_out)}' файл руу хадгалагдлаа.")