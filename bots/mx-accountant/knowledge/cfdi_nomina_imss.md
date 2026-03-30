# CFDI, Nómina e IMSS en México

## CFDI (Comprobante Fiscal Digital por Internet)

### ¿Qué es el CFDI?
El CFDI es la factura electrónica oficial en México. Es el único documento fiscal válido para:
- Deducir gastos del ISR
- Acreditar IVA
- Comprobar ingresos y pagos

**Versión actual:** CFDI 4.0 (obligatorio desde 1 enero 2022)

---

### Estructura del CFDI 4.0

**Datos obligatorios del emisor:**
- RFC del emisor (12 o 13 caracteres)
- Nombre o razón social del emisor
- Régimen fiscal del emisor
- Código postal del domicilio fiscal del emisor
- Número de certificado del CSD

**Datos obligatorios del receptor:**
- RFC del receptor
- Nombre o razón social del receptor
- **Uso del CFDI** (nuevo en 4.0) — clave del SAT según el uso
- Régimen fiscal del receptor (nuevo en 4.0)
- Código postal del domicilio fiscal del receptor

**Usos del CFDI más comunes:**

| Clave | Descripción |
|-------|------------|
| G01 | Adquisición de mercancias |
| G02 | Devoluciones, descuentos o bonificaciones |
| G03 | Gastos en general |
| I01 | Construcciones |
| I02 | Mobilario y equipo de oficina |
| I04 | Equipo de computo y accesorios |
| I06 | Comunicaciones telefónicas |
| D01 | Honorarios médicos, dentales y gastos hospitalarios |
| D03 | Gastos funerales |
| D04 | Donativos |
| D05 | Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación) |
| D07 | Primas por seguros de gastos médicos |
| D09 | Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones |
| D10 | Pagos por servicios educativos (colegiaturas) |
| CP01 | Pagos (solo para complemento de pagos) |
| CN01 | Nómina (solo para comprobante de nómina) |
| S01 | Sin efectos fiscales |

---

### Tipos de CFDI

**1. Ingreso:** Para comprobar ingresos por venta de bienes o servicios prestados.

**2. Egreso (nota de crédito):** Para registrar devoluciones, descuentos o bonificaciones.

**3. Traslado:** Para acompañar mercancías en tránsito (requiere complemento de carta porte).

**4. Pago (REP — Recibo Electrónico de Pago):**
- Se emite cuando el pago NO se recibió al momento de la factura
- Crédito, transferencias, etc.
- Complemento de Pagos

**5. Nómina:** Para comprobar pagos a trabajadores (con complemento de nómina 1.2).

---

### CFDI de Nómina (Complemento 1.2)

**Obligatorio para:** Todos los patrones que paguen sueldos, salarios, asimilados.

**Datos específicos del complemento de nómina:**
- Tipo de nómina: Ordinaria / Extraordinaria
- Fecha de pago
- Fecha inicio y fin del periodo pagado
- Días pagados
- Percepciones (salario ordinario, horas extra, prima vacacional, etc.)
- Deducciones (ISR retenido, IMSS trabajador, INFONAVIT, etc.)
- Datos del IMSS (NSS del trabajador, tipo de contrato, tipo de jornada)

**Periodicidad de emisión:**
- Semanal: viernes o día de pago
- Catorcenal / Quincenal: en fecha de pago
- Mensual: en fecha de pago

**Plazo para emitir:** Hasta 3 días después del día de pago (recomendado: mismo día)

---

### Cancelación de CFDI

**¿Cuándo se puede cancelar?**
- Error en datos del receptor (RFC incorrecto, nombre mal escrito)
- Error en importe, concepto o tasa
- Factura emitida sin corresponder a operación real
- Devolución total de mercancía

**¿Cuándo NO se puede cancelar?**
- Si el receptor ya usó el CFDI para deducción o acreditamiento (en muchos casos)
- Si hay obligación de complemento de pagos

**Proceso de cancelación:**

1. **Con aceptación del receptor:**
   - Aplica cuando: hay relación comercial o el receptor es persona moral
   - Emisor solicita cancelación → receptor recibe aviso en buzón tributario
   - Receptor tiene 72 horas para aceptar/rechazar
   - Sin respuesta en 72h → cancelación automática

2. **Sin aceptación del receptor:**
   - RFC del receptor: XAXX010101000 (público en general) o XEXX010101000 (extranjero)
   - Monto ≤ $1,000 (cancelación directa sin aceptación)
   - Facturas emitidas en el mes en curso (regla flexible por SAT)

**Plazos para cancelar:**
- CFDI del ejercicio en curso: hasta **31 de enero del año siguiente**
- CFDI de ejercicios anteriores: procedimiento especial ante el SAT

---

### Facturación al Público en General (CFDI Global)

Cuando no se puede identificar al receptor:
- RFC receptor: **XAXX010101000** (nacionales)
- RFC receptor: **XEXX010101000** (extranjeros)
- Nombre: "Público en General"
- Código postal: el del domicilio fiscal del emisor
- Uso CFDI: S01 (Sin efectos fiscales)
- Régimen fiscal receptor: 616 (Sin obligaciones fiscales)

**CFDI Global (resumen):**
- Se puede emitir un CFDI global diario, semanal, mensual o bimestral
- Consolida todas las operaciones con público en general
- Recomendado para negocios con muchas ventas de bajo monto (tiendas, restaurantes)

---

## IMSS — Instituto Mexicano del Seguro Social

### Obligaciones del Patrón

**Alta del trabajador:**
- Fecha límite: **el mismo día que inicia labores** (artículo 15 LSS)
- Portal IMSS: imss.gob.mx → IDSE (IMSS Desde su Empresa)
- O mediante IMSS Digital para patrones con e.firma

**Documentos necesarios para el alta:**
- CURP del trabajador
- NSS (Número de Seguridad Social) — si no tiene, el IMSS lo asigna
- RFC del trabajador (desde 2022 obligatorio)
- Datos del contrato (tipo, duración, salario)

---

### Salario Base de Cotización (SBC)

El SBC es la base para calcular las cuotas IMSS e INFONAVIT.

**Integración del SBC:**
- Salario ordinario
- + Partes proporcionales diarias de: aguinaldo, prima vacacional, tiempo extra habitual
- + Comisiones promedio
- + Premios, bonos, incentivos de pago regular
- − Concepciones EXENTAS de integración (por ley)

**Percepciones NO integran al SBC (límites):**
- Instrumentos de trabajo (herramientas, uniformes)
- Fondo de ahorro (igual aportación patrón-trabajador, ≤13% del SalMin)
- Vales de despensa y fondo de ahorro (hasta 30% del SM diario)
- Cuotas al IMSS pagadas por el patrón

**Topes del SBC:**
- Máximo: 25 UMAs ($2,977.50/día en 2024 — verificar actualización anual)
- Mínimo: 1 UMA diaria ($108.57/día en 2024)

---

### Cuotas IMSS 2024

**Las cuotas se dividen en ramos:**

| Ramo | Patrón | Trabajador |
|------|--------|-----------|
| Enfermedad y Maternidad (prestaciones en especie) | 20.40% sobre base de $1 SM + diferencial | Según tabla |
| Enfermedad y Maternidad (dinero) | 0.70% | 0.25% |
| Invalidez y Vida | 1.75% | 0.625% |
| Retiro (SAR) | 2.00% | 0% |
| Cesantía y Vejez (AFORE) | 3.150% | 1.125% |
| Guarderías y Prestaciones Sociales | 1.00% | 0% |
| Riesgos de Trabajo (SIMIT) | Variable (0.5% — 15%) | 0% |

*Nota: Los porcentajes exactos varían con el salario y pueden cambiar anualmente. Consultar tablas oficiales del IMSS.*

**Calculo simplificado (estimación):**
- Cuota patronal total ≈ **25-30%** del SBC mensual
- Cuota obrera total ≈ **2-3%** del SBC mensual

---

### SUA (Sistema Único de Autodeterminación)

Software gratuito del IMSS para calcular y pagar cuotas.

**Funciones del SUA:**
- Cálculo automático de cuotas IMSS (todos los ramos)
- Generación del archivo de pago (IDSE)
- Control de altas, bajas y modificaciones salariales
- Generación de CFDI de pago (para patrones obligados)

**Descarga:** imss.gob.mx → Patrones → SUA

**Pago de cuotas IMSS:**
- Plazos: Mensualmente, los primeros 17 días del mes siguiente
- Banco o BBVA IMSS Digital

---

### INFONAVIT

**Aportación patronal:** 5% del SBC mensual (obligatoria para todos los trabajadores)

**Destino:** Fondo de vivienda individual del trabajador (puede usarse para crédito hipotecario o como ahorro para el retiro)

**Crédito INFONAVIT:**
- El trabajador puede solicitar crédito después de ciertos puntos acumulados
- El patrón debe hacer descuento mensual de la amortización del crédito (si el trabajador tiene crédito activo)

**Pago al INFONAVIT:**
- Junto con el IMSS, en los primeros 17 días del mes siguiente
- Mismo SBC que el IMSS

---

### Prestaciones Mínimas de Ley (LFT — Ley Federal del Trabajo)

| Prestación | Mínimo legal |
|-----------|-------------|
| Salario | Mínimo vigente ($248.93/día general en 2024; $374.89 zona frontera norte) |
| Vacaciones (1er año) | 12 días |
| Vacaciones (incremento) | +2 días por cada año, hasta 20 días (a partir del año 6, +2 cada 5 años) |
| Prima vacacional | 25% del salario durante vacaciones |
| Aguinaldo | 15 días de salario (pago antes del 20 de diciembre) |
| PTU | 10% de la utilidad fiscal del patrón (pago antes del 30 de mayo) |
| IMSS | Alta desde el primer día |
| INFONAVIT | 5% del SBC mensual |
| Séptimo día (descanso semanal) | Con goce de salario |

---

### PTU (Participación de los Trabajadores en las Utilidades)

**¿Qué es?** El 10% de la utilidad fiscal del ejercicio se distribuye entre trabajadores.

**Plazo de pago:**
- Personas morales: **60 días después de presentar declaración anual** (hasta ~30 de mayo)
- Personas físicas con trabajadores: **60 días después del 30 de abril** (hasta ~29 de junio)

**¿Quiénes tienen derecho?**
- Trabajadores que laboraron al menos 60 días en el año
- Trabajadores eventuales con más de 60 días acumulados

**¿Quiénes NO tienen derecho?**
- Directores generales, gerentes generales
- Socios o accionistas
- Trabajadores domésticos
- Trabajadores estacionales menores de 60 días

**Cálculo y distribución:**
- 50% de la PTU total se distribuye a partes iguales entre trabajadores (días laborados)
- 50% restante en proporción al salario percibido

**Exención del ISR para el trabajador:**
- PTU exenta: la mayor entre 15 días de salario mínimo O el 90% de la PTU recibida
- El excedente sí paga ISR (retención por el patrón)

---

### Finiquito e Indemnización

**Finiquito (renuncia voluntaria):**
- Parte proporcional de aguinaldo
- Parte proporcional de vacaciones no disfrutadas
- Prima vacacional proporcional
- PTU pendiente

**Indemnización (despido injustificado — artículo 123 Constitucional + LFT):**
- 3 meses de salario integrado
- 20 días por año de servicio
- Partes proporcionales (aguinaldo, vacaciones, prima)
- Prima de antigüedad: 12 días por año de servicio (hasta 2 SalMin diarios)

**Salario integrado para finiquito:**
- Salario diario + parte proporcional de aguinaldo + prima vacacional + otras prestaciones regulares

*Ejemplo: Salario diario $500 + aguinaldo (15d/365 × $500 = $20.55) + prima vacacional (12d × 25% / 365 × $500 = $4.11) = Salario integrado ≈ $524.66/día*
