import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# Judul Aplikasi
# -----------------------------
st.set_page_config(page_title="EOQ Calculator", layout="centered")
st.title("📦 Aplikasi Perhitungan EOQ (Economic Order Quantity)")
st.markdown("""
Aplikasi ini digunakan untuk menghitung **jumlah pemesanan optimal (EOQ)** guna meminimalkan total biaya persediaan.
""")

# -----------------------------
# Panduan Penggunaan
# -----------------------------
with st.expander("📘 Panduan Penggunaan"):
    st.markdown("""
    1. Masukkan jumlah permintaan tahunan (unit).
    2. Masukkan biaya pemesanan per pesanan (Rp).
    3. Masukkan biaya penyimpanan per unit per tahun (Rp).
    4. Tekan tombol **Hitung** untuk melihat hasil perhitungan EOQ, biaya total, dan grafik visualisasi.
    """)

# -----------------------------
# Input User
# -----------------------------
st.header("🧮 Input Data")
D = st.number_input("Permintaan Tahunan (unit) - D", min_value=1, value=1000, step=100)
S = st.number_input("Biaya Pemesanan per Pesanan (Rp) - S", min_value=0.0, value=50000.0, step=1000.0)
H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp) - H", min_value=0.0, value=10000.0, step=500.0)

# -----------------------------
# Tampilkan Rumus EOQ
# -----------------------------
st.header("📐 Rumus EOQ yang Digunakan")
st.latex(r''' 
EOQ = \sqrt{\frac{2DS}{H}} 
''')
st.markdown("""
**Keterangan:**
- `D`: Permintaan tahunan  
- `S`: Biaya pemesanan per pesanan  
- `H`: Biaya penyimpanan per unit per tahun
""")

# -----------------------------
# Perhitungan EOQ
# -----------------------------
if st.button("Hitung EOQ"):
    if D > 0 and S > 0 and H > 0:
        EOQ = math.sqrt((2 * D * S) / H)
        orders_per_year = D / EOQ
        total_cost = (D / EOQ) * S + (EOQ / 2) * H

        # -------------------------
        # Hasil Perhitungan
        # -------------------------
        st.header("✅ Hasil Perhitungan")
        st.success(f"**EOQ (Jumlah Pesanan Optimal):** {EOQ:.2f} unit")
        st.info(f"**Jumlah Pemesanan per Tahun:** {orders_per_year:.2f} kali")
        st.warning(f"**Total Biaya Persediaan:** Rp {total_cost:,.2f}")

        # -------------------------
        # Grafik Visualisasi Biaya
        # -------------------------
        st.header("📊 Grafik Visualisasi Biaya")
        Q = np.linspace(1, D, 300)
        TC = (D / Q) * S + (Q / 2) * H
        OC = (D / Q) * S
        HC = (Q / 2) * H

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(Q, TC, label='Total Biaya', color='blue')
        ax.plot(Q, OC, '--', label='Biaya Pemesanan', color='green')
        ax.plot(Q, HC, '--', label='Biaya Penyimpanan', color='red')
        ax.axvline(EOQ, color='gray', linestyle='dashed', label=f'EOQ = {EOQ:.2f}')

        ax.set_xlabel('Kuantitas Pemesanan (unit)')
        ax.set_ylabel('Biaya (Rp)')
        ax.set_title('Kurva Biaya Persediaan vs Kuantitas')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # -------------------------
        # Penjelasan Ringkas
        # -------------------------
        st.markdown("---")
        st.markdown("""
        ✅ **Interpretasi Hasil:**
        - Dengan memesan sebanyak **{:.0f} unit** setiap kali, perusahaan akan menekan total biaya persediaan tahunan.
        - Total biaya meliputi biaya pemesanan dan biaya penyimpanan yang saling memengaruhi.
        """.format(EOQ))
    else:
        st.error("Mohon masukkan semua nilai input dengan benar.")
