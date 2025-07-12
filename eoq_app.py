import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from PIL import Image
import io

st.title('Aplikasi Perhitungan EOQ (Economic Order Quantity)')
st.write("""
Aplikasi ini membantu menentukan jumlah pemesanan optimal dengan dua metode:
1. **Metode Klasik**: Menggunakan biaya penyimpanan tetap per unit
2. **Metode Persentase**: Menggunakan persentase dari nilai barang sebagai biaya penyimpanan
""")

# Tampilkan kedua rumus
st.header("Rumus EOQ")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Metode Klasik")
    st.latex(r'''
    EOQ = \sqrt{\frac{2DS}{H}}
    ''')
    st.write("""
    Dimana:
    - D = Permintaan tahunan (unit)
    - S = Biaya pemesanan per pesanan
    - H = Biaya penyimpanan per unit per tahun
    """)

with col2:
    st.subheader("Metode Persentase")
    st.latex(r'''
    EOQ = \sqrt{\frac{2DS}{iC}}
    ''')
    st.write("""
    Dimana:
    - D = Permintaan tahunan (unit)
    - S = Biaya pemesanan per pesanan
    - i = Persentase biaya penyimpanan (%)
    - C = Harga per unit barang
    """)

# Tab untuk memilih metode
tab1, tab2 = st.tabs(["Metode Klasik", "Metode Persentase"])

with tab1:
    st.header("Metode Klasik")
    st.write("""
    **Panduan Penggunaan:**
    1. Masukkan permintaan tahunan (jumlah unit yang dibutuhkan dalam setahun)
    2. Masukkan biaya pemesanan per pesanan (dalam mata uang)
    3. Masukkan biaya penyimpanan per unit per tahun (dalam mata uang)
    4. Aplikasi akan menghitung:
       - EOQ (jumlah optimal pemesanan)
       - Total biaya persediaan
       - Frekuensi pemesanan optimal per tahun
    """)
    
    st.subheader("Parameter Input")
    D = st.number_input("Permintaan tahunan (unit)", min_value=1, value=1000, key="D1")
    S = st.number_input("Biaya pemesanan per pesanan", min_value=0.01, value=50.0, key="S1")
    H = st.number_input("Biaya penyimpanan per unit per tahun", min_value=0.01, value=2.0, key="H1")
    
    if st.button("Hitung EOQ (Metode Klasik)"):
        # Hitung EOQ
        eoq = math.sqrt((2 * D * S) / H)
        total_cost = (D / eoq) * S + (eoq / 2) * H
        order_frequency = D / eoq
        
        st.subheader("Hasil Perhitungan")
        st.write(f"EOQ (Jumlah Pemesanan Optimal): {eoq:.2f} unit")
        st.write(f"Total Biaya Persediaan Tahunan: {total_cost:.2f}")
        st.write(f"Jumlah Pemesanan per Tahun: {order_frequency:.2f} kali")
        
        # Visualisasi
        st.subheader("Visualisasi Biaya Persediaan")
        
        q_values = np.linspace(1, 2*eoq, 100)
        ordering_costs = (D / q_values) * S
        holding_costs = (q_values / 2) * H
        total_costs = ordering_costs + holding_costs
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(q_values, ordering_costs, label='Biaya Pemesanan')
        ax.plot(q_values, holding_costs, label='Biaya Penyimpanan')
        ax.plot(q_values, total_costs, label='Total Biaya')
        ax.axvline(eoq, color='r', linestyle='--', label='EOQ')
        ax.set_xlabel('Jumlah Pemesanan (Q)')
        ax.set_ylabel('Biaya')
        ax.set_title('Hubungan Biaya dan Jumlah Pemesanan')
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)

with tab2:
    st.header("Metode Persentase")
    st.write("""
    **Panduan Penggunaan:**
    1. Masukkan permintaan tahunan (jumlah unit yang dibutuhkan dalam setahun)
    2. Masukkan biaya pemesanan per pesanan (dalam mata uang)
    3. Masukkan harga per unit barang (dalam mata uang)
    4. Masukkan persentase biaya penyimpanan (% dari nilai barang)
    5. Aplikasi akan menghitung:
       - EOQ (jumlah optimal pemesanan)
       - Total biaya persediaan
       - Frekuensi pemesanan optimal per tahun
    """)
    
    st.subheader("Parameter Input")
    D = st.number_input("Permintaan tahunan (unit)", min_value=1, value=1000, key="D2")
    S = st.number_input("Biaya pemesanan per pesanan", min_value=0.01, value=50.0, key="S2")
    C = st.number_input("Harga per unit barang", min_value=0.01, value=10.0)
    i = st.number_input("Persentase biaya penyimpanan (%)", min_value=0.01, value=20.0)
    
    if st.button("Hitung EOQ (Metode Persentase)"):
        # Konversi persentase ke desimal
        i_decimal = i / 100
        H = i_decimal * C  # Hitung biaya penyimpanan per unit
        
        # Hitung EOQ
        eoq = math.sqrt((2 * D * S) / (i_decimal * C))
        total_cost = (D / eoq) * S + (eoq / 2) * H
        order_frequency = D / eoq
        
        st.subheader("Hasil Perhitungan")
        st.write(f"EOQ (Jumlah Pemesanan Optimal): {eoq:.2f} unit")
        st.write(f"Total Biaya Persediaan Tahunan: {total_cost:.2f}")
        st.write(f"Jumlah Pemesanan per Tahun: {order_frequency:.2f} kali")
        st.write(f"Biaya Penyimpanan per Unit: {H:.2f} (dihitung dari {i}% dari harga unit {C})")
        
        # Visualisasi
        st.subheader("Visualisasi Biaya Persediaan")
        
        q_values = np.linspace(1, 2*eoq, 100)
        ordering_costs = (D / q_values) * S
        holding_costs = (q_values / 2) * H
        total_costs = ordering_costs + holding_costs
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(q_values, ordering_costs, label='Biaya Pemesanan')
        ax.plot(q_values, holding_costs, label='Biaya Penyimpanan')
        ax.plot(q_values, total_costs, label='Total Biaya')
        ax.axvline(eoq, color='r', linestyle='--', label='EOQ')
        ax.set_xlabel('Jumlah Pemesanan (Q)')
        ax.set_ylabel('Biaya')
        ax.set_title('Hubungan Biaya dan Jumlah Pemesanan')
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)

# Tambahan informasi
st.markdown("---")
st.subheader("Penjelasan Metode")
with st.expander("Tentang Metode Klasik"):
    st.write("""
    **Metode Klasik EOQ** mengasumsikan biaya penyimpanan per unit adalah nilai tetap yang diketahui. 
    Rumus ini cocok digunakan ketika:
    - Biaya penyimpanan per unit sudah pasti
    - Tidak ada variasi harga barang
    - Tidak ada diskon kuantitas
    """)

with st.expander("Tentang Metode Persentase"):
    st.write("""
    **Metode Persentase EOQ** mengasumsikan biaya penyimpanan adalah persentase dari nilai barang. 
    Rumus ini lebih realistis ketika:
    - Biaya penyimpanan tergantung pada nilai barang (misal biaya modal, asuransi)
    - Harga barang bervariasi
    - Ada pertimbangan opportunity cost dari modal yang tertanam di persediaan
    """)