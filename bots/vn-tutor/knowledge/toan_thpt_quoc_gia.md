# Toán học THPT Quốc gia — Kiến thức & Dạng bài

## Cấu trúc đề thi Toán THPT 2024-2025
- 50 câu trắc nghiệm, thời gian 90 phút
- Cấp độ: 60% nhận biết-thông hiểu, 40% vận dụng-vận dụng cao
- Điểm: 10 điểm (0.2 điểm/câu)

---

## CHƯƠNG 1: HÀM SỐ VÀ ĐỒ THỊ

### 1.1 Tính đơn điệu — Cực trị
**Hàm số bậc 3:** y = ax³ + bx² + cx + d (a ≠ 0)
- y' = 3ax² + 2bx + c
- Hàm đồng biến: y' > 0; nghịch biến: y' < 0
- Cực đại/cực tiểu: y' = 0 và y' đổi dấu

**Hàm số bậc 4 trùng phương:** y = ax⁴ + bx² + c (a ≠ 0)
- Đặt t = x², hàm trở thành y = at² + bt + c
- Khảo sát dạng bậc 2 theo t (t ≥ 0)

**Bảng biến thiên:** Kẻ bảng với x, y', y để thể hiện chiều biến thiên và cực trị.

### 1.2 Tiệm cận
**Hàm phân thức:** y = (ax + b)/(cx + d)
- Tiệm cận đứng: x = -d/c (mẫu = 0)
- Tiệm cận ngang: y = a/c (khi x → ±∞)
- Tiệm cận xiên: nếu bậc tử cao hơn mẫu 1 bậc → chia đa thức

### 1.3 Số cực trị — Bài toán điều kiện tham số
- Hàm bậc 3 có 2 điểm cực trị ⟺ y' = 0 có 2 nghiệm phân biệt ⟺ Δ' > 0
- Bài toán: "Tìm m để hàm số có cực đại, cực tiểu" → giải phương trình y' = 0

**Ví dụ:** y = x³ - 3x² + m có cực đại và cực tiểu khi:
y' = 3x² - 6x = 3x(x-2) = 0 → x = 0 và x = 2 (luôn có, không phụ thuộc m)
→ Hàm luôn có cực đại x=0, cực tiểu x=2 với mọi m.

---

## CHƯƠNG 2: MŨ VÀ LOGARIT

### 2.1 Lũy thừa
- aᵐ · aⁿ = aᵐ⁺ⁿ ; aᵐ/aⁿ = aᵐ⁻ⁿ ; (aᵐ)ⁿ = aᵐⁿ
- a⁰ = 1 ; a⁻ⁿ = 1/aⁿ ; a^(p/q) = ᵍ√(aᵖ)

### 2.2 Hàm số mũ và logarit
- Hàm mũ: y = aˣ (a > 0, a ≠ 1)
  + a > 1: đồng biến trên ℝ
  + 0 < a < 1: nghịch biến trên ℝ
- Hàm logarit: y = logₐx (a > 0, a ≠ 1, x > 0)
  + logₐ(MN) = logₐM + logₐN
  + logₐ(M/N) = logₐM - logₐN
  + logₐMⁿ = n·logₐM
  + Đổi cơ số: logₐM = logᵦM / logᵦa

### 2.3 Phương trình mũ và logarit
**Phương trình mũ cơ bản:** aˣ = b → x = logₐb
**Phương trình logarit:** logₐx = b → x = aᵇ

**Phương trình mũ phức tạp:** Đặt t = aˣ → phương trình bậc 2 theo t
Ví dụ: 4ˣ - 5·2ˣ + 4 = 0 → đặt t = 2ˣ (t > 0): t² - 5t + 4 = 0 → t=1 hoặc t=4
→ 2ˣ = 1 → x=0; 2ˣ = 4 → x=2

**Bất phương trình mũ:**
- a > 1: aˣ > aʸ ⟺ x > y (giữ chiều)
- 0 < a < 1: aˣ > aʸ ⟺ x < y (đổi chiều)

---

## CHƯƠNG 3: NGUYÊN HÀM — TÍCH PHÂN

### 3.1 Nguyên hàm cơ bản
| Hàm | Nguyên hàm |
|-----|-----------|
| xⁿ (n≠-1) | xⁿ⁺¹/(n+1) + C |
| 1/x | ln|x| + C |
| eˣ | eˣ + C |
| aˣ | aˣ/lna + C |
| sinx | -cosx + C |
| cosx | sinx + C |
| 1/cos²x | tanx + C |
| 1/sin²x | -cotx + C |

### 3.2 Phương pháp tính nguyên hàm
**Phương pháp đổi biến:**
∫f(u(x))·u'(x)dx = F(u) + C (đặt t = u(x))

Ví dụ: ∫2x·(x²+1)⁵dx → đặt t = x²+1, dt = 2xdx
= ∫t⁵dt = t⁶/6 + C = (x²+1)⁶/6 + C

**Phương pháp từng phần:**
∫u·dv = u·v - ∫v·du

Quy tắc chọn u (LIATE): Logarit → Ngược giác → Đại số → Lượng giác → Mũ

### 3.3 Tích phân xác định
∫ₐᵇf(x)dx = F(b) - F(a) (F là một nguyên hàm của f)

**Tính diện tích:**
- Diện tích hình phẳng giới hạn bởi y=f(x), Ox, x=a, x=b:
  S = ∫ₐᵇ|f(x)|dx

- Giữa 2 đường cong f(x) và g(x):
  S = ∫ₐᵇ|f(x) - g(x)|dx

**Tính thể tích khối tròn xoay:**
- Quay quanh Ox: V = π·∫ₐᵇ[f(x)]²dx

---

## CHƯƠNG 4: SỐ PHỨC

### 4.1 Định nghĩa
- Số phức: z = a + bi (a, b ∈ ℝ; i² = -1)
- Phần thực: Re(z) = a ; Phần ảo: Im(z) = b
- Số phức liên hợp: z̄ = a - bi
- Mô-đun: |z| = √(a² + b²)

### 4.2 Phép tính
- Cộng/trừ: (a+bi) ± (c+di) = (a±c) + (b±d)i
- Nhân: (a+bi)(c+di) = (ac-bd) + (ad+bc)i
- Chia: (a+bi)/(c+di) = (a+bi)(c-di)/|c+di|²
- z·z̄ = a² + b² = |z|²

### 4.3 Căn bậc hai số phức
√(a+bi) = x+yi → x²-y² = a và 2xy = b

**Phương trình bậc 2 số phức:**
az² + bz + c = 0 → Δ = b² - 4ac
- Δ ≥ 0: 2 nghiệm thực
- Δ < 0: 2 nghiệm phức liên hợp z₁,₂ = (-b ± i√|Δ|)/(2a)

---

## CHƯƠNG 5: TỔ HỢP — XÁC SUẤT

### 5.1 Quy tắc đếm
- Quy tắc nhân: n₁ × n₂ × ... × nₖ cách
- Quy tắc cộng: n₁ + n₂ + ... + nₖ cách

### 5.2 Hoán vị — Chỉnh hợp — Tổ hợp
- Hoán vị n phần tử: Pₙ = n!
- Chỉnh hợp chập k của n: Aₙᵏ = n!/(n-k)!
- Tổ hợp chập k của n: Cₙᵏ = n!/[k!(n-k)!]
- Tính chất: Cₙᵏ = Cₙⁿ⁻ᵏ ; Cₙᵏ + Cₙᵏ⁺¹ = Cₙ₊₁ᵏ⁺¹

### 5.3 Nhị thức Newton
(a+b)ⁿ = Σₖ₌₀ⁿ Cₙᵏ·aⁿ⁻ᵏ·bᵏ
Số hạng tổng quát: Tₖ₊₁ = Cₙᵏ·aⁿ⁻ᵏ·bᵏ

### 5.4 Xác suất
- P(A) = số kết quả thuận lợi / tổng số kết quả
- 0 ≤ P(A) ≤ 1 ; P(Ā) = 1 - P(A)
- P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
- A, B độc lập: P(A ∩ B) = P(A)·P(B)
- Xác suất có điều kiện: P(A|B) = P(A∩B)/P(B)
- Công thức Bayes: P(Aᵢ|B) = P(Aᵢ)·P(B|Aᵢ) / ΣP(Aⱼ)·P(B|Aⱼ)

---

## CHƯƠNG 6: HÌNH HỌC KHÔNG GIAN

### 6.1 Khối đa diện — Hình thể tích
| Hình | Thể tích | Diện tích |
|------|----------|-----------|
| Hình hộp chữ nhật | V = a·b·c | S = 2(ab+bc+ca) |
| Khối lập phương | V = a³ | S = 6a² |
| Lăng trụ đứng | V = S_đáy × h | |
| Hình chóp | V = (1/3)·S_đáy × h | |
| Hình nón | V = (1/3)πr²h | S_xq = πrl ; S = πr(r+l) |
| Hình cầu | V = (4/3)πR³ | S = 4πR² |
| Hình trụ | V = πr²h | S_xq = 2πrh |

### 6.2 Khối chóp — Bài toán thực tế
**Chóp tứ giác đều S-ABCD (đáy vuông cạnh a, chiều cao h):**
- SO ⊥ ABCD, O là tâm đáy → SO = h
- SA = √(SO² + OA²) = √(h² + a²/2) (apothem lateral face)
- Thể tích V = (1/3)·a²·h

---

## CHƯƠNG 7: GIẢI TÍCH — HÀM SỐ LƯỢNG GIÁC

### 7.1 Công thức lượng giác cơ bản
- sin²x + cos²x = 1
- tan²x + 1 = 1/cos²x
- sin2x = 2sinx·cosx ; cos2x = cos²x - sin²x = 1 - 2sin²x = 2cos²x - 1
- sin(A±B) = sinA·cosB ± cosA·sinB
- cos(A±B) = cosA·cosB ∓ sinA·sinB

### 7.2 Phương trình lượng giác cơ bản
- sinx = a → x = arcsin(a) + 2kπ hoặc x = π - arcsin(a) + 2kπ
- cosx = a → x = ±arccos(a) + 2kπ
- tanx = a → x = arctan(a) + kπ
- cotx = a → x = arccot(a) + kπ

**Phương trình dạng đặc biệt:**
- sin²x = sin²α → x = ±α + kπ
- cos²x = cos²α → x = ±α + kπ

---

## CHƯƠNG 8: HÌNH HỌC GIẢI TÍCH Oxyz

### 8.1 Vector trong không gian
- a⃗ = (a₁; a₂; a₃) ; b⃗ = (b₁; b₂; b₃)
- a⃗ + b⃗ = (a₁+b₁; a₂+b₂; a₃+b₃)
- a⃗·b⃗ = a₁b₁ + a₂b₂ + a₃b₃ (tích vô hướng)
- cosθ = (a⃗·b⃗)/(|a⃗|·|b⃗|)
- a⃗×b⃗ = (a₂b₃-a₃b₂; a₃b₁-a₁b₃; a₁b₂-a₂b₁) (tích có hướng)

### 8.2 Phương trình đường thẳng
- Phương trình tham số: x = x₀ + at; y = y₀ + bt; z = z₀ + ct
- Phương trình chính tắc: (x-x₀)/a = (y-y₀)/b = (z-z₀)/c
- Đường thẳng qua 2 điểm A(x₁,y₁,z₁) và B(x₂,y₂,z₂): VTCP u⃗ = AB⃗ = (x₂-x₁; y₂-y₁; z₂-z₁)

### 8.3 Phương trình mặt phẳng
- Dạng tổng quát: Ax + By + Cz + D = 0 (VTPT n⃗ = (A;B;C))
- Khoảng cách từ điểm M(x₀;y₀;z₀) đến mặt phẳng (Ax+By+Cz+D=0):
  d = |Ax₀+By₀+Cz₀+D| / √(A²+B²+C²)
- Khoảng cách giữa 2 mặt phẳng song song Ax+By+Cz+D₁=0 và Ax+By+Cz+D₂=0:
  d = |D₁-D₂| / √(A²+B²+C²)

### 8.4 Mặt cầu
- Phương trình: (x-a)² + (y-b)² + (z-c)² = R²
- Tâm I(a;b;c), bán kính R
- Dạng khai triển: x²+y²+z² - 2ax - 2by - 2cz + (a²+b²+c²-R²) = 0

---

## ĐỀ THI MINH HỌA — Câu hỏi mẫu

**Câu 1 (NB):** Cho hàm số y = x³ - 3x + 2. Số điểm cực trị của hàm là:
A. 0    B. 1    C. 2    D. 3
→ y' = 3x² - 3 = 3(x-1)(x+1) = 0 → x = ±1 (2 điểm cực trị) → **Đáp án C**

**Câu 2 (TH):** Tích phân ∫₀¹ (2x+1)dx = ?
→ F(x) = x² + x → F(1) - F(0) = 2 - 0 = **2**

**Câu 3 (VD):** Số nghiệm thực của phương trình 4ˣ - 3·2ˣ - 4 = 0:
→ Đặt t = 2ˣ (t > 0): t² - 3t - 4 = 0 → t = 4 hoặc t = -1 (loại)
→ 2ˣ = 4 → x = 2. **Có 1 nghiệm thực**

**Câu 4 (VD cao):** Tìm m để phương trình x³ - 3x² - 9x + m = 0 có 3 nghiệm phân biệt:
→ y = x³ - 3x² - 9x ; y' = 3x² - 6x - 9 = 3(x-3)(x+1) = 0
→ Cực đại y(-1) = -1-3+9 = 5 ; Cực tiểu y(3) = 27-27-27 = -27
→ Phương trình có 3 nghiệm phân biệt khi: -27 < -m < 5 → **-5 < m < 27**
