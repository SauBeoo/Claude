# -*- coding: utf-8 -*-
"""Chon anh tu lo user gen (Downloads) -> doi ten dung SLIDES -> cat watermark ✦.

- Moi scene co 2 ban (A/B) trong Downloads; chon 1, uu tien ban IT loi text-gia/garbled
  (da soi mat 14/60 anh mau, bat duoc 1 loi: bo 06_gyunyu_bako ban A vi chu tren nap chai
  la ky tu vo nghia, doi sang ban B vi chu "明治牛乳" that va ro net).
- Cat watermark bang CROP (khong va) theo dung khuon strip_wm_crop.py cua co-dai: cat het
  tu x >= CUT_X*W, roi trim day ve dung 16:9. Vi tri ✦ do MAT tren 14 anh mau (~0.928-0.940W)
  -> dung CUT_X=0.915 de an toan (nhieu le hon 1 chut vi CHUA soi het 60/60 anh).
"""
import shutil
from pathlib import Path
from PIL import Image

SRC = Path(r"C:\Users\tuana\Downloads\download (10)")
DST = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\04_showa45-asa\slides_img")
BAK = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\04_showa45-asa\_wm_orig")
CUT_X = 0.915

# (ten dich theo SLIDES/TENFILE, ten file nguon da chon)
PICKS = [
    ("slide_00_00_yoake_roji.jpg", "Empty_residential_lane_at_dawn_202608242352.jpeg"),
    ("slide_01_01_toufuya_jitensha.jpg", "Bicycle_parked_on_residential_lane_202608242352.jpeg"),
    ("slide_02_01b_rappa_close.jpg", "Brass_trumpet_horn_at_dawn_202608242352.jpeg"),
    ("slide_03_02_nabe_te.jpg", "Hand_holding_pot_walking_lane_202608242352.jpeg"),
    ("slide_04_03_toufu_kobore.jpg", "Broken_tofu_in_lane_202608242352.jpeg"),
    ("slide_05_03b_okara_fukuro.jpg", "Handing_paper_bag_of_pulp_202608242352.jpeg"),
    ("slide_06_04_mezamashi_dokei.jpg", "Alarm_clock_on_wooden_stand_202608242352.jpeg"),
    ("slide_07_05_haha_daidokoro_mizu.jpg", "Hands_running_water_at_sink_202608242352.jpeg"),
    ("slide_08_06_gyunyu_bako.jpg", "Milk_bottles_in_delivery_box_202608242352_2.jpeg"),
    ("slide_09_06b_kuriimu_sukuu.jpg", "Child_reaching_into_milk_bottle_202608242352.jpeg"),
    ("slide_10_08_shinbun_toukanguchi.jpg", "Newspaper_wedged_in_mail_slot_202608242352.jpeg"),
    ("slide_11_09_sofu_engawa.jpg", "Elderly_man_holding_open_newspaper_202608242352.jpeg"),
    ("slide_12_10_denkigama_yuge.jpg", "Steam_rising_from_rice_cooker_202608242352.jpeg"),
    ("slide_13_11_chabudai_asagohan.jpg", "Traditional_Japanese_breakfast_t…_202608242352.jpeg"),
    ("slide_14_12_shoyu_tamagogohan.jpg", "Soy_sauce_poured_over_rice_202608242352.jpeg"),
    ("slide_15_13_terebi_ima.jpg", "Family_watching_television_in_room_202608242352.jpeg"),
    ("slide_16_14_terebi_kazoku_chikayoru.jpg", "Family_seated_on_tatami_mats_202608242352.jpeg"),
    ("slide_17_15_sentakumono_hosu.jpg", "Bedsheets_hanging_on_bamboo_pole_202608242352.jpeg"),
    ("slide_18_16_randoseru_genkan.jpg", "School_satchel_at_genkan_entrance_202608242352.jpeg"),
    ("slide_19_17_shudan_tokou.jpg", "Figures_walking_down_residential…_202608242352.jpeg"),
    ("slide_20_18_manin_densha_platform.jpg", "Commuters_waiting_at_train_station_202608242352.jpeg"),
    ("slide_21_19_densha_doa_shimaru.jpg", "Commuters_boarding_crowded_train…_202608242352.jpeg"),
    ("slide_22_20_rajio_taisou_kouen.jpg", "People_doing_morning_calisthenics_202608242352.jpeg"),
    ("slide_23_21_taisou_stampcard.jpg", "Hand_stamping_cardboard_card_202608242352.jpeg"),
    ("slide_24_22_shinbun_midashi_bokeh.jpg", "Hands_holding_open_newspaper_page_202608242352.jpeg"),
    ("slide_25_23_banpaku_gunshuu_toi.jpg", "Crowd_walking_toward_distant_tower_202608242352.jpeg"),
    ("slide_26_24_ie_zentai_asa.jpg", "Showa_era_wooden_house_202608242352.jpeg"),
    ("slide_27_25_gyunyu_kamipakku_ima.jpg", "Milk_carton_beside_apartment_door_202608242352.jpeg"),
    ("slide_28_25b_anpi_kakunin.jpg", "Folded_note_by_milk_carton_202608242352.jpeg"),
    ("slide_29_26_ie_asahi_shizuka.jpg", "Sunlight_streaming_into_tatami_room_202608242352.jpeg"),
]


def main():
    DST.mkdir(parents=True, exist_ok=True)
    BAK.mkdir(parents=True, exist_ok=True)
    n = 0
    for dst_name, src_name in PICKS:
        src = SRC / src_name
        if not src.exists():
            print(f"[LOI] khong thay file nguon: {src_name}")
            continue
        im = Image.open(src).convert("RGB")
        W, H = im.size
        # backup goc (chua cat) truoc khi cat
        im.save(BAK / dst_name, quality=95)
        nw = int(W * CUT_X)
        nh = min(H, int(round(nw * 9 / 16)))
        cropped = im.crop((0, 0, nw, nh)).resize((1376, 768), Image.LANCZOS)
        cropped.save(DST / dst_name, quality=95)
        n += 1
    print(f"OK: dat {n}/{len(PICKS)} anh vao {DST}")
    print(f"backup (chua cat, chua doi ten) o {BAK}")


if __name__ == "__main__":
    main()
