import sys
variables = {}

def perform_assignment(line): # "=" Bulduğunda çalıştırılacak fonksiyon, satır parametresini alır ve satırdaki ifadeyi değerlendirme fonksiyonuna gönderir.
    items = [item.strip() for item in line.split('=')] # "="in(varsa birden fazla "="in) taraflarını parçalar indexler.
    variable_name = items[0].strip() # "="in sol taraftaki kısmı
    expression = items[1].strip() # "="in sağ taraftaki kısmı
    result = evaluate_expression(expression) # İfadeyi örneğin "c=a+b"yi değerlendirmek için(operatör var mı yok mu) değerlendirme fonksiyonuna gönderir.
    if 'bastir' in expression: # derleyicinin kullanıcıdan input almasını sağlamak için
        print_target = extract_value(expression, 'bastir')
        print(print_target)
        user_input = input().strip() # kullanıcıdan girdi alır
        variables[variable_name] = user_input # kullanıcıdan alınan girdiyi eşittirin solunda kalan değişkene atar.
    elif result is not None: # Bir değer varsa eşitle
        variables[variable_name] = result

def evaluate_expression(expression):
    expression = expression.replace(' ', '')  # Boşlukları kaldır
    result = evaluate_addition_subtraction(expression)
    return result

def evaluate_addition_subtraction(expression):
    terms = expression.split('+')
    result = evaluate_multiplication_division(terms[0])
    for i in range(1, len(terms)):
        if '-' in terms[i]:
            subtraction_terms = terms[i].split('-')
            result += evaluate_multiplication_division(subtraction_terms[0])
            for j in range(1, len(subtraction_terms)):
                result -= evaluate_multiplication_division(subtraction_terms[j])
        else:
            result += evaluate_multiplication_division(terms[i])
    return result




def evaluate_multiplication_division(term):
    factors = term.split('*')
    result = evaluate_factor(factors[0])
    for i in range(1, len(factors)):
        if '/' in factors[i]:
            division_factors = factors[i].split('/')
            result *= evaluate_factor(division_factors[0])
            for j in range(1, len(division_factors)):
                fractional = evaluate_factor(division_factors[j])
                if fractional == 0:
                    print("Sıfıra bölme hatası")
                    return None
                result /= fractional
        else:
            result *= evaluate_factor(factors[i])
    return result

def evaluate_factor(factor):
    if factor in variables:
        return int(variables[factor])
    try:
        if '(' in factor:  # Eğer faktör içinde parantez varsa, içindeki ifadeyi değerlendir.
            inner_expression = factor[1:-1]  # Parantez içindeki ifadeyi alır.
            return evaluate_expression(inner_expression)
        return int(factor)
    except ValueError:
        return None


def execute_print(line): # İncelenen satırda "yaz" var ise çalışır.
    print_target = extract_value(line, 'yaz')
    print(print_target)

def extract_value(text, command): # Komutu ifadede çıkartır ve ifadeyi çıkarmaya çalışır.
    text_list = text.split(command)
    result = ""
    for item in text_list[1:]: # 1. indexten son indee kadar olan textlerin içinde item'i döndürür.
        value = extract_string_or_variable(item)
        result += str(value)
    return result

def extract_string_or_variable( text): # Parantezlerin içindeki ifade string mi yoksa bir değişken mi tespit eder.
    if text[0] == '(' and (text[1] == '"' or text[1] == "'"): # ilk index açık parantez ve ondan sonra gelen çift tırnak veya tek tırnak işaretiyse gir.
        closing_char = text[1] # çift tırnak veya tek tırnakla başlıyorsa bitişi de aynı olmalı.
        value = ""
        index = 2 # Açık parantez ve tırnak işaretlerini atlayarak başlıyor.
        while index < len(text):
            if text[index] == closing_char and text[index + 1] == ")": # kapanış başlanılan tırnak işaretiyle aynı olmalı ve bir sonraki karakter kapalı parantez olmalı.
                break
            value += text[index]
            index += 1
        return value
    elif text[0] == '(': # Sadece açık parantez ise girer bu şartın yukarıdakinden aşağıda olması önemli eğer bu şart yukarıda olsaydı hep bu şart dönerdi.
        index = 1
        variable_name = ""
        while index < len(text):
            if text[index] == ')':
                break
            variable_name += text[index] # Hangi deişken olduğunu çıkardık.
            index += 1
        variable_name = variable_name.strip()
        return variables.get(variable_name, '') # Parantezin içindekinin değişken olduğunu bulup değeriyle geri dönderdik.
    return ""

def find_equality(line): # Eşitlik veya yazdırma durumu kontrolü yapılır.
    if '=' in line: # Eşitlik bulunduğunda
        perform_assignment(line)
    elif 'yaz' in line: # "yaz" komutu bulunduğunda.
        execute_print(line)
    else:
        print("Bilinmeyen ifade: ", line)

def get_from_file(file_name): # Dosya okunur.
    with open(file_name) as file_object:
        return file_object.read()

def get_lines(file_name): # Dosya okunması ve satırların tek tek ayrılması yapılır.
    text = get_from_file(file_name) # Dosya okuma fonksiyonunu çalıştırır metinler "text" değişkenine atanır.
    lines = text.split("\n")
    for line in lines:
        find_equality(line) # Eşitlik veya yazdırma durumu kontrolü ve işlemlerinin başlatılması için her satırı tek tek gönderilir.


if len(sys.argv) < 2:
    get_lines("deneme.txt")
else:
    dosya_adi = sys.argv[1]
    try:
        with open(dosya_adi, "r") as file:
            text = file.read()
            lines = text.split("\n")
            for line in lines:
                find_equality(line)
    except FileNotFoundError:
        print(f"{dosya_adi} adlı dosya bulunamadı.")



