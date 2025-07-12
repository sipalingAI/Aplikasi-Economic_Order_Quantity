import streamlit as st
import math

# Judul
st.title("📦 Perhitungan EOQ (Economic Order Quantity)")
st.write("Simulasi sistem persediaan untuk menentukan jumlah pemesanan optimal.")

# Input pengguna
st.header("📝 Input Data")
D = st.number_input("Permintaan Tahunan (unit)", min_value=1, value=1000, step=10)
S = st.number_input("Biaya Pemesanan per Pesanan (Rp)", min_value=0.0, value=50000.0, step=1000.0)
H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", min_value=0.0, value=10000.0, step=500.0)

# Hitung EOQ
if D > 0 and S > 0 and H > 0:
    EOQ = math.sqrt((2 * D * S) / H)
    total_order = D / EOQ
    total_cost = (D / EOQ) * S + (EOQ / 2) * H

    st.header("📊 Hasil Perhitungan")
    st.write(f"**EOQ (Jumlah Pemesanan Optimal):** {EOQ:.2f} unit")
    st.write(f"**Jumlah Pemesanan per Tahun:** {total_order:.2f} kali")
    st.write(f"**Total Biaya Persediaan per Tahun:** Rp {total_cost:,.2f}")
else:
    st.warning("Silakan masukkan semua input dengan nilai yang lebih besar dari nol.")

# Catatan
st.markdown("---")
st.markdown("**Konsep:** Inventory Model – EOQ Formula")
