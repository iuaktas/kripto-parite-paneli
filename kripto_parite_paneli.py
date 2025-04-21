import streamlit as st
import requests
import pandas as pd

def fiyatlari_cek(kripto_listesi, para_birimi="usd"):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(kripto_listesi),
        "vs_currencies": para_birimi
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Veri çekme hatası! HTTP Kod: {response.status_code}")
        return None

def main():
    st.set_page_config(page_title="Kripto Parite Paneli", layout="centered")
    st.title("💹 Kripto Parite Paneli")
    st.write("Gerçek zamanlı kripto parite fiyatları (Kaynak: CoinGecko API)")

    kriptolar = ["bitcoin", "ethereum", "solana", "ripple", "dogecoin"]
    secilen_kriptolar = st.multiselect("Pariteleri seç:", kriptolar, default=kriptolar)

    if secilen_kriptolar:
        fiyatlar = fiyatlari_cek(secilen_kriptolar)

        if fiyatlar:
            # Bu kısmı ekleyelim
            st.write(fiyatlar)  # Çekilen veriyi ekrana yazdıralım

            tablo = []
            for kripto in secilen_kriptolar:
                fiyat = fiyatlar.get(kripto, {}).get("usd", "Veri Yok")
                tablo.append({"Kripto": kripto.capitalize(), "Fiyat (USD)": fiyat})

            df = pd.DataFrame(tablo)
            st.table(df)
        else:
            st.warning("Veri alınamadı.")
    else:
        st.info("Lütfen en az bir kripto para seçin.")

if __name__ == "__main__":
    main()