import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Aplikasi EOQ - Dua Versi Rumus")

st.markdown("Aplikasi ini menghitung EOQ dengan **dua versi rumus** untuk kebutuhan perbandingan dan analisis:")

with st.expander("📘 Rumus yang Digunakan"):
    st.latex(r'''EOQ_1 = \sqrt{\frac{2 \times R \times S}{H}}''')
    st.markdown("- **H** = Biaya simpan per unit per tahun (dimasukkan langsung)")
    st.latex(r'''EOQ_2 = \sqrt{\frac{2 \times R \times S}{P \times I}}''')
    st.markdown("- **P** = Harga beli per unit  \n- **I** = Biaya simpan dalam persen (%)")

# Input
st.header("📥 Input Parameter")

R = st.number_input("Jumlah kebutuhan tahunan (R) dalam unit", min_value=1.0, value=5000.0)
S = st.number_input("Biaya pemesanan per pesanan (S) dalam rupiah", min_value=0.0, value=200000.0)

# Versi 1 input
st.subheader("🔹 Rumus 1 (H langsung)")
H = st.number_input("Biaya simpan per unit per tahun (H) dalam rupiah", min_value=0.0, value=5000.0)

# Versi 2 input
st.subheader("🔹 Rumus 2 (berdasarkan P dan I)")
P = st.number_input("Harga beli per unit (P) dalam rupiah", min_value=0.0, value=50000.0)
I_percent = st.number_input("Persentase biaya simpan (I) dalam %", min_value=0.0, value=10.0)
I_decimal = I_percent / 100
H_2 = P * I_decimal

# Perhitungan EOQ
EOQ1 = np.sqrt((2 * R * S) / H)
EOQ2 = np.sqrt((2 * R * S) / H_2)

# Output hasil
st.header("📊 Hasil Perhitungan EOQ")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧮 EOQ Rumus 1")
    st.markdown(f"EOQ₁ = {EOQ1:.2f} unit")
    st.markdown(f"Total biaya persediaan = Rp {((R / EOQ1) * S + (EOQ1 / 2) * H):,.2f}")

with col2:
    st.markdown("### 🧮 EOQ Rumus 2")
    st.markdown(f"EOQ₂ = {EOQ2:.2f} unit")
    st.markdown(f"Total biaya persediaan = Rp {((R / EOQ2) * S + (EOQ2 / 2) * H_2):,.2f}")

# Grafik perbandingan
st.header("📈 Visualisasi Perbandingan")

Q_range = np.arange(100, int(max(EOQ1, EOQ2)*1.5), 10)
ordering_costs = (R / Q_range) * S
holding_costs_1 = (Q_range / 2) * H
holding_costs_2 = (Q_range / 2) * H_2
total_costs_1 = ordering_costs + holding_costs_1
total_costs_2 = ordering_costs + holding_costs_2

plt.figure(figsize=(10, 5))
plt.plot(Q_range, total_costs_1, label='Total Biaya (Rumus 1)', color='blue')
plt.plot(Q_range, total_costs_2, label='Total Biaya (Rumus 2)', color='green')
plt.axvline(EOQ1, color='blue', linestyle=':', label='EOQ₁')
plt.axvline(EOQ2, color='green', linestyle=':', label='EOQ₂')
plt.xlabel('Jumlah Pemesanan')
plt.ylabel('Total Biaya (Rp)')
plt.title('Perbandingan EOQ - Dua Versi Rumus')
plt.legend()
plt.grid(True)
st.pyplot(plt)

# Panduan
with st.expander("📌 Panduan Penggunaan"):
    st.markdown("""
    - Masukkan data kebutuhan tahunan, biaya pesan, dan parameter simpan sesuai dua rumus.
    - EOQ dihitung untuk dua skenario:
        - Langsung menggunakan H (biaya simpan/unit)
        - Menggunakan persentase simpan dari harga unit (P × I)
    - Grafik menunjukkan total biaya persediaan terhadap jumlah pemesanan.
    """)
with st.expander("📘 Panduan Lengkap Penggunaan Aplikasi EOQ"):
    st.markdown("""
    ### 🧭 Langkah Penggunaan

    Aplikasi ini menghitung jumlah pemesanan optimal (**EOQ**) dengan dua metode berbeda.

    #### 1. Masukkan Data Kebutuhan & Biaya

    | Parameter | Keterangan |
    |----------|------------|
    | **R (Demand)** | Jumlah permintaan tahunan (unit barang per tahun). Contoh: `5000` |
    | **S (Ordering Cost)** | Biaya pemesanan setiap kali memesan. Contoh: `200000` rupiah |
    | **H (Holding Cost - versi 1)** | Biaya penyimpanan per unit per tahun (langsung). Contoh: `5000` rupiah |
    | **P (Harga per Unit)** | Harga beli per unit barang. Digunakan dalam Rumus 2. Contoh: `50000` rupiah |
    | **I (%)** | Persentase biaya penyimpanan dari harga unit per tahun. Contoh: `10` % |

    ---

    #### 2. Pemilihan Rumus

    Aplikasi menghitung EOQ dengan dua pendekatan:
    - **EOQ₁**: Rumus klasik menggunakan `H`
    - **EOQ₂**: Rumus alternatif menggunakan `P × I`

    ---

    #### 3. Interpretasi Hasil

    Aplikasi akan menampilkan:
    - EOQ dari masing-masing rumus
    - Estimasi total biaya persediaan
    - Grafik perbandingan biaya vs kuantitas pemesanan

    ---

    #### 4. Grafik Visualisasi

    - **Sumbu X** = Jumlah unit yang dipesan
    - **Sumbu Y** = Total biaya persediaan
    - Garis biru: Total biaya dari Rumus 1
    - Garis hijau: Total biaya dari Rumus 2
    - Garis vertikal: EOQ optimal dari masing-masing metode

    ---

    #### 5. Contoh Perhitungan

    Misal:
    - R = 5000
    - S = 200000
    - H = 5000
    - P = 50000
    - I = 10%

    Maka:
    - EOQ₁ dan EOQ₂ ≈ 632 unit
    - Total biaya akan terlihat di hasil aplikasi

    ---

    #### ✅ Tips
    - Gunakan Rumus 1 jika tahu H langsung
    - Gunakan Rumus 2 jika hanya punya harga dan persentase simpan
    - Cek grafik untuk visualisasi titik biaya minimum
    """)

# Footer
st.caption("© 2025 | EOQ Dua Rumus - Model Matematika Industri")
