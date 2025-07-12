import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Judul
st.title("📦 Aplikasi Perhitungan EOQ")
st.markdown("Hitung Economic Order Quantity (EOQ) menggunakan dua metode yang berbeda dalam satu aplikasi.")

# Pilihan rumus
metode = st.selectbox("Pilih Metode Perhitungan EOQ:", ["Rumus 1 - Biaya Simpan Langsung (H)", "Rumus 2 - Berdasarkan Harga Unit dan Persentase (P × I)"])

# Input kebutuhan dan biaya pesan (umum untuk semua metode)
st.header("📥 Input Data Umum")
R = st.number_input("Jumlah kebutuhan tahunan (R) dalam unit", min_value=1.0, value=5000.0)
S = st.number_input("Biaya pemesanan per pesanan (S) dalam rupiah", min_value=0.0, value=200000.0)

# Proses sesuai metode
if metode == "Rumus 1 - Biaya Simpan Langsung (H)":
    st.subheader("🔹 Input Rumus 1")
    H = st.number_input("Biaya simpan per unit per tahun (H) dalam rupiah", min_value=0.0, value=5000.0)
    
    EOQ = np.sqrt((2 * R * S) / H)
    total_cost = (R / EOQ) * S + (EOQ / 2) * H

    st.header("📊 Hasil Perhitungan EOQ - Rumus 1")
    st.markdown(f"**EOQ = {EOQ:.2f} unit**")
    st.markdown(f"**Total biaya persediaan = Rp {total_cost:,.2f}**")

    # Grafik
    Q_range = np.arange(100, int(EOQ*1.5), 10)
    ordering_costs = (R / Q_range) * S
    holding_costs = (Q_range / 2) * H
    total_costs = ordering_costs + holding_costs

    plt.figure(figsize=(10, 5))
    plt.plot(Q_range, ordering_costs, label='Biaya Pemesanan', linestyle='--')
    plt.plot(Q_range, holding_costs, label='Biaya Penyimpanan', linestyle='--')
    plt.plot(Q_range, total_costs, label='Total Biaya', color='blue')
    plt.axvline(EOQ, color='red', linestyle=':', label='EOQ')
    plt.xlabel('Jumlah Pemesanan (Q)')
    plt.ylabel('Biaya (Rp)')
    plt.title('Grafik Biaya EOQ - Rumus 1')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

elif metode == "Rumus 2 - Berdasarkan Harga Unit dan Persentase (P × I)":
    st.subheader("🔹 Input Rumus 2")
    P = st.number_input("Harga beli per unit (P) dalam rupiah", min_value=0.0, value=50000.0)
    I_percent = st.number_input("Persentase biaya simpan per tahun (I) dalam %", min_value=0.0, value=10.0)
    I_decimal = I_percent / 100
    H = P * I_decimal

    EOQ = np.sqrt((2 * R * S) / H)
    total_cost = (R / EOQ) * S + (EOQ / 2) * H

    st.header("📊 Hasil Perhitungan EOQ - Rumus 2")
    st.markdown(f"**EOQ = {EOQ:.2f} unit**")
    st.markdown(f"**Total biaya persediaan = Rp {total_cost:,.2f}**")
    st.markdown(f"**Biaya simpan dihitung dari H = P × I = {P:.0f} × {I_decimal:.2f} = Rp {H:,.2f}**")

    # Grafik
    Q_range = np.arange(100, int(EOQ*1.5), 10)
    ordering_costs = (R / Q_range) * S
    holding_costs = (Q_range / 2) * H
    total_costs = ordering_costs + holding_costs

    plt.figure(figsize=(10, 5))
    plt.plot(Q_range, ordering_costs, label='Biaya Pemesanan', linestyle='--')
    plt.plot(Q_range, holding_costs, label='Biaya Penyimpanan', linestyle='--')
    plt.plot(Q_range, total_costs, label='Total Biaya', color='green')
    plt.axvline(EOQ, color='red', linestyle=':', label='EOQ')
    plt.xlabel('Jumlah Pemesanan (Q)')
    plt.ylabel('Biaya (Rp)')
    plt.title('Grafik Biaya EOQ - Rumus 2')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Panduan penggunaan aplikasi
with st.expander("📘 Panduan Lengkap Penggunaan Aplikasi EOQ"):
    st.markdown("""
    ### 🧭 Langkah Penggunaan

    Pilih salah satu metode perhitungan EOQ sesuai data yang Anda miliki:

    #### ➤ Rumus 1: EOQ = √(2RS / H)
    - Gunakan jika Anda mengetahui **biaya simpan langsung (H)** per unit per tahun.

    #### ➤ Rumus 2: EOQ = √(2RS / (P × I))
    - Gunakan jika Anda **tidak tahu H**, tetapi mengetahui **harga unit (P)** dan **persentase simpan tahunan (I)**.

    #### Parameter Umum:
    - **R**: Jumlah kebutuhan tahunan
    - **S**: Biaya pemesanan per pesanan
    - **H**: Biaya simpan per unit (untuk Rumus 1)
    - **P**: Harga beli per unit (untuk Rumus 2)
    - **I**: Persentase biaya simpan tahunan (untuk Rumus 2)

    #### Output:
    - EOQ (jumlah optimal pemesanan)
    - Total biaya persediaan tahunan
    - Grafik hubungan jumlah pemesanan dan total biaya

    👉 Gunakan grafik untuk melihat titik biaya minimum yang optimal.
    """)

st.caption("© 2025 | Aplikasi EOQ Dua Metode | Model Matematika dalam Industri")
