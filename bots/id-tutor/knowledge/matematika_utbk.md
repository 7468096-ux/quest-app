# Matematika UTBK/SNBT — Materi Lengkap

## 1. Aljabar

### Persamaan Kuadrat
- Bentuk umum: ax² + bx + c = 0
- Rumus ABC: x = (-b ± √(b²-4ac)) / 2a
- Diskriminan D = b² - 4ac
  - D > 0: dua akar real berbeda
  - D = 0: dua akar real sama
  - D < 0: tidak ada akar real
- Hubungan akar: x₁+x₂ = -b/a dan x₁·x₂ = c/a

### Fungsi dan Grafik
- **Fungsi linear:** f(x) = ax + b (garis lurus)
- **Fungsi kuadrat:** f(x) = ax² + bx + c (parabola)
  - Titik puncak: x = -b/2a; y = -D/4a
  - Parabola terbuka ke atas (a>0) atau ke bawah (a<0)
- **Fungsi komposisi:** (f∘g)(x) = f(g(x))
- **Fungsi invers:** f⁻¹(x): tukar x dan y, lalu selesaikan

### Pertidaksamaan
- Kalikan/bagi dengan bilangan negatif → tanda tidak sama berbalik
- Pertidaksamaan kuadrat: tentukan akar → test interval

---

## 2. Trigonometri

### Nilai Sudut Istimewa
| Sudut | sin | cos | tan |
|-------|-----|-----|-----|
| 0° | 0 | 1 | 0 |
| 30° | ½ | ½√3 | ⅓√3 |
| 45° | ½√2 | ½√2 | 1 |
| 60° | ½√3 | ½ | √3 |
| 90° | 1 | 0 | - |

### Identitas Trigonometri
- sin²x + cos²x = 1
- tan x = sin x / cos x
- sin(A±B) = sin A cos B ± cos A sin B
- cos(A±B) = cos A cos B ∓ sin A sin B
- sin 2A = 2 sin A cos A
- cos 2A = cos²A - sin²A = 1 - 2sin²A = 2cos²A - 1

### Aturan Sinus dan Cosinus
- **Aturan sinus:** a/sin A = b/sin B = c/sin C
- **Aturan cosinus:** a² = b² + c² - 2bc cos A

---

## 3. Limit dan Kalkulus

### Limit Fungsi
- lim(x→a) k = k (konstanta)
- lim(x→a) x = a
- Limit tak tentu 0/0 → faktorisasi atau L'Hôpital
- lim(x→∞) (axⁿ + ...)/(bxⁿ + ...) = a/b (pangkat sama)

### Turunan (Diferensial)
- (xⁿ)' = n·xⁿ⁻¹
- (sin x)' = cos x; (cos x)' = -sin x; (tan x)' = sec²x
- (eˣ)' = eˣ; (ln x)' = 1/x
- **Aturan rantai:** (f∘g)'(x) = f'(g(x))·g'(x)
- **Aturan perkalian:** (f·g)' = f'g + fg'
- **Aturan pembagian:** (f/g)' = (f'g - fg')/g²

### Integral
- ∫xⁿ dx = xⁿ⁺¹/(n+1) + C (n ≠ -1)
- ∫sin x dx = -cos x + C
- ∫cos x dx = sin x + C
- ∫eˣ dx = eˣ + C
- ∫1/x dx = ln|x| + C
- **Integral tentu:** ∫ₐᵇ f(x) dx = F(b) - F(a)
- **Luas daerah:** L = ∫ₐᵇ |f(x) - g(x)| dx

---

## 4. Statistika dan Peluang

### Statistika Dasar
- **Mean (rata-rata):** x̄ = Σxᵢ/n
- **Median:** nilai tengah (data terurut)
- **Modus:** nilai yang paling sering muncul
- **Ragam (varians):** s² = Σ(xᵢ - x̄)²/n
- **Simpangan baku:** s = √varians

### Peluang
- P(A) = n(A)/n(S) (0 ≤ P(A) ≤ 1)
- P(A∪B) = P(A) + P(B) - P(A∩B)
- P(Aᶜ) = 1 - P(A)
- **Kejadian bebas:** P(A∩B) = P(A)·P(B)
- **Permutasi:** ₙPᵣ = n!/(n-r)!
- **Kombinasi:** ₙCᵣ = n!/[r!(n-r)!]

---

## 5. Geometri

### Bangun Datar
- Luas lingkaran: L = πr²; Keliling: K = 2πr
- Luas segitiga: L = ½alas×tinggi = ½ab sin C
- Luas trapesium: L = ½(a+b)×t

### Vektor
- Panjang vektor: |a| = √(x²+y²+z²)
- Dot product: a·b = |a||b|cos θ = x₁x₂+y₁y₂+z₁z₂
- Cross product: |a×b| = |a||b|sin θ

### Transformasi Geometri
- **Translasi:** (x,y) → (x+a, y+b)
- **Refleksi terhadap sumbu x:** (x,y) → (x,-y)
- **Refleksi terhadap sumbu y:** (x,y) → (-x,y)
- **Rotasi 90° berlawanan jarum jam:** (x,y) → (-y,x)
- **Dilatasi dengan faktor k:** (x,y) → (kx,ky)

---

## 6. Barisan dan Deret

### Aritmetika
- Suku ke-n: aₙ = a₁ + (n-1)d
- Jumlah n suku: Sₙ = n/2 × (2a₁ + (n-1)d) = n/2 × (a₁ + aₙ)

### Geometri
- Suku ke-n: aₙ = a₁ × rⁿ⁻¹
- Jumlah n suku: Sₙ = a₁(rⁿ-1)/(r-1) untuk r ≠ 1
- Deret tak hingga (|r|<1): S∞ = a₁/(1-r)

---

## Tips Soal UTBK Matematika
1. Baca soal dua kali sebelum menjawab
2. Untuk soal grafik: identifikasi kunci (titik potong, titik puncak)
3. Untuk soal cerita: buat persamaan matematikanya dulu
4. Jika bingung: eliminasi pilihan jawaban yang jelas salah
5. Cek satuan dan skala pada soal
