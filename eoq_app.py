import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------
# Judul & Deskripsi
# ------------------------------
st.title("📦 Aplikasi Perhitungan EOQ (Economic Order Quantity)")
st.markdown("""
Simulasi sistem persediaan untuk menentukan jumlah pemesanan optimal berdasarkan model **EOQ**.
""")

# ------------------------------
# Panduan Penggunaan
# ------------------------------
with st.expander("📘 Panduan Penggunaan Aplikasi"):
    st.markdown("""
    1. Masukkan nilai permintaan tahunan (jumlah unit yang dibutuhkan dalam satu tahun).
    2. Masukkan biaya pemesanan per transaksi (misalnya biaya administrasi, pengiriman, dll).
    3. Masukkan biaya penyimpanan per unit per tahun (biaya gudang, asuransi, penyusutan, dll).
    4. Hasil berupa nilai EOQ, jumlah pesanan per tahun, dan total biaya persediaan.
    5. Grafik akan menampilkan bagaimana biaya total berubah terhadap kuantitas pemesanan.
    """)

# ------------------------------
# Input Data
# ------------------------------
st.header("📝 Input Data")
D = st.number_input("Permintaan Tahunan (unit)", min_value=1, value=1000, step=100)
S = st.number_input("Biaya Pemesanan per Pesanan (Rp)", min_value=0.0, value=50000.0, step=1000.0)
H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", min_value=0.0, value=10000.0, step=500.0)

# ------------------------------
# Perhitungan EOQ
# ------------------------------
if D > 0 and S > 0 and H > 0:
    EOQ = math.sqrt((2 * D * S) / H)
    order_per_year = D / EOQ
    total_cost = (D / EOQ) * S + (EOQ / 2) * H

    # --------------------------
    # Output Hasil
    # --------------------------
    st.header("📊 Hasil Perhitungan")
    st.success(f"**EOQ (Jumlah Pemesanan Optimal):** {EOQ:.2f} unit")
    st.info(f"**Jumlah Pemesanan per Tahun:** {order_per_year:.2f} kali")
    st.warning(f"**Total Biaya Persediaan per Tahun:** Rp {total_cost:,.2f}")

    # --------------------------
    # Grafik Biaya Total vs Kuantitas
    # --------------------------
    st.header("📈 Visualisasi Grafik EOQ")

    Q = np.linspace(1, D, 300)
    TC = (D / Q) * S + (Q / 2) * H  # Total Cost
    OC = (D / Q) * S                # Ordering Cost
    HC = (Q / 2) * H                # Holding Cost

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(Q, TC, label='Total Biaya', color='blue')
    ax.plot(Q, OC, '--', label='Biaya Pemesanan', color='green')
    ax.plot(Q, HC, '--', label='Biaya Penyimpanan', color='red')
    ax.axvline(EOQ, color='gray', linestyle='dashed', label=f'EOQ = {EOQ:.2f}')

    ax.set_xlabel('Jumlah Pemesanan (unit)')
    ax.set_ylabel('Biaya (Rp)')
    ax.set_title('Grafik Biaya EOQ')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

else:
    st.warning("⚠️ Masukkan semua input dengan nilai yang valid dan lebih besar dari nol.")

# ------------------------------
# Footer Konsep
# ------------------------------
st.markdown("---")
st.markdown("""
**📚 Konsep EOQ:**  
Economic Order Quantity (EOQ) adalah model matematika yang digunakan untuk menentukan jumlah pemesanan yang optimal untuk meminimalkan total biaya persediaan (biaya pemesanan + biaya penyimpanan).
""")
