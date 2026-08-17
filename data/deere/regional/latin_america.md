# Deere & Company — Latin America regional desk
### FY2026 Q3 briefing (quarter ≈ 4 May – 2 Aug 2026)

**Prepared 16 August 2026. Deere has NOT reported FY2026 Q3.** The Q3 earnings call is 09:00 US Central,
Thursday 20 August 2026. Nothing in this note is a Q3 actual. Everything below is either (a) a verified
historical figure from the 10-Q/10-K revenue-recognition footnote, (b) a third-party statistic published
during or about the May–July 2026 window, or (c) my forecast, explicitly labelled.

**Basis warning.** All Deere revenue figures in this note are **revenue from contracts with customers**
(the ASC 606 primary-geographic-market footnote), *not* segment net sales. The two do not tie: Q2 FY2026
PPA is 4,607 on the 606 basis versus 4,503 in the 8-K segment table, a 104m gap. Do not mix bases when
aggregating.

**Corpus trap noted and avoided.** `INDEX.md` labels `call-transcripts/2026-05-21__…-call-qna__1042775.md`
as "Q3 2026". It is Q2 FY2026 material — it discusses the Q2 print and the guidance cut delivered that day.
Treated as Q2 throughout.

---

## 1. The seven-year history

Latin America quarterly revenue, USDm, ASC 606 basis. Extracted by script from the corpus filings
(`scripts/data/extract_latam_matrix.py`); Q4 rows are derived as fiscal-year minus nine-months from the
same footnote. FY2019 and the first half of FY2020 pre-date the PPA/SAT split and carry a combined
Agriculture & Turf figure instead — those cells are blank for PPA/SAT in the CSV, not zero.

| Fiscal quarter | PPA | SAT | CF | FS | **Total** | PPA YoY | Total YoY |
|---|---:|---:|---:|---:|---:|---:|---:|
| FY2021 Q3 | 758 | 125 | 227 | 60 | **1,170** | +48.0% | +50.6% |
| FY2022 Q3 | 1,327 | 155 | 459 | 77 | **2,018** | +75.1% | +72.5% |
| FY2023 Q3 | 1,326 | 220 | 371 | 117 | **2,034** | −0.1% | +0.8% |
| FY2024 Q3 | 841 | 125 | 305 | 94 | **1,365** | −36.6% | −32.9% |
| **FY2025 Q3** | **1,055** | **124** | **252** | **28** | **1,459** | **+25.4%** | **+6.9%** |
| FY2025 Q4 | 1,256 | 133 | 259 | 32 | **1,680** | +29.2% | +15.0% |
| FY2026 Q1 | 684 | 95 | 231 | 32 | **1,042** | −4.3% | −4.9% |
| FY2026 Q2 | 828 | 128 | 280 | 32 | **1,268** | −16.8% | −7.6% |

Fiscal-year totals: FY2022 7,339 → FY2023 8,197 → FY2024 5,538 → FY2025 **5,607**. Latin America *grew*
in FY2025 (PPA 3,482 → 4,021, +15%) while North America was falling. That is what makes FY2026 Q3 a hard
comparative.

Two structural notes:
- **FS is not deteriorating, it was deconsolidated.** LatAm FS revenue fell 453 (FY2024) → 197 (FY2025)
  because in Q2 FY2025 Deere sold 50% of Banco John Deere S.A. to Banco Bradesco (10-K,
  `2025-11-26__…-q4-10k__469216.md`). The quarterly run-rate has been stable at 28–32 ever since. Q3 FY2025
  onward is a clean comparable base.
- **Q3 seasonality in LatAm is mild.** Q3 is 26.0% of the fiscal-year PPA (median, FY2021–25, n=5) and the
  Q2→Q3 sequential move has a +6.0% median with a −14.1% to +17.9% range. Small sample; treat as a
  centring device, not a law.

---

## 2. What management said, and when

Deere cut the South America ag industry outlook **twice** this fiscal year, and the second cut is the
anchor for Q3:

| Date | South America tractors + combines | Source |
|---|---|---|
| 2025-11-26 (Q4 FY25 call) | **flat** | `call-transcripts/2025-11-26__…-call-q4-pres-2__361265.md` |
| 2026-02-19 (Q1 call) | **down ~5%** | `call-transcripts/2026-02-19__…-call-pres__605076.md` |
| 2026-05-21 (Q2 call) | **down ~15%** | `call-transcripts/2026-05-21__…-call-pres__1042774.md` |

Management's own read on 21 May, verbatim in substance: the revision to −15% "primarily reflect[s]
incremental softness in Brazil"; Brazilian tractor and combine industry retail "has declined about 15% in
six months"; Deere's Brazilian retail declined *less* than the industry; **small and mid-size tractors have
been more resilient while large tractors and combines have declined more than the industry overall**. The
causes cited were the Iran conflict's effect on oil and fertilizer, high interest rates, and the
strengthening real squeezing growers who sell in dollars.

Three operational statements matter more than the industry number:

1. **"In Brazil we expect to underproduce retail demand, most notably in combines."** (Q2 call, repeated
   from Q1.) This is a deliberate shipment cut, so Deere's Q3 revenue should be *worse* than Brazilian
   retail, not better.
2. **"Order visibility in both regions now extends through the third quarter and into the fourth."**
   (Q2 call.) Q3 shipments were largely committed before conditions worsened. This is the main thing
   stopping Q3 from falling off a cliff sequentially.
3. **Positive price realization and double-digit margins in Brazil "even at trough levels"**, with share
   gains across all tractor categories. The volume problem is not a competitive problem.

---

## 3. Brazil, country desk

### 3.1 The crop was excellent and prices held

CONAB's 11th survey (13 Aug 2026) puts the 2025/26 Brazilian grain crop at a record **360.75 Mt, +2.4%**,
on 83.5m ha (+2.1%). Soybeans **180.5 Mt** — the largest in the series. All-crop corn **142.96 Mt**, also a
record, of which safrinha **111.03 Mt**. Domestic prices in BRL were firm through the window: the
ESALQ/B3 corn indicator gained roughly 3% over July, and CEPEA reported soybean quotations easing only at
the very end of July after posting **the highest monthly averages of 2026**. Gross farm receipts in reais
were therefore fine. The problem is on the cost and financing side, not the revenue side.

### 3.2 …but the safrinha harvest ran badly late, inside the quarter

Second-crop corn was **~42% harvested at mid-July 2026, against 74% a year earlier and a 51% five-year
average**, after heavy June rain and cooler temperatures raised grain moisture. That is a ~4-week delay
sitting squarely in Deere's fiscal Q3. It pushes harvest-linked machine activity, dealer settlement and
farmer cash receipts toward Q4. It is a *timing* negative for Q3 and a modest positive for Q4.

### 3.3 Farm credit: rates fell, the pot did not grow, and buyers waited

**Plano Safra 2026/27, announced Tuesday 30 June 2026** (commercial agriculture tranche):

| | 2025/26 | 2026/27 | Change |
|---|---:|---:|---|
| Total | R$516.2bn | **R$525.1bn** | +1.7% nominal — a real-terms cut |
| Custeio + comercialização | R$414.7bn | R$384.9bn | −7% |
| **Investimento** (the machinery bucket) | R$101.5bn | **R$140.2bn** | **+38%** |
| Custeio empresarial rate | 14.0% | **12.5%** | −1.5pp |
| Pronamp cap | 10% | **9%** | −1pp |
| Floor rate across programmes | — | **8%** | |
| Moderfrota | — | R$3.7bn @12.5% | see caveat |
| Moderfrota Pronamp | — | R$2.1bn @11.5% | see caveat |

**Caveat, flagged rather than resolved:** one secondary source reports the combined Moderfrota allocation
of R$5.8bn as a **54% cut** year over year, which sits awkwardly against a 38% increase in the total
investment tranche. The plausible reconciliation is a reallocation away from Moderfrota toward Inovagro
(R$4.2bn @11.5%), PCA (R$3.4bn @11.5% plus R$2.5bn @8%) and RenovAgro (R$4.2bn @9.5%), all of which can
also finance equipment. I have **not** verified either figure against the primary MAPA/BCB resolution text
and have marked the CSV row accordingly. Someone should close this; it is the single biggest unresolved
item in the Brazilian demand picture.

The behavioural effect is clear and documented. ABIMAQ reports Brazilian agricultural machinery sales of
**R$4.97bn in June 2026, −22.3% YoY** (though **+8.3% versus May**), and **R$26.64bn in H1 CY2026, −21.3%
YoY**, attributing the deceleration explicitly to **producers waiting for the Plano Safra 2026/27 subsidised
rates announced at the end of that month**. ABIMAQ holds a −20% full-year call. ANFAVEA had Q1 CY2026
domestic ag machine sales at 9.8k units, −13.1%, and cut its CY2026 forecast to 46.7k units, −6.2%,
citing the Iran war's effect on fertilizer and freight plus high rates.

So: the market paused *into* the announcement (hurting May–June, i.e. Deere Q3) and the release of that
deferred demand lands after resource liberation — historically a lag of weeks to months — i.e. Deere's Q4
and FY2027. **The Plano Safra is a Q4/FY2027 positive that cost Q3.**

### 3.4 Rates, currency, inputs

- **Selic 14.25%** after a third consecutive cut on 17 June 2026, down from a 15.00% peak. Easing, but the
  real policy rate remains punishing and Deere flagged in May that expectations for further 2026 cuts had
  been *reduced* on inflation from the conflict.
- **USD/BRL averaged 5.0756 across Deere's fiscal Q3, against 5.5846 a year earlier — a 10.0% translation
  tailwind** to USD-reported Brazilian revenue (FRED `DEXBZUS`, 62 daily observations). Sequentially the
  real barely moved (5.1489 → 5.0756). This is the single most important number in this note: it means
  local-currency volume has to fall roughly 30% for USD revenue to print −20%.
- **Fertilizer eased after the guidance cut.** Urea spiked from ~US$400/t to **>US$850/t in April 2026** on
  the Strait of Hormuz disruption, then **fell back to US$453/t by June**. Brent averaged **$90.84** in
  Deere's fiscal Q3 versus **$97.63** in Q2 (and a $118 spot reading at the Q2 close) — still +32% YoY, but
  materially better than the peak fear priced into the 21 May guide.

### 3.5 Farm financial distress is real and getting worse

Serasa Experian counted **474 agribusiness judicial-recovery filings in Q1 CY2026, +21.9% YoY**, with rural
producers operating as legal entities at 196 filings, **+73.5%**. Neot's methodology gives 517, +33%, on
pace to beat last year's record. Average debt among defaulting rural borrowers has roughly tripled since
2023, ~75% of Banco do Brasil's defaulting farmers are first-time defaulters, and at least one major bank
has moved to halt credit to farmers filing for reorganisation. This is a slow-burning constraint on the
2027 recovery, not a Q3 swing factor, but it caps how bullish anyone should be about the rebound.

### 3.6 Deere's own Brazilian footprint — and the production cut that defines Q3

Deere has eight factories and four facilities in Brazil, over 12m sq ft: **Horizontina** (combines,
platforms, planters, cabins — where the business began in 1999), **Montenegro** (8R tractors, from 2008),
**Catalão**, **Indaiatuba** (construction & forestry from 2014, plus the R&D centre opened 2024), and the
**Campinas** parts distribution centre. Combine market share is up nearly 50% over fifteen years; tractor
share has risen steadily.

The operationally decisive fact for Q3: **Horizontina went to collective holidays from 12 March 2026 and
then to layoff — formal suspension of employment contracts — from 1 April, for two to five months,
affecting up to 887 workers, with roughly a 30% reduction in combine output over the period.** Catalão and
Montenegro were unaffected. That window covers essentially the whole of Deere's fiscal Q3. It is the
physical expression of "we will underproduce retail in combines," and it is the reason I do not expect
normal Q2→Q3 seasonality this year.

---

## 4. Argentina

The 2025/26 campaign was outstanding: **163.2 Mt total, +21.25% YoY** and a record, per the Secretaría de
Agricultura (22 May 2026). **Corn 71.5 Mt**, a record, on area up 26.1% to 11.6m ha and yields up to
7,240 kg/ha. **Soybeans 49.9 Mt** at 32.3 qq/ha, the second-best yield on record.

Policy moved the right way but slowly. Milei announced cuts at the Bolsa de Cereales on 21 May 2026;
**wheat and barley export tax fell 7.5% → 5.5%**, gazetted 3 June 2026. **Soybeans remained at 24%
throughout Deere's fiscal Q3** — the promised step-downs only begin January 2027 (to 21% by Dec 2027, 15%
by Dec 2028). Machinery is scheduled to reach zero export tax between July 2026 and June 2027.

Net: Argentine farm income was strong in the window, but the incremental policy relief a Deere customer
actually received during May–July was small, and Deere itself guided in November 2025 that Argentine
industry growth would "moderate after robust growth in 2025." Separately, ANFAVEA's automotive data shows
Brazilian vehicle exports to Argentina down 35.4% year-to-date through July — a demand-side warning about
the Argentine capital-goods cycle, though it is not ag equipment. **Argentina is a positive within the
region but is not large enough to offset Brazil.** The 606 footnote does not break Argentina out; I have
not attempted to synthesise a country split from the regional total.

## 5. Mexico and the rest

Deere runs sales/administrative offices, a parts depot and financial-services operations in Mexico, but the
country is not separately disclosed and is a modest share of the LatAm line. The peso appreciated 9.0%
year over year across Deere's fiscal Q3 (USD/MXN 17.38 average vs 19.09), giving the same direction of
translation tailwind as Brazil. Mexico's Deere exposure skews to SAT and CF rather than large ag, which is
consistent with those two segments holding up in the regional totals. I found no region-moving Mexican
policy event inside the window. Chile, Colombia and the Andean markets are immaterial at this resolution.

---

## 6. Did conditions improve or deteriorate versus the 21 May guidance?

The brief asked specifically. The honest answer is **mixed, and net roughly neutral-to-slightly-better on
fundamentals but slightly worse on Q3 shipment timing.**

**Improved since 21 May:**
- Urea collapsed from >$850/t (April peak) to $453/t (June); Brent fell from $118 spot at the Q2 close to a
  $90.84 quarterly average. The specific input-cost shock Deere named in its guidance cut partially unwound.
- Plano Safra 2026/27 landed on 30 June with rates down ~1.5pp and the investment tranche up 38%. Better
  than a flat renewal.
- Selic cut again on 17 June to 14.25%, a third consecutive cut.
- The crop finished at a record 360.75 Mt with soybean prices at their best monthly averages of 2026.

**Deteriorated or confirmed-negative since 21 May:**
- The safrinha harvest ran ~4 weeks late (42% vs 74% at mid-July), displacing activity out of Q3.
- ABIMAQ June −22.3% YoY and H1 −21.3% confirm the demand pause was deeper than the −15% industry guide
  implies in revenue terms, precisely because buyers deferred into the Plano Safra announcement.
- Horizontina's layoff and ~30% combine output cut ran through the entire quarter.
- Farm insolvencies kept setting records.

**Conclusion for the forecast:** the *fundamentals* for FY2027 improved during the window; the *shipments
recognisable in Q3 FY2026* did not. I therefore do not expect Deere to cut the South America industry guide
again on 20 August, and I would expect constructive commentary on 2027 — but I do expect the Q3 Latin
America PPA line itself to be weak, and weaker than the −15% industry number taken naively.

---

## 7. Forecast — FY2026 Q3, Latin America, ASC 606 basis

Anchored on the Q3 FY2025 comparative extracted from the 10-Q footnote
(`filings/2025-08-14__de-us-20250814-q3-10q__155834.md`): PPA 1,055 / SAT 124 / CF 252 / FS 28 /
Total 1,459.

| Segment | Q3 FY2025 | **Q3 FY2026 central** | **YoY** | Range | Confidence |
|---|---:|---:|---:|---|---|
| PPA | 1,055 | **820** | **−22.3%** | 760–900 | medium |
| SAT | 124 | **136** | **+9.7%** | 125–148 | medium |
| CF | 252 | **285** | **+13.1%** | 265–305 | medium |
| FS | 28 | **33** | **+17.9%** | 30–36 | medium |
| **Total** | **1,459** | **1,274** | **−12.7%** | 1,180–1,389 | medium |

**PPA reasoning.** Q2 FY2026 was 828. The five-year median Q2→Q3 sequential is +6.0%, but three things
argue against normal seasonality: a ~30% cut to Horizontina combine output running through the quarter, an
explicit plan to underproduce Brazilian retail, and a four-week-late safrinha harvest. Against that, the
order book was described on 21 May as covering Q3 and reaching into Q4, and the BRL delivers a +10.0%
translation tailwind. I take the sequential at roughly flat to −1%, giving ~820. Cross-check: at the
median 26.0% Q3 share of the fiscal year, 820 implies FY2026 LatAm PPA ~3,150 (−22% vs FY2025 4,021);
splitting the H2 residual at the historic Q3:Q4 ratio of ~0.84 from an FY of ~3,300 gives Q3 ~816. The two
methods agree. Implied ex-FX local-currency decline is roughly −29%, which is consistent with the −29%
already implied in Q2 and with ABIMAQ's −22% BRL revenue prints given Deere's mix skew to the
worst-affected categories (large tractors and combines).

**SAT reasoning.** Management calls small and mid-size tractors "more resilient," and the high-value-crop
franchise (coffee, citrus — the 5EN specialty tractor) benefits from tariff relief flagged in November. The
LatAm SAT Q2→Q3 sequential has been positive in all five observed years (+6.9% to +21.4%, median +15.7%).
I take a conservative +6% sequential off 128 given the general demand malaise, plus the FX tailwind.

**CF reasoning.** LatAm CF has been the region's growth engine: +12.7% in Q1 and +27.3% in Q2. Global
roadbuilding is guided up ~10% and global forestry down ~5%; Brazil carries both, plus Indaiatuba-built
earthmoving. Median Q2→Q3 sequential is only +3.2%, so I hold roughly flat sequentially and let the FX and
momentum carry the YoY to ~+13%.

**FS reasoning.** Purely a run-rate call on the post-Bradesco-JV base: 28, 32, 32, 32 over the last four
quarters. The YoY percentage looks dramatic but the absolute swing is $5m.

### Risks to this view
- **Upside:** the order book converts better than the production cut implies; Plano Safra demand releases
  faster than the historical resource-liberation lag; Deere's share gains and positive Brazilian price
  realisation carry more than modelled.
- **Downside:** the Horizontina suspension ran to the full five months rather than two; the late safrinha
  pushed dealer settlements further than assumed; a hard reading of "underproduce retail in combines"
  implies a sequential decline rather than flat.
- **Structural:** record insolvencies and a bank pull-back are a 2027 constraint that could make the
  "2026 is the bottom" thesis wrong for Brazil specifically even if it is right globally.

### What would change my mind
Brazilian retail data for May–July at the tractor/combine level (I could not source it — ANFAVEA's
ag-machinery series is published in spreadsheets behind a 406 and the monthly press releases carry only
automotive data). If Deere's Q3 Brazilian retail is down less than 10%, my PPA number is too low by roughly
50–70m.

---

## Sources

Corpus (paths relative to `challenge/offline-data/deere/`):
`filings/2019-05-17__…-q2-10q__469675.md`, `filings/2019-08-16__…-q3-10q__469206.md`,
`filings/2019-11-27__…-q4-10k__469283.md`, `filings/2020-02-21__…-q1-10q__468373.md`,
`filings/2020-05-21__…-q2-10q__469470.md`, `filings/2021-02-19__…-q1-10q__105814.md`,
`filings/2021-05-21__…-q2-10q__105821.md`, `filings/2021-08-20__…-q3-10q__105837.md`,
`filings/2021-11-24__…-q4-10k__131650.md`, `filings/2022-02-18__…-q1-10q__105834.md`,
`filings/2022-05-20__…-q2-10q__105838.md`, `filings/2022-08-19__…-q3-10q__105818.md`,
`filings/2022-11-23__…-q4-10k__105816.md`, `filings/2023-02-17__…-q1-10q__105813.md`,
`filings/2023-05-19__…-q2-10q__105852.md`, `filings/2023-08-18__…-q3-10q__105835.md`,
`filings/2023-11-22__…-q4-10k__105844.md`, `filings/2024-02-15__…-q1-10q__105826.md`,
`filings/2024-05-16__…-q2-10q__105820.md`, `filings/2024-08-15__…-q3-10q__105828.md`,
`filings/2024-11-21__…-q4-10k__105810.md`, `filings/2025-02-13__…-q1-10q__105832.md`,
`filings/2025-05-15__…-q2-10q__105831.md`, `filings/2025-08-14__…-q3-10q__155834.md`,
`filings/2025-11-26__…-q4-10k__469216.md`, `filings/2026-02-19__…-q1-10q__648937.md`,
`filings/2026-05-21__…-q2-10q__1055929.md`, `filings/2026-05-28__…-q2-10q__1055932.md`,
`call-transcripts/2025-06-10__…-call-pres-2__469351.md`, `slides/2025-06-10__…-slide__46442.md`,
`call-transcripts/2025-11-26__…-call-q4-pres-2__361265.md`, `call-transcripts/2025-11-26__…-call-q4-qna__361266.md`,
`call-transcripts/2026-02-19__…-call-pres__605076.md`, `call-transcripts/2026-02-19__…-call-qna__605077.md`,
`call-transcripts/2026-05-21__…-call-pres__1042774.md`, `call-transcripts/2026-05-21__…-call-qna__1042775.md`

Macro and market data:
- FRED `DEXBZUS`, `DEXMXUS`, `DCOILBRENTEU`, `PCU325311325311` — https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXBZUS (accessed 2026-08-16)
- CONAB 11th survey via O Tempo, 13 Aug 2026 — https://www.otempo.com.br/agro/2026/8/13/conab-estima-safra-de-graos-de-360-8-milhoes-de-toneladas-em-2025-26
- CONAB corn record via Forbes Brasil Agro, Aug 2026 — https://forbes.com.br/forbes-agro/2026/08/conab-eleva-projecao-recorde-para-safra-de-milho-do-brasil-em-25-26/
- Safrinha harvest pace (CONAB via Farm Progress), Jul 2026 — https://www.farmprogress.com/commentary/market-forecast-brazil-calls-the-shots
- Plano Safra 2026/27, CNN Brasil, 30 Jun 2026 — https://www.cnnbrasil.com.br/agro/governo-oficializa-plano-safra-2026-27-empresarial-de-r-5251-bilhoes/
- Plano Safra line-by-line, Agrishow Digital, Jul 2026 — https://digital.agrishow.com.br/gesto/plano-safra-2026-27-veja-os-principais-pontos-anunciados-para-o-credito-rural/
- Plano Safra rates, InfoMoney, Jun/Jul 2026 — https://www.infomoney.com.br/politica/plano-safra-reduz-juros-para-ate-9-ao-ano-e-amplia-credito-para-r-525-bilhoes/
- Plano Safra > R$610bn incl. Pronaf, Ministério da Fazenda, Jul 2026 — https://www.gov.br/fazenda/pt-br/assuntos/noticias/2026/julho/plano-safra-2026-2027-supera-r-610-bilhoes-com-participacao-da-fazenda-na-reducao-de-juros-e-equilibrio-nas-contas-publicas
- Copom cuts Selic to 14.25%, Agência Brasil, 17 Jun 2026 — https://agenciabrasil.ebc.com.br/economia/noticia/2026-06/copom-reduz-taxa-selic-para-1425-ao-ano
- ABIMAQ June/H1 machinery sales, CNN Brasil, Jul 2026 — https://www.cnnbrasil.com.br/agro/vendas-de-maquinas-agricolas-caem-mais-de-22-em-junho-diz-abimaq/
- ANFAVEA Q1 CY2026 ag machines −13%, IstoÉ Dinheiro, Apr 2026 — https://istoedinheiro.com.br/vendas-de-maquinas-agricolas-caem-13-no-1o-tri-na-comparacao-anual-diz-anfavea
- ANFAVEA CY2026 forecast −6.2%, Reuters via Investing Brasil, Apr 2026 — https://br.investing.com/news/world-news/anfavea-ve-queda-de-62-nas-vendas-de-maquinas-agricolas-no-brasil-em-2026-com-guerra-e-juros-altos-1898781
- ANFAVEA August release (July data, automotive only) — https://anfavea.com.br/site/wp-content/uploads/2026/08/RELEASE-AGOSTO26.pdf
- Agribusiness judicial recoveries +21.9%, Canal Rural, 2026 — https://www.canalrural.com.br/economia/recuperacao-judicial-no-agro-sobe-219-no-1o-trimestre-de-2026
- Agribusiness bankruptcies +33% Q1, Rio Times, 2026 — https://www.riotimesonline.com/brazil-agribusiness-bankruptcies-surge-33-in-q1/
- Banks tighten farm credit, The AgriBiz, 2026 — https://www.theagribiz.com/agronegocio/brazilian-banks-take-harder-line-as-farm-credit-strains-deepen
- Iran war fertilizer/energy costs in Brazil and Argentina, IFPRI, 2026 — https://www.ifpri.org/blog/the-iran-war-farmers-in-brazil-and-argentina-face-rising-fertilizer-and-energy-prices/
- Fertilizer trade and the Strait of Hormuz, World Bank, 2026 — https://blogs.worldbank.org/en/opendata/fertilizer-prices-surge-as-strait-of-hormuz-disruptions-tighten-
- CEPEA soybean, end-July 2026 — https://cepea.org.br/br/diarias-de-mercado/soja-cepea-cotacoes-recuam-no-fim-de-julho-medias-sao-as-maiores-de-2026.aspx
- CEPEA corn, July 2026 — https://www.cepea.org.br/br/diarias-de-mercado/milho-safrinha-avanca-e-preco-comeca-a-cair.aspx
- Deere Horizontina collective holidays and layoff, AgFeed, Feb 2026 — https://agfeed.com.br/negocios/a-espera-da-recuperacao-john-deere-da-ferias-coletivas-e-layoff-a-trabalhadores-e-reduz-producao-no-rs/
- Argentina record 163.2 Mt crop, Argentina.gob.ar, May 2026 — https://www.argentina.gob.ar/noticias/la-produccion-de-granos-alcanzo-una-cosecha-record-que-supero-las-163-millones-de-toneladas
- Argentina record 71.5 Mt corn, Argentina.gob.ar, 2026 — https://www.argentina.gob.ar/noticias/la-produccion-de-maiz-marca-un-record-historico-con-715-millones-de-toneladas
- Argentina soybean 49.9 Mt, RuralNet, 2026 — https://ruralnet.com.ar/cosecha-soja-argentina-2025-26-produccion-50-millones-toneladas/
- Argentina export tax cuts, USDA FAS GAIN, Jun 2026 — https://www.fas.usda.gov/data/gain/2026/06/argentina-argentina-further-cuts-agricultural-export-taxes

Reproducible scripts: `scripts/data/extract_latam_matrix.py`, `scripts/data/latam_fx_macro.py`,
`scripts/data/build_latam_csv.py`, `scripts/data/latam_q3_forecast.py`.
