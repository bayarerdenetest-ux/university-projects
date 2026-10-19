import numpy as np 
def convert_to_array(lst):
    to_array = np.array(lst)
    print("төрөл: ", type(to_array))
    return to_array
def get_user_elements():
    our_list = []
    user_input= input("жагсаалт /list/ дээр нэмэх элементээ өгнө үү. оруулсаны дараа exit гэж бичнэ үү: ")
    words = user_input.split()
    for word in words:
        if word.lower() == 'exit':
            break
        our_list.append(word)
    return our_list