# -*- coding: utf-8 -*-
r"""Sinh 105 prompt clip cho video 30 -> FLOW (extension) + TENFILE.

MOT FILE duy nhat (user chot 2026-09-06: *"viet chung vao 1 file thoi"*).

Khuon chep tu video 29. Khac 29 o mot cho co chu y: video 29 ghi
`no modern appliances` cho MOI clip; bai 30 co may say futon / tiem giat / may
hut bui nen tong IMA duoc phep do hien dai — xem BLOCKS.md muc TONG SANG.

    python tools\gen_prompts30.py
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:\Claude\Projects\youtube-jp-co-dai\06_VIDEO\30_futon-dani-uchinaoshi")

BASE = ("photorealistic, documentary style, soft 16mm film grain, shallow depth of field, "
        "locked-off tripod")
NEG = "no text, no letters, no logo, no watermark, no face visible. 16:9, 8 seconds."

TONE = {
    "SHOJI": "old Japanese wooden house, soft diffused light from a paper shoji window, "
             "warm faded palette, weathered wood, tatami floor, no modern appliances in frame",
    "NATSU": "wooden veranda of an old Japanese house, harsh midsummer overhead sun, heat haze, "
             "bleached highlights, humid still air, no modern appliances in frame",
    "FUYU":  "wooden veranda of an old Japanese house, cold clear winter morning, low slanting sun, "
             "crisp dry air, pale blue sky, bare branches, visible frost, no modern appliances in frame",
    "IMA":   "plain modern Japanese apartment interior, flat neutral daylight, cool white tone",
    "KOUBOU": "old futon workshop, warm low side light, deep shadows, dust motes in a shaft of light, "
              "soot-stained timber, no modern appliances in frame",
}

# (so, ton, ten file, canh, MOTION)
C = [
 (1,"SHOJI","asa_futon_tatami","a cotton futon laid out on a tatami floor in a dim morning room","fine dust motes drifting slowly through a slanting shaft of light"),
 (2,"SHOJI","macro_wata_hokori","extreme macro of cotton futon fibres","tiny white dust particles settling down between the fibres"),
 (3,"SHOJI","tatamu_hokori","two hands gripping the edge of a futon and starting to fold it","the fabric lifts and a cloud of dust bursts out into the light beam"),
 (4,"SHOJI","hakobu_senaka","seen from behind, a person carrying a folded futon toward a closet","a halo of dust drifting slowly around the shoulders"),
 (5,"SHOJI","nozzle_oku","a vacuum cleaner nozzle being lowered onto a white futon surface","the nozzle begins to glide, the fabric sinking under its mouth"),
 (6,"SHOJI","macro_nozzle","macro of a vacuum nozzle mouth passing over woven fabric","cotton fibres standing up then lying flat as the nozzle passes"),
 (7,"SHOJI","macro_seni_hikari","extreme macro of woven fabric threads in raking light","a few white dust grains rolling between the thread valleys"),
 (8,"SHOJI","hikari_toosu","light shining through a stretched futon panel from behind","the internal cotton structure emerging as the light grows"),
 (9,"SHOJI","kakuhi_otiru","a hand rubbing a forearm above a dark cloth","white flakes of dust drifting down onto the dark fabric"),
 (10,"SHOJI","wata_dansou","macro cross-section of layered cotton wadding","light sweeping slowly from the outer layer inward"),
 (11,"SHOJI","koyomi_kabe","an old paper calendar hanging on a wooden wall, no readable text","a page fluttering gently in a draught"),
 (12,"NATSU","hosu_ranakan","a futon draped over a wooden veranda rail under a blazing summer sun","the fabric bulging slightly in hot wind, heat haze rippling above it"),
 (13,"NATSU","ondokei_ue","a mercury thermometer lying flat on the sunlit futon surface","the mercury column rising slowly"),
 (14,"NATSU","macro_netsu","macro of the futon surface under harsh noon sun","heat haze distorting the surface"),
 (15,"NATSU","te_osu_atsui","a palm pressing down onto the hot futon surface","the fabric compressing, then the hand pulling back"),
 (16,"NATSU","urasokumen_kage","the UNDERSIDE of the same hanging futon, in shade","dark, damp, completely still air, no heat shimmer"),
 (17,"NATSU","dansou_hikari","cross-section of a futon: bright outer edge, dark inner core","light stopping at the second layer of cotton"),
 (18,"NATSU","yuuhi_futon","late afternoon sun casting long shadows across the hanging futon","the shadow line creeping across the frame"),
 (19,"NATSU","sentakubasami","a hand removing a wooden clothes peg from the futon edge","the peg springing open, the fabric dropping"),
 (20,"NATSU","shitsudokei","a round dial hygrometer hanging on a veranda post, no readable text","the needle trembling then settling"),
 (21,"NATSU","yuge_agaru","moisture rising off the futon surface in sunlight","a faint plume of vapour lifting and dissolving"),
 (22,"NATSU","macro_shizuku","macro of a water droplet clinging to a cotton fibre","the droplet shrinking as it dries"),
 (23,"NATSU","kaze_fukuramu","the futon billowing as wind passes underneath","slow rolling waves across the fabric"),
 (24,"SHOJI","futontataki_kake","a bamboo futon beater hanging on a wooden wall","the beater swaying very slightly"),
 (25,"NATSU","te_furiageru","a hand gripping the beater handle, raised","the forearm swinging into the stroke"),
 (26,"NATSU","tataku_shunkan","the exact moment the beater strikes the hanging futon","a cloud of dust bursting outward, the fabric denting inward"),
 (27,"NATSU","hokori_taiyou","the dust cloud suspended in a sunbeam","dust grains swirling then drifting sideways"),
 (28,"SHOJI","macro_ochiru","macro of dust settling onto a tatami mat","grains sinking into the woven grooves"),
 (29,"NATSU","danchi_monohoshi","a row of drying poles at an old housing block, many futons hung side by side at dusk","a few futons swaying; a distant figure seen from behind swinging a beater"),
 (30,"IMA","souji_futon","a vacuum nozzle sliding across a futon surface","fabric rippling along the nozzle mouth"),
 (31,"IMA","macro_tatsu","macro of cotton fibres standing up under suction","fibres springing up then lying down"),
 (32,"IMA","dansou_ugokanai","cross-section of a futon: the top layer moving, the deep layer completely still","motion confined to the upper fifth of the frame"),
 (33,"SHOJI","kyuuban_shigamitsuku","abstract macro: a tiny sucker-tipped claw gripping a thick fabric fibre","the claw tightening its grip, refusing to let go"),
 (34,"IMA","dust_box","a transparent vacuum dust container filled with grey dust","dust swirling inside the clear chamber"),
 (35,"IMA","akeru_shiroi","dust being tipped from the container onto a sheet of white paper","the dust falling into a small mound"),
 (36,"SHOJI","koyomi_kasanaru","two old calendar sheets overlapping on a wooden table, no readable text","the top sheet flipping over in a draught"),
 (37,"SHOJI","oshiire_sukima","folded futons stacked inside a closet, the sliding door slightly ajar","light entering through the narrow gap"),
 (38,"SHOJI","oshiire_akeru","the closet door sliding open","a plume of dust bursting out into the light beam"),
 (39,"SHOJI","asa_suwaru","a person sitting on a futon in the morning, shoulders and back only","shoulders rising and falling with slow breathing"),
 (40,"IMA","ippoukou","a vacuum nozzle moving slowly in ONE direction across a futon","the nozzle gliding steadily, never reversing"),
 (41,"IMA","stopwatch","a stopwatch resting beside the futon, no readable text","the second hand ticking forward"),
 (42,"IMA","tekubi_yurumeru","a hand holding the vacuum handle, wrist relaxed","the arm pushing slowly and evenly"),
 (43,"IMA","sheets_hagasu","hands stripping a fitted sheet off a futon","the fabric sliding free and folding over"),
 (44,"IMA","kansouki_sasu","a futon dryer beside a futon, its hose inserted under the cover","the hose beginning to inflate"),
 (45,"IMA","fukuramu_futon","the futon swelling as hot air fills it","the surface tightening and rising slowly"),
 (46,"IMA","timer_tatami","a mechanical timer dial set on the floor, no readable text","the dial hand turning"),
 (47,"IMA","coin_laundry","a coin laundry at night, a row of large dryers","fluorescent light, one drum turning"),
 (48,"IMA","drum_mado","looking through the round glass door of a dryer drum","a futon tumbling slowly inside"),
 (49,"NATSU","kuroi_fukuro","a large black plastic bag placed on sunlit concrete","the bag inflating with hot air"),
 (50,"NATSU","macro_kuroi","macro of the black bag surface under harsh sun","heat haze shimmering over the plastic"),
 (51,"NATSU","ondokei_fukuro","a thermometer slipped into the mouth of the black bag","the mercury column climbing quickly"),
 (52,"NATSU","fukuro_akeru","two hands opening the mouth of the bag","hot air escaping, briefly fogging the lens"),
 (53,"IMA","shimau_manzoku","a warm futon being carried into a closet, seen from behind","the shoulders relaxing as the futon is set down inside"),
 (54,"IMA","souji_atotsuki","a vacuum nozzle gliding over a freshly dried futon","fibres flattening in the nozzle path"),
 (55,"SHOJI","shimau_shimeru","a warm futon being put into the closet, the door sliding shut","the light gap narrowing then going dark"),
 (56,"IMA","tana_sheets","a shop shelf stacked with folded anti-mite sheets, no readable text, no brand logo","light sweeping across the shelf"),
 (57,"IMA","spray_toru","a spray bottle on a shelf, a hand reaching for it","the hand lifting the bottle off the shelf"),
 (58,"IMA","kago_oku","a plastic shopping basket holding a few fabric packages","the basket being set down on a counter"),
 (59,"SHOJI","kozeni_tsukue","a few coins and a banknote on a wooden table","one coin rolling then toppling flat"),
 (60,"SHOJI","engawa_karappo","an empty old wooden veranda in late afternoon light","a pillar shadow creeping slowly across the floorboards"),
 (61,"KOUBOU","futonya_omote","the storefront of an old futon shop, wooden sliding door and frosted glass","a noren curtain swaying gently"),
 (62,"KOUBOU","furui_futon_yuka","a flattened old futon spread on the workshop floor","dust puffing up as the fabric touches the boards"),
 (63,"KOUBOU","ito_hodoku","hands unpicking the stitching along a futon edge","a long thread being drawn out of the fabric"),
 (64,"KOUBOU","wata_dasu","clumped old wadding being pulled out of the cover","mass after mass of cotton spilling out"),
 (65,"KOUBOU","macro_katamari","macro of a hard grey clump of old cotton","light sweeping across the matted surface"),
 (66,"KOUBOU","kikai_mawaru","an old cotton-carding machine in the workshop, its drum turning","the drum rotating steadily, cotton drawn in"),
 (67,"KOUBOU","wata_kumo","cotton pouring out of the machine as a white cloud-like layer","the layer flowing out slowly and swelling"),
 (68,"KOUBOU","sou_kasaneru","thin layers of cotton stacked on a work table","hands laying down one more layer"),
 (69,"KOUBOU","fuchi_tatamu","two hands folding the edge of a cotton layer","the edge being smoothed flat"),
 (70,"KOUBOU","atarashii_nuno","new fabric unrolled across the wooden table","the cloth unfurling to cover the table"),
 (71,"KOUBOU","wata_ireru","the cotton layer being laid into the middle of the new cloth","the cotton settling, the fabric sinking"),
 (72,"KOUBOU","hari_toosu","a large needle passing through the fabric edge","the needle drawing thread through"),
 (73,"KOUBOU","atsui_futon","the finished thicker futon resting on the floor","a hand stroking along its surface"),
 (74,"KOUBOU","osu_modoru","a palm pressing down on the new futon then lifting away","the surface springing back up"),
 (75,"KOUBOU","watayumi_kabe","an old bamboo bow with a taut string hanging on the workshop wall","the bowstring vibrating faintly"),
 (76,"SHOJI","riyakaa_mae","a wooden hand-cart parked in front of a house, futons loaded on it","the wheel inching forward one turn"),
 (77,"SHOJI","koyomi_hashira","an old paper calendar hanging on a house pillar, no readable text","one page turning over"),
 (78,"SHOJI","kibako_akeru","an old wooden box with a sliding lid on the tatami","the lid pushed open, dust lifting"),
 (79,"SHOJI","azekura_tooku","an ancient raised wooden storehouse seen from across a gravel courtyard","leaves blowing across the frame"),
 (80,"SHOJI","kura_tobira","the storehouse door standing ajar, light entering the interior","the light patch widening across the floor"),
 (81,"SHOJI","kofu_take","antique textiles draped over bamboo racks in a courtyard","the cloths swaying in a light breeze"),
 (82,"SHOJI","nuno_kakeru","a hand laying one more cloth over the bamboo rack","the cloth falling open across the pole"),
 (83,"FUYU","shimo_niwa","a house courtyard on a winter morning, frost on the gravel","cold vapour rising faintly off the stones"),
 (84,"FUYU","fuyu_hosu","a futon draped over the rail under a deep blue winter sky with bare branches","the fabric hanging flat, no heat shimmer at all"),
 (85,"FUYU","shiroi_iki","white breath escaping into the freezing air","the plume expanding then dissolving"),
 (86,"FUYU","shitsudokei_fuyu","a hygrometer on the veranda post in winter light, no readable text","the needle resting still at a low position"),
 (87,"FUYU","fuyu_hikari","low winter sun raking across the futon surface","the band of light travelling slowly"),
 (88,"FUYU","macro_kawaita","macro of dry cotton fibres, curled and loose","fibres unfurling slightly as they dry"),
 (89,"FUYU","te_tsumetai","a palm laid flat on the cold dry futon surface","the hand pressing then lifting away"),
 (90,"FUYU","tatamu_hokori_nashi","the futon being folded outdoors in the cold","folding with almost no dust rising at all"),
 (91,"NATSU","hikaku_natsu","the same veranda in humid summer","the air thick and hazy, the light flat and washed out"),
 (92,"FUYU","hikaku_fuyu","the same veranda in clear winter","the air perfectly transparent, every edge sharp"),
 (93,"FUYU","kakedokei","an old wall clock showing a morning hour, no readable text","the minute hand advancing"),
 (94,"FUYU","urakaesu","two hands flipping the futon over on the rail","the futon turning, the other face coming up"),
 (95,"FUYU","toriKomu","a hand pulling the futon off the rail in the afternoon","the fabric drawn in toward the body"),
 (96,"SHOJI","samasu_yuge","the futon laid in the middle of the room, warmth rising off it","a faint plume lifting from the surface"),
 (97,"SHOJI","genkan_aku","the entrance sliding door opening, a figure standing outside","the door sliding open, light flooding in"),
 (98,"SHOJI","tsumamu_wata","an aged hand pinching a tuft of cotton from the futon edge","the fingers rolling the tuft"),
 (99,"SHOJI","peshanko_genkan","a completely flattened futon spread out in the entrance hall","the fabric being smoothed out flat"),
 (100,"SHOJI","tenohira_wata","an old tuft of cotton resting on an upturned palm","the tuft expanding slightly as the hand opens"),
 (101,"SHOJI","oshiire_oku","the closet open, an old cotton futon lying at the very back","light reaching in and falling across the fabric"),
 (102,"SHOJI","hikidasu","two hands pulling the old futon out of the closet","the futon sliding out, thin dust lifting"),
 (103,"FUYU","hirogeru_fuyu","the futon unfolded under winter sunlight","the fabric opening out and puffing up"),
 (104,"FUYU","engawa_fuyu","the winter veranda, the futon full of sunlight","the fabric undulating gently"),
 (105,"SHOJI","techou_hiraku","an open notebook on a wooden table, a pencil lying across it, no readable text","the page fluttering, the pencil rolling slightly"),
]


def build(no, tone, fn, scene, motion):
    return (f"{scene}. MOTION: {motion}. {TONE[tone]}. {BASE}. {NEG}")


def main():
    assert len(C) == 105, len(C)
    assert len({c[2] for c in C}) == 105, "trung ten file"
    io.open(VD / "video_prompts_FLOW.txt", "w", encoding="utf-8").write(
        "\n".join(build(*r) for r in C) + "\n")
    io.open(VD / "video_prompts_TENFILE.txt", "w", encoding="utf-8").write(
        "\n".join(f"{r[0]} -> {r[2]}.mp4 | {r[3]}" for r in C) + "\n")
    print(f"video_prompts_FLOW.txt: {len(C)} prompt · "
          f"dai TB {sum(len(build(*r)) for r in C)//len(C)} ky")

    bad = [r[0] for r in C if "MOTION:" not in build(*r) or "16:9" not in build(*r)]
    print("thieu MOTION/16:9:", bad or "0 ✅")
    cam = ["whip pan", "orbit", "drone", "fast zoom"]
    print("camera cam:", [r[0] for r in C if any(k in build(*r) for k in cam)] or "0 ✅")
    print("tong theo tone:", {t: sum(1 for r in C if r[1] == t) for t in TONE})


if __name__ == "__main__":
    main()
