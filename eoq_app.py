import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aplikasi EOQ", layout="centered")

# Judul dan Panduan
st.title("📦 Aplikasi Perhitungan EOQ (Economic Order Quantity)")

with st.expander("📘 Panduan Penggunaan"):
    st.markdown("""
Economic Order Quantity (EOQ) adalah metode untuk menentukan jumlah pesanan optimal yang meminimalkan total biaya persediaan.

### 📐 Rumus yang Digunakan:

**Rumus Klasik:**  
\\[
EOQ = \\sqrt{\\frac{2 \\times R \\times S}{H}}
\\]

**Rumus Persentase:**  
\\[
EOQ = \\sqrt{\\frac{2 \\times R \\times S}{P \\times I}}
\\]

---

**Keterangan variabel:**
- R = Jumlah kebutuhan tahunan (unit)
- S = Biaya pemesanan per pesanan
- H = Biaya simpan per unit per tahun
- P = Harga beli per unit
- I = Persentase biaya simpan tahunan (desimal)

Aplikasi ini memiliki dua bagian perhitungan terpisah.
""")

# =========================
# Input Data Umum
# =========================
st.header("📝 Input Data Umum")
R = st.number_input("Jumlah kebutuhan tahunan (R) dalam unit", min_value=1.0, value=1200.0, format="%.0f")
S = st.number_input("Biaya pemesanan per pesanan (S) dalam rupiah", min_value=0.0, value=15000000.0, format="%.0f")

# =========================
# EOQ - Rumus Klasik
# =========================
st.subheader("📊 Perhitungan EOQ - Rumus Klasik")

H = st.number_input("Biaya simpan per unit per tahun (H) dalam rupiah", min_value=0.01, value=40000.0, format="%.0f")

if H > 0:
    eoq_klasik = math.sqrt((2 * R * S) / H)
    st.success(f"📦 EOQ (Klasik) = {eoq_klasik:,.2f} unit")

    # Visualisasi Grafik EOQ Klasik
    st.markdown("### 📈 Grafik Biaya Total - Rumus Klasik")
    Q_range = range(int(eoq_klasik * 0.5), int(eoq_klasik * 1.5) + 1, max(1, int(eoq_klasik / 10)))
    grafik_data = []
    for Q in Q_range:
        OC = (R / Q) * S  # Ordering Cost
        HC = (Q / 2) * H  # Holding Cost
        TC = OC + HC
        grafik_data.append({"Q": Q, "Biaya Total": TC, "Biaya Simpan": HC, "Biaya Pesan": OC})
    
    df_klasik = pd.DataFrame(grafik_data)
    fig1, ax1 = plt.subplots()
    ax1.plot(df_klasik["Q"], df_klasik["Biaya Total"], label="Total Cost", color="blue")
    ax1.plot(df_klasik["Q"], df_klasik["Biaya Simpan"], label="Holding Cost", linestyle="--", color="green")
    ax1.plot(df_klasik["Q"], df_klasik["Biaya Pesan"], label="Ordering Cost", linestyle="--", color="red")
    ax1.axvline(eoq_klasik, color="gray", linestyle=":", label="EOQ")
    ax1.set_xlabel("Kuantitas Pesan (Q)")
    ax1.set_ylabel("Biaya (Rp)")
    ax1.set_title("Kurva Biaya EOQ - Rumus Klasik")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

# =========================
# EOQ - Rumus Persentase
# =========================
st.subheader("📊 Perhitungan EOQ - Rumus Persentase")

P = st.number_input("Harga beli per unit (P) dalam rupiah", min_value=0.01, value=1000000.0, format="%.0f")
I_percent = st.number_input("Persentase biaya simpan per tahun (I) dalam %", min_value=0.01, value=40.0, format="%.2f")
I = I_percent / 100  # ubah ke desimal

if P > 0 and I > 0:
    H_persen = P * I
    eoq_persen = math.sqrt((2 * R * S) / H_persen)
    st.success(f"📦 EOQ (Persentase) = {eoq_persen:,.2f} unit")

    # Visualisasi Grafik EOQ Persentase
    st.markdown("### 📈 Grafik Biaya Total - Rumus Persentase")
    Q_range = range(int(eoq_persen * 0.5), int(eoq_persen * 1.5) + 1, max(1, int(eoq_persen / 10)))
    grafik_data2 = []
    for Q in Q_range:
        OC = (R / Q) * S
        HC = (Q / 2) * H_persen
        TC = OC + HC
        grafik_data2.append({"Q": Q, "Biaya Total": TC, "Biaya Simpan": HC, "Biaya Pesan": OC})
    
    df_persen = pd.DataFrame(grafik_data2)
    fig2, ax2 = plt.subplots()
    ax2.plot(df_persen["Q"], df_persen["Biaya Total"], label="Total Cost", color="blue")
    ax2.plot(df_persen["Q"], df_persen["Biaya Simpan"], label="Holding Cost", linestyle="--", color="green")
    ax2.plot(df_persen["Q"], df_persen["Biaya Pesan"], label="Ordering Cost", linestyle="--", color="red")
    ax2.axvline(eoq_persen, color="gray", linestyle=":", label="EOQ")
    ax2.set_xlabel("Kuantitas Pesan (Q)")
    ax2.set_ylabel("Biaya (Rp)")
    ax2.set_title("Kurva Biaya EOQ - Rumus Persentase")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

st.caption("© 2025 | Aplikasi EOQ Dua Metode Rumus | Model Matematika dalam Industri")