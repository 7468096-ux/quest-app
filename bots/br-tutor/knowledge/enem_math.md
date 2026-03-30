# Matemática para o ENEM — Fórmulas e Conceitos Essenciais

> Este guia cobre os principais tópicos de Matemática cobrados no ENEM, com fórmulas, exemplos e dicas de resolução.

---

## 1. ARITMÉTICA E TEORIA DOS NÚMEROS

### Razão e Proporção
- **Razão**: comparação entre duas grandezas. Ex: a/b
- **Proporção**: igualdade entre duas razões: a/b = c/d → a·d = b·c (produto dos extremos = produto dos meios)
- **Grandezas diretamente proporcionais**: quando uma aumenta, a outra aumenta na mesma razão.
- **Grandezas inversamente proporcionais**: quando uma aumenta, a outra diminui na mesma proporção.

### Porcentagem
- **Fórmula**: P% de X = (P/100) × X
- **Acréscimo**: novo valor = X × (1 + P/100)
- **Desconto**: novo valor = X × (1 – P/100)
- **Variação percentual**: [(valor final – valor inicial) / valor inicial] × 100

**Exemplo ENEM**: Um produto custava R$80 e sofreu redução de 15%. Qual o novo preço?
Solução: 80 × (1 – 0,15) = 80 × 0,85 = **R$68,00**

### Regra de Três

**Simples (duas grandezas)**:
```
A₁ → B₁
A₂ → B₂

Direta: A₁/A₂ = B₁/B₂  →  B₂ = (A₂ × B₁)/A₁
Inversa: A₁ × B₁ = A₂ × B₂
```

**Composta (três ou mais grandezas)**: Montar a proporção com cada par e verificar o tipo de cada relação.

---

## 2. ÁLGEBRA

### Equações do 1º Grau

**Forma geral**: ax + b = 0 → x = –b/a (com a ≠ 0)

### Equações do 2º Grau — Bhaskara

**Forma geral**: ax² + bx + c = 0 (a ≠ 0)

**Fórmula de Bhaskara**:
$$x = \frac{-b \pm \sqrt{\Delta}}{2a}$$

**Discriminante**: Δ = b² – 4ac
- Δ > 0: duas raízes reais distintas
- Δ = 0: raízes reais iguais (x = –b/2a)
- Δ < 0: sem raízes reais (raízes complexas)

**Relações de Girard**:
- Soma das raízes: x₁ + x₂ = –b/a
- Produto das raízes: x₁ · x₂ = c/a

**Exemplo**: x² – 5x + 6 = 0
Δ = 25 – 24 = 1 → x = (5 ± 1)/2 → x₁ = 3 e x₂ = 2 ✓

### Sistemas de Equações Lineares

**2×2** — Métodos:
- **Substituição**: isolar uma variável e substituir
- **Adição/Eliminação**: multiplicar equações para eliminar uma variável
- **Matriz/Regra de Cramer**: det(A) ≠ 0 para sistema determinado

### Inequações
- Ao multiplicar ou dividir por número **negativo**, inverte-se o sinal da desigualdade.
- Inequação do 2º grau: analisar sinal da parábola (Δ, concavidade).

### Progressões

**Progressão Aritmética (PA)**
- Termo geral: aₙ = a₁ + (n–1)·r
- Soma dos n primeiros termos: Sₙ = n·(a₁ + aₙ)/2
- r = razão da PA

**Exemplo**: PA (2, 5, 8, 11, ...) → a₁=2, r=3
- a₁₀ = 2 + 9×3 = 29
- S₁₀ = 10×(2+29)/2 = 155

**Progressão Geométrica (PG)**
- Termo geral: aₙ = a₁ · q^(n–1)
- Soma dos n primeiros termos: Sₙ = a₁·(qⁿ – 1)/(q – 1), para q ≠ 1
- Soma de PG infinita (|q| < 1): S = a₁/(1 – q)
- q = razão da PG

**Exemplo**: PG (3, 6, 12, 24, ...) → a₁=3, q=2
- a₆ = 3 × 2⁵ = 96
- S₅ = 3×(2⁵–1)/(2–1) = 3×31 = 93

---

## 3. FUNÇÕES

### Função do 1º Grau (Afim)

**Forma**: f(x) = ax + b (a ≠ 0)
- Gráfico: reta
- **a > 0**: função crescente
- **a < 0**: função decrescente
- Raiz (zero): x = –b/a
- Coeficiente angular: a (tangente do ângulo com eixo x)
- Coeficiente linear: b (intersecção com eixo y)

### Função do 2º Grau (Quadrática)

**Forma**: f(x) = ax² + bx + c (a ≠ 0)
- Gráfico: parábola
- **a > 0**: concavidade para cima (mínimo)
- **a < 0**: concavidade para baixo (máximo)
- Vértice: V = (–b/2a, –Δ/4a)
- Eixo de simetria: x = –b/2a

**Dica ENEM**: O valor mínimo ou máximo da função quadrática é sempre –Δ/4a.

### Função Exponencial

**Forma**: f(x) = aˣ (a > 0, a ≠ 1)
- **a > 1**: crescente
- **0 < a < 1**: decrescente
- Domínio: todos os reais; Imagem: reais positivos
- Aplicação: juros compostos, crescimento populacional, decaimento radioativo.

### Função Logarítmica

**Forma**: f(x) = logₐ(x) (a > 0, a ≠ 1, x > 0)
- É a inversa da exponencial.

**Propriedades dos logaritmos**:
- log(A·B) = log A + log B
- log(A/B) = log A – log B
- log(Aⁿ) = n·log A
- logₐ(a) = 1
- logₐ(1) = 0
- Mudança de base: logₐ(b) = log(b)/log(a)

---

## 4. JUROS — MATEMÁTICA FINANCEIRA

### Juros Simples

**Fórmulas**:
- J = C × i × t
- M = C × (1 + i×t)

Onde: C = capital; i = taxa (em decimal); t = tempo; M = montante; J = juros

**Exemplo**: Capital R$2.000, taxa 5% ao mês, 3 meses.
J = 2000 × 0,05 × 3 = **R$300**; M = 2.300

### Juros Compostos (mais cobrado no ENEM)

**Fórmulas**:
- M = C × (1 + i)ᵗ
- J = M – C

**Exemplo**: Capital R$1.000, taxa 10% ao ano, 2 anos.
M = 1000 × (1,1)² = 1000 × 1,21 = **R$1.210**; J = R$210

**Dica**: No ENEM, use log para descobrir o tempo (t):
t = log(M/C) / log(1+i)

---

## 5. GEOMETRIA PLANA

### Figuras e Fórmulas de Área

| Figura | Área | Perímetro |
|--------|------|-----------|
| Quadrado (lado l) | l² | 4l |
| Retângulo (b×h) | b×h | 2(b+h) |
| Triângulo (base b, altura h) | b×h/2 | a+b+c |
| Trapézio (B, b, h) | (B+b)×h/2 | soma dos lados |
| Losango (d₁, d₂) | d₁×d₂/2 | 4l |
| Círculo (raio r) | πr² | 2πr |
| Setor circular (raio r, ângulo α°) | πr²×α/360 | 2r + arco |

### Teorema de Pitágoras

Em todo triângulo retângulo: **a² = b² + c²**
(a = hipotenusa; b e c = catetos)

**Ternas pitagóricas comuns**: (3,4,5); (5,12,13); (8,15,17); (6,8,10)

### Triângulos Especiais

**Triângulo 30°–60°–90°**: lados em proporção 1 : √3 : 2
**Triângulo 45°–45°–90°** (isósceles retângulo): lados em proporção 1 : 1 : √2

### Semelhança de Triângulos

Dois triângulos são semelhantes (AA, LLL, LAL) quando:
- Razão de semelhança k → razão de áreas = k²; razão de volumes = k³

---

## 6. GEOMETRIA ESPACIAL

### Volumes e Áreas

| Sólido | Volume | Área Total |
|--------|--------|-----------|
| Cubo (aresta a) | a³ | 6a² |
| Paralelepípedo (a,b,c) | a×b×c | 2(ab+bc+ac) |
| Cilindro (r, h) | πr²h | 2πr(r+h) |
| Cone (r, h, g) | πr²h/3 | πr(r+g) |
| Esfera (r) | 4πr³/3 | 4πr² |
| Pirâmide | Ab×h/3 | Ab + soma dos triângulos laterais |

Onde g = geratriz do cone: g = √(r² + h²)

**Diagonal do cubo**: d = a√3
**Diagonal do paralelepípedo**: d = √(a²+b²+c²)

---

## 7. TRIGONOMETRIA

### Razões Trigonométricas no Triângulo Retângulo

```
sen α = cateto oposto / hipotenusa
cos α = cateto adjacente / hipotenusa
tg α  = cateto oposto / cateto adjacente
```

**Relação fundamental**: sen²α + cos²α = 1

### Tabela de Valores

| Ângulo | sen | cos | tg |
|--------|-----|-----|----|
| 0° | 0 | 1 | 0 |
| 30° | 1/2 | √3/2 | √3/3 |
| 45° | √2/2 | √2/2 | 1 |
| 60° | √3/2 | 1/2 | √3 |
| 90° | 1 | 0 | ∞ |

### Lei dos Senos e Lei dos Cossenos

**Lei dos Senos**: a/sen A = b/sen B = c/sen C = 2R

**Lei dos Cossenos**: a² = b² + c² – 2bc·cos A
(generalização do Teorema de Pitágoras para qualquer triângulo)

### Funções Trigonométricas no Ciclo Unitário

- Período de sen e cos: 2π (360°)
- Período de tg: π (180°)
- Amplitude de sen e cos: 1 (varia entre -1 e 1)

---

## 8. ESTATÍSTICA E PROBABILIDADE

### Estatística Descritiva

- **Média aritmética**: x̄ = (x₁+x₂+…+xₙ)/n
- **Média ponderada**: x̄ = (x₁p₁+x₂p₂+…)/(p₁+p₂+…)
- **Mediana**: valor central (dados ordenados). Para n par: média dos dois centrais.
- **Moda**: valor mais frequente.
- **Desvio padrão**: mede dispersão; σ = √(Σ(xᵢ–x̄)²/n)
- **Variância**: σ² = Σ(xᵢ–x̄)²/n

### Probabilidade

**Fórmula básica**: P(A) = nº de casos favoráveis / nº de casos possíveis (igualmente prováveis)

**Propriedades**:
- 0 ≤ P(A) ≤ 1
- P(A) + P(Ā) = 1 (complementar)
- P(A ∪ B) = P(A) + P(B) – P(A ∩ B)
- Se A e B independentes: P(A ∩ B) = P(A) × P(B)
- Se A e B mutuamente exclusivos: P(A ∩ B) = 0

### Análise Combinatória

**Fatorial**: n! = n × (n–1) × … × 2 × 1; 0! = 1

**Permutação simples** (n objetos distintos, todos usados):
P(n) = n!

**Arranjo** (n objetos, p a p, sem repetição):
A(n,p) = n!/(n–p)!

**Combinação** (grupos sem importar ordem):
C(n,p) = n!/[p!(n–p)!]

**Exemplo ENEM**: De um grupo de 6 pessoas, quantas comissões de 3 podem ser formadas?
C(6,3) = 6!/(3!×3!) = 720/36 = **20 comissões**

---

## 9. LEITURA DE GRÁFICOS E TABELAS

O ENEM frequentemente apresenta dados em gráficos de barra, linha, pizza ou tabelas. Pontos-chave:

- Leia sempre o título, os eixos e as unidades antes de responder.
- Calcule variação percentual: [(final–inicial)/inicial]×100
- Identifique tendências (crescimento, decaimento, sazonalidade)
- Cuidado com escalas que não começam em zero (podem distorcer a percepção visual)

---

## 10. DICAS GERAIS PARA O ENEM

1. **Leia todo o enunciado** — muitos dados estão no texto, não só na pergunta.
2. **Estime antes de calcular** — elimine alternativas absurdas.
3. **Unidades**: converta tudo para a mesma unidade antes de calcular.
4. **Geometria**: desenhe e marque os dados conhecidos.
5. **Tempo**: gaste no máximo 3 minutos por questão; marque e volte depois.
6. **π ≈ 3,14** ou **22/7** — use o valor que o ENEM fornecer no enunciado.
7. **√2 ≈ 1,41**; **√3 ≈ 1,73** — memorize esses valores.

---

*Material preparado com base no conteúdo programático do ENEM (INEP). Última atualização: 2025.*
