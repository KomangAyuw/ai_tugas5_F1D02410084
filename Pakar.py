import argparse
import json
import sys
import textwrap


# Mengatur bagian atutannyaa
def muat_kb(path):
    with open(path, encoding="utf-8") as f:
        kb = json.load(f)
    validasi_kb(kb)
    return kb

def validasi_kb(kb):
    ids = [r["id"] for r in kb["aturan"]]
    if len(ids) != len(set(ids)):
        raise ValueError("ID aturan ada yang kembar")
    for r in kb["aturan"]:
        if r["mode"] not in ("dan", "atau"):
            raise ValueError(f"{r['id']}: mode harus 'dan' atau 'atau'")
        if not r["jika"]:
            raise ValueError(f"{r['id']}: bagian 'jika' kosong")
        sumber = r["sumber"] if isinstance(r["sumber"], list) else [r["sumber"]]
        for s in sumber:
            if s not in kb["sumber"]:
                raise ValueError(f"{r['id']}: sumber {s} tidak ada di daftar sumber")

def fakta_dasar(kb):
    hasil = {r["maka"] for r in kb["aturan"]}
    ditanya = []
    for bagian in kb["bagian"]:
        for f in bagian["fakta"]:
            if f not in hasil:
                ditanya.append(f)
    return ditanya


# FORWARD CHAINING
def terpenuhi(aturan, memori):
    ada = [s in memori for s in aturan["jika"]]
    return all(ada) if aturan["mode"] == "dan" else any(ada)

def forward_chaining(kb, fakta_awal):
    memori = set(fakta_awal)
    asal = {}
    log = []
    while True:
        cocok = [r for r in kb["aturan"]
                 if r["maka"] not in memori and terpenuhi(r, memori)]
        if not cocok:
            break
        r = cocok[0]  # mengambil aturan pertama
        memori.add(r["maka"])
        asal[r["maka"]] = r
        log.append(r)
    return memori, asal, log

def kesimpulan_akhir(kb, memori):
    hasil = []
    for k, d in kb["kesimpulan"].items():
        if k not in memori:
            continue
        if d.get("diganti_oleh") in memori:
            continue
        hasil.append(k)
    return hasil


# MENGATUR TAMPILANNYA
def nama_fakta(kb, f):
    if f in kb["fakta"]:
        return kb["fakta"][f]
    if f in kb["turunan"]:
        return kb["turunan"][f]
    if f in kb["kesimpulan"]:
        return kb["kesimpulan"][f]["nama"]
    return f


def jelaskan(kb, hasil, asal, memori_awal, indent=1, keluar=None, sumber_dipakai=None):
    keluar = keluar if keluar is not None else []
    sumber_dipakai = sumber_dipakai if sumber_dipakai is not None else set()
    pad = "  " * indent
    r = asal[hasil]
    syarat = [s for s in r["jika"] if s in asal or s in memori_awal]
    srcs = r["sumber"] if isinstance(r["sumber"], list) else [r["sumber"]]
    sumber_dipakai.update(srcs)
    keluar.append(f"{pad}{nama_fakta(kb, hasil)}  <- {r['id']} ({r['mode']}: "
                  f"{', '.join(r['jika'])}) [{','.join(srcs)}]")
    for s in syarat:
        if s in asal:
            jelaskan(kb, s, asal, memori_awal, indent + 1, keluar, sumber_dipakai)
        else:
            keluar.append(f"{pad}  {s}: {kb['fakta'][s]} (jawaban: ya)")
    return keluar, sumber_dipakai


def tanya(kb, ya_otomatis=None):
    ditanya = fakta_dasar(kb)
    ya = set()
    print("Jawab y (ya, sesuai dengan saya) atau t (tidak).")
    nomor = 0
    for bagian in kb["bagian"]:
        print(f"\n{bagian['judul']}")
        for f in bagian["fakta"]:
            if f not in ditanya:
                continue
            nomor += 1
            if ya_otomatis is not None:
                jawab = "y" if f in ya_otomatis else "t"
                print(f"{nomor}. {kb['fakta'][f]} (y/t) > {jawab}")
            else:
                while True:
                    jawab = input(f"{nomor}. {kb['fakta'][f]} (y/t) > ").strip().lower()
                    if jawab in ("y", "t"):
                        break
                    print("   Ketik y atau t.")
            if jawab == "y":
                ya.add(f)
    return ya


def anda(teks):
    return "Anda " + teks[5:] if teks.startswith("Saya ") else teks


def bungkus(teks, awal="", lanjut=None, lebar=78):
    return textwrap.fill(teks, width=lebar, initial_indent=awal, subsequent_indent=awal if lanjut is None else lanjut)


def pendukung(hasil, asal, memori_awal, kumpul=None, aturan=None):
    kumpul = kumpul if kumpul is not None else []
    aturan = aturan if aturan is not None else []
    r = asal[hasil]
    aturan.append(r["id"])
    for s in r["jika"]:
        if s in asal:
            pendukung(s, asal, memori_awal, kumpul, aturan)
        elif s in memori_awal and s not in kumpul:
            kumpul.append(s)
    return kumpul, aturan


def tampil_hasil(kb, ya, memori, asal):
    garis = "=" * 72
    print("\n" + garis)
    print("HASIL UNTUK ANDA".center(72))
    print(garis)

    ditanya = fakta_dasar(kb)
    minat = [f for f in ditanya if f.startswith("i_") and f in ya]
    kemampuan = [f for f in ditanya if f.startswith("k_") and f in ya]
    print("\nDari jawaban Anda, kami mencatat:")
    print("  Minat Anda:")
    for f in minat or []:
        print(bungkus(anda(kb["fakta"][f]), "    - ", "      "))
    if not minat:
        print("    (belum ada pernyataan minat yang Anda pilih)")
    print("  Kemampuan Anda:")
    for f in kemampuan:
        print(bungkus(anda(kb["fakta"][f]), "    - ", "      "))
    if not kemampuan:
        print("    (belum ada pernyataan kemampuan yang Anda pilih)")

    kesimpulan = kesimpulan_akhir(kb, memori)
    cocok = [k for k in kesimpulan if kb["kesimpulan"][k].get("tingkat", "cocok") == "cocok"]
    eksplorasi = [k for k in kesimpulan if k not in cocok]
    sumber_dipakai = set()
    nomor = 0

    def kartu(k, jelajah):
        nonlocal nomor
        nomor += 1
        d = kb["kesimpulan"][k]
        daun, aturan = pendukung(k, asal, ya)
        for a in aturan:
            sumber_dipakai.update(next(r["sumber"] for r in kb["aturan"] if r["id"] == a))
        print(f"\n{nomor}. {d['nama'].upper()}")
        print(bungkus("Contoh bidang pekerjaan: " + d["bidang_terkait"] + ".", "   ", "   "))
        print("   Mengapa:")
        for f in daun:
            if f.startswith("i_"):
                print(bungkus("Minat: " + anda(kb["fakta"][f]), "     - ", "       "))
        for f in daun:
            if f.startswith("k_"):
                print(bungkus("Kemampuan: " + anda(kb["fakta"][f]), "     - ", "       "))
        if jelajah:
            print(bungkus("Kemampuan di bidang ini belum terlihat dari jawaban Anda. "
                          "Coba pelajari dan latih dulu, lalu ulangi tes ini.", "     - ", "       "))
        print(bungkus("(Dasar penalaran: aturan " + ", ".join(aturan) + ")", "   ", "   "))

    if cocok:
        print("\nBIDANG KARIER YANG COCOK UNTUK ANDA")
        print("(minat dan kemampuan Anda sama-sama mendukung)")
        for k in cocok:
            kartu(k, False)
    if eksplorasi:
        print("\nBIDANG YANG LAYAK ANDA JELAJAHI LEBIH LANJUT")
        print("(minat Anda cocok, tetapi kemampuannya belum terlihat)")
        for k in eksplorasi:
            kartu(k, True)
    if not kesimpulan:
        print("\nBelum ada bidang karier yang bisa kami sarankan dari jawaban Anda.")
        print(bungkus("Penyebabnya: sistem membutuhkan minimal dua pernyataan minat yang sama-sama "
                      "Anda pilih dalam satu bidang (misalnya dua pernyataan tentang seni), dan "
                      "jawaban Anda belum memenuhi itu."))
        print("Saran: baca ulang pernyataan bagian A, lalu coba lagi.")

    print("\nCatatan penting:")
    print(bungkus(kb.get("batas", ""), "  ", "  "))
    print(garis)


def tampil_detail(kb, ya, memori, asal, log):
    """Detail teknis: jalannya forward chaining dan pohon alasan lengkap."""
    print("\n--- DETAIL TEKNIS ---")
    print("Fakta awal:", ", ".join(sorted(ya)) if ya else "(tidak ada)")
    print()
    for i, r in enumerate(log, 1):
        print(f"Siklus {i}: {r['id']} -> {r['maka']}")
    print(f"Siklus {len(log) + 1}: tidak ada aturan baru, berhenti")
    antara = [f for f in kb["turunan"] if f in memori]
    print("\nFakta antara yang disimpulkan:", ", ".join(antara) if antara else "(tidak ada)")
    kesimpulan = kesimpulan_akhir(kb, memori)
    if kesimpulan:
        sumber_dipakai = set()
        print("\nAlasan (pohon aturan):")
        for k in kesimpulan:
            baris, sd = jelaskan(kb, k, asal, ya)
            sumber_dipakai |= sd
            print("\n".join(baris))
        print("\nSumber aturan yang dipakai:")
        for s in sorted(sumber_dipakai):
            print(f"  {s}: {kb['sumber'][s]}")


def main():
    ap = argparse.ArgumentParser(description="KarirKu: sistem pakar rekomendasi bidang karier (forward chaining)")
    ap.add_argument("--kb", default="kb_karier.json", help="file aturan (default: kb_karier.json)")
    ap.add_argument("--ya", help="mode otomatis: daftar fakta 'ya' dipisah koma (kosong = tidak ada)")
    ap.add_argument("--detail", action="store_true", help="tampilkan juga detail teknis (siklus dan aturan)")
    args = ap.parse_args()

    kb = muat_kb(args.kb)
    print(kb["judul"])
    print(kb["sasaran"])

    ya_otomatis = None
    if args.ya is not None:
        ya_otomatis = {x.strip() for x in args.ya.split(",") if x.strip()}
        salah = ya_otomatis - set(fakta_dasar(kb))
        if salah:
            sys.exit(f"Fakta tidak dikenal: {', '.join(sorted(salah))}")

    print()
    ya = tanya(kb, ya_otomatis)
    memori, asal, log = forward_chaining(kb, ya)

    tampil_hasil(kb, ya, memori, asal)

    if ya_otomatis is None and not args.detail:
        jawab = input("\nTampilkan detail teknis (siklus dan aturan lengkap)? (y/t) > ").strip().lower()
        args.detail = jawab == "y"
    if args.detail:
        tampil_detail(kb, ya, memori, asal, log)


if __name__ == "__main__":
    main()