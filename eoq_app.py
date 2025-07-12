import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import FuncFormatter, StrMethodFormatter

# Fungsi format miliar
def format_miliar(x, pos):
    return 'Rp %.1fM' % (x / 1_000_000)

# Konfigurasi tema Streamlit
st.set_page_config(
    page_title="Aplikasi EOQ Interaktif",
    page_icon="💡",
    layout="wide"
)

# CSS untuk mempercantik tampilan
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stNumberInput, .stTextInput, .stSelectbox {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stTab {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .result-box {
        background-color: #e8f5e9;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header dengan gambar
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://images.icon-icons.com/4309/PNG/512/seminar_lecture_speech_talk_slides_presentation_icon_267246.png", width=100)
with col2:
    st.title("Aplikasi Perhitungan EOQ")
    st.markdown("**Economic Order Quantity - Optimalkan Persediaan Anda**")

# Tampilkan kedua rumus
st.header("📝 Rumus EOQ", divider="green")
col1, col2 = st.columns(2)

with col1:
    with st.expander("**Metode Klasik**", expanded=True):
        st.latex(r'''
        EOQ = \sqrt{\frac{2DS}{H}}
        ''')
        st.write("""
        **Keterangan:**
        - D = Permintaan tahunan (unit)
        - S = Biaya pemesanan per pesanan (Rp)
        - H = Biaya penyimpanan per unit per tahun (Rp)
        """)

with col2:
    with st.expander("**Metode Persentase**", expanded=True):
        st.latex(r'''
        EOQ = \sqrt{\frac{2DS}{iC}}
        ''')
        st.write("""
        **Keterangan:**
        - D = Permintaan tahunan (unit)
        - S = Biaya pemesanan per pesanan (Rp)
        - i = Persentase biaya penyimpanan (%)
        - C = Harga per unit barang (Rp)
        """)

# Tab untuk memilih metode
tab1, tab2 = st.tabs(["📈 Metode Klasik", "📊 Metode Persentase"])

with tab1:
    st.header("Perhitungan EOQ Metode Klasik", divider="green")
    
    with st.container(border=True):
        st.subheader("📋 Panduan Penggunaan")
        st.write("""
        1. Masukkan **permintaan tahunan** (jumlah unit yang dibutuhkan dalam setahun)
        2. Masukkan **biaya pemesanan** per pesanan (dalam Rp)
        3. Masukkan **biaya penyimpanan** per unit per tahun (dalam Rp)
        4. Klik tombol **Hitung EOQ** untuk melihat hasil
        """)
    
    with st.container(border=True):
        st.subheader("🔢 Parameter Input")
        col1, col2, col3 = st.columns(3)
        with col1:
            D = st.number_input("Permintaan tahunan (unit)", min_value=1, value=5000, key="D1")
        with col2:
            S = st.number_input("Biaya pemesanan per pesanan (Rp)", min_value=1, value=75000, key="S1")
        with col3:
            H = st.number_input("Biaya penyimpanan per unit per tahun (Rp)", min_value=1, value=3000, key="H1")
    
    if st.button("Hitung EOQ (Metode Klasik)", type="primary"):
        # Hitung EOQ
        eoq = math.sqrt((2 * D * S) / H)
        total_cost = (D / eoq) * S + (eoq / 2) * H
        order_frequency = D / eoq
        
        with st.container(border=True):
            st.subheader("📊 Hasil Perhitungan")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("EOQ (Jumlah Optimal)", f"{eoq:,.0f} unit".replace(",", "."))
            with col2:
                st.metric("Total Biaya Tahunan", f"Rp {total_cost:,.0f}".replace(",", "."))
            with col3:
                st.metric("Frekuensi Pemesanan", f"{order_frequency:.1f} kali/tahun")
        
        # Visualisasi
        st.subheader("📈 Visualisasi Biaya Persediaan", divider="green")
        
        q_values = np.linspace(1, 2*eoq, 100)
        ordering_costs = (D / q_values) * S
        holding_costs = (q_values / 2) * H
        total_costs = ordering_costs + holding_costs
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(q_values, ordering_costs, label='Biaya Pemesanan', color='#FF6B6B', linewidth=2)
        ax.plot(q_values, holding_costs, label='Biaya Penyimpanan', color='#4ECDC4', linewidth=2)
        ax.plot(q_values, total_costs, label='Total Biaya', color='#45B7D1', linewidth=3)
        ax.axvline(eoq, color='#FFA500', linestyle='--', label='EOQ (Titik Optimal)')
        
        # Formatting dengan skala miliar
        plt.ylim(0, 1_000_000_000)  # Maksimal 1 miliar
        plt.yticks(np.arange(0, 1_100_000_000, 100_000_000))  # Interval 100 juta
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", ".")))
        
        ax.set_xlabel('Jumlah Pemesanan (Q)', fontsize=12)
        ax.set_ylabel('Biaya', fontsize=12)
        ax.set_title('Hubungan Antara Jumlah Pemesanan dan Biaya (Skala Miliar Rp)', fontsize=14, pad=20)
        ax.legend(fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Annotate EOQ point
        ax.annotate(f'EOQ = {eoq:,.0f} unit'.replace(",", "."), 
                    xy=(eoq, total_cost), xytext=(eoq*1.1, total_cost*1.1),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
        
        st.pyplot(fig)
        
        with st.expander("📝 Penjelasan Grafik", expanded=True):
            st.write("""
            **Interpretasi Grafik EOQ:**
            
            1. **Biaya Pemesanan (Merah)**:
               - Menurun saat jumlah pesanan meningkat (karena pesanan lebih sedikit)
            
            2. **Biaya Penyimpanan (Hijau)**:
               - Meningkat linear dengan jumlah pesanan (semakin banyak disimpan, biaya semakin besar)
            
            3. **Total Biaya (Biru)**:
               - Kurva berbentuk U yang menunjukkan trade-off antara biaya pemesanan dan penyimpanan
               - Titik terendah adalah EOQ (jumlah pesanan optimal)
            
            4. **Garis Oranye**:
               - Menunjukkan posisi EOQ pada grafik
               - Di titik ini, total biaya persediaan adalah yang paling minimum
            """)

with tab2:
    st.header("Perhitungan EOQ Metode Persentase", divider="green")
    
    with st.container(border=True):
        st.subheader("📋 Panduan Penggunaan")
        st.write("""
        1. Masukkan **permintaan tahunan** (jumlah unit yang dibutuhkan dalam setahun)
        2. Masukkan **biaya pemesanan** per pesanan (dalam Rp)
        3. Masukkan **harga per unit** barang (dalam Rp)
        4. Masukkan **persentase biaya penyimpanan** (% dari nilai barang)
        5. Klik tombol **Hitung EOQ** untuk melihat hasil
        """)
    
    with st.container(border=True):
        st.subheader("🔢 Parameter Input")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            D = st.number_input("Permintaan tahunan (unit)", min_value=1, value=10000, key="D2")
        with col2:
            S = st.number_input("Biaya pemesanan per pesanan (Rp)", min_value=1, value=100000, key="S2")
        with col3:
            C = st.number_input("Harga per unit barang (Rp)", min_value=1, value=25000, key="C")
        with col4:
            i = st.number_input("Persentase biaya penyimpanan (%)", min_value=0.1, value=15.0, key="i")
    
    if st.button("Hitung EOQ (Metode Persentase)", type="primary"):
        # Konversi persentase ke desimal
        i_decimal = i / 100
        H = i_decimal * C  # Hitung biaya penyimpanan per unit
        
        # Hitung EOQ
        eoq = math.sqrt((2 * D * S) / (i_decimal * C))
        total_cost = (D / eoq) * S + (eoq / 2) * H
        order_frequency = D / eoq
        
        with st.container(border=True):
            st.subheader("📊 Hasil Perhitungan")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("EOQ (Jumlah Optimal)", f"{eoq:,.0f} unit".replace(",", "."))
            with col2:
                st.metric("Total Biaya Tahunan", f"Rp {total_cost:,.0f}".replace(",", "."))
            with col3:
                st.metric("Frekuensi Pemesanan", f"{order_frequency:.1f} kali/tahun")
            
            st.write(f"**Biaya Penyimpanan per Unit:** Rp {H:,.0f}".replace(",", ".") + 
                    f" ({i}% dari harga unit Rp {C:,.0f})".replace(",", "."))
        
        # Visualisasi
        st.subheader("📈 Visualisasi Biaya Persediaan", divider="green")
        
        q_values = np.linspace(1, 2*eoq, 100)
        ordering_costs = (D / q_values) * S
        holding_costs = (q_values / 2) * H
        total_costs = ordering_costs + holding_costs
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(q_values, ordering_costs, label='Biaya Pemesanan', color='#FF6B6B', linewidth=2)
        ax.plot(q_values, holding_costs, label='Biaya Penyimpanan', color='#4ECDC4', linewidth=2)
        ax.plot(q_values, total_costs, label='Total Biaya', color='#45B7D1', linewidth=3)
        ax.axvline(eoq, color='#FFA500', linestyle='--', label='EOQ (Titik Optimal)')
        
        # Formatting dengan skala miliar
        plt.ylim(0, 1_500_000_000)  # Maksimal 1.5 miliar
        plt.yticks(np.arange(0, 1_600_000_000, 200_000_000))  # Interval 200 juta
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", ".")))
        
        ax.set_xlabel('Jumlah Pemesanan (Q)', fontsize=12)
        ax.set_ylabel('Biaya', fontsize=12)
        ax.set_title('Hubungan Antara Jumlah Pemesanan dan Biaya (Skala Miliar Rp)', fontsize=14, pad=20)
        ax.legend(fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Annotate EOQ point
        ax.annotate(f'EOQ = {eoq:,.0f} unit'.replace(",", "."), 
                    xy=(eoq, total_cost), xytext=(eoq*1.1, total_cost*1.1),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
        
        st.pyplot(fig)
        
        with st.expander("📝 Penjelasan Grafik", expanded=True):
            st.write("""
            **Interpretasi Grafik EOQ (Metode Persentase):**
            
            1. **Biaya Pemesanan (Merah)**:
               - Berbanding terbalik dengan jumlah pesanan (fixed cost per order)
            
            2. **Biaya Penyimpanan (Hijau)**:
               - Proporsional dengan nilai barang (persentase dari harga unit)
               - Semakin banyak barang disimpan, biaya modal semakin besar
            
            3. **Total Biaya (Biru)**:
               - Mencapai titik minimum pada EOQ
               - Menunjukkan keseimbangan optimal antara biaya pemesanan dan penyimpanan
            
            4. **Garis Oranye**:
               - Titik optimal (EOQ) dimana total biaya minimum
               - Pemesanan di bawah atau di atas titik ini akan meningkatkan total biaya
            """)
            st.info("💡 **Tip Manajemen Persediaan:** EOQ membantu mengurangi biaya total tetapi pertimbangkan juga faktor lain seperti diskon kuantitas atau fluktuasi permintaan.")

# Footer
st.markdown("---")
st.markdown("📌 **Tips Penggunaan:** Gunakan contoh soal yang tersedia untuk memvalidasi perhitungan Anda")
st.caption("© 2025 Aplikasi EOQ - Optimalkan Manajemen Persediaan Anda")
st.caption("Matematika Terapan | Dikembangkan oleh: Samuel")