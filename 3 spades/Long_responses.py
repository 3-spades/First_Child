import random

def unknown():
    phản_hồi = ["...","Ý của bạn là gì nhỉ?", "Bạn có thể viết lại rõ nghĩa hơn để mình có thể hiểu không ?"][random.randrange(4)]
    return phản_hồi
