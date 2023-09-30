import re

def xác_suất_xuất_hiện_từ(câu_từ_người_dùng, từ_khả_thi, là_một_từ=False, key_word=[]):
    tần_xuất = 0
    chứa_key_word = True
    for từ in câu_từ_người_dùng:
        if từ in từ_khả_thi: tần_xuất+=1
    
    phần_trăm = float(tần_xuất) / float(len(câu_từ_người_dùng))

    for từ in key_word:
        if từ not in câu_từ_người_dùng:
            chứa_key_word = False
            break
    
    if chứa_key_word or là_một_từ:
        return int(phần_trăm*100)
    else: return 0

def kiểm_tra_câu(danh_sách_từ_trong_câu_của_người_dùng):
    danh_sách_xác_suất_xuất_hiện_cao_nhất = {}

    def phản_hồi(phản_hồi_của_Malfy, danh_sách_các_từ, là_từ_đơn, key_word):
        nonlocal danh_sách_xác_suất_xuất_hiện_cao_nhất
        danh_sách_xác_suất_xuất_hiện_cao_nhất[phản_hồi_của_Malfy] = xác_suất_xuất_hiện_từ(danh_sách_từ_trong_câu_của_người_dùng,danh_sách_các_từ,là_từ_đơn,key_word)

    #Các câu phản hồi =======================================================================================
    phản_hồi("Xin chào!", ["chào","hi","hello","yo"],là_từ_đơn=True,key_word=[])
    phản_hồi("Mình cảm thấy rất khỏe!",["bạn","khỏe","chứ"],là_từ_đơn=False,key_word=["khỏe"])
    phản_hồi("Hẹn gặp lại nhé!", ["tạm","biệt","hẹn","gặp","lại"],là_từ_đơn=False,key_word=["tạm","biệt"])

    câu_phản_hồi_phù_hợp_nhất = max(danh_sách_xác_suất_xuất_hiện_cao_nhất, key=danh_sách_xác_suất_xuất_hiện_cao_nhất.get)

    return câu_phản_hồi_phù_hợp_nhất

def phản_hồi(câu_từ_người_dùng):
    danh_sách_từ_trong_câu_của_người_dùng = re.split(r'\s+|[.;?!,-=]\s*', câu_từ_người_dùng.lower())
    câu_phản_hồi = kiểm_tra_câu(danh_sách_từ_trong_câu_của_người_dùng)
    return câu_phản_hồi

while True:
    print("Malfy: " + phản_hồi(input("Bạn: ")))