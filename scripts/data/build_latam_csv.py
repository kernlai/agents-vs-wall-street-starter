#!/usr/bin/env python3
"""Build the Latin America regional tidy-long CSV for the Deere FY2026 Q3 bottom-up forecast.

Inputs:
  - ASC 606 primary-geographic-market matrix rows parsed by extract_latam_matrix.py
    (Deere 10-Q / 10-K corpus, /challenge/offline-data/deere/filings)
  - Q4 rows derived as (fiscal year) - (nine months) from the same footnote
  - FRED daily series averaged over Deere fiscal quarters
  - Hand-keyed country/policy series from cited public sources

Output: /data/deere/regional/latin_america.csv
"""
import csv, io, os, json, statistics, urllib.request, subprocess, sys

OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/regional/latin_america.csv"
HDR = ["series_id","period_end","fiscal_year","fiscal_quarter","geography","country",
       "segment","value","units","source_type","source","notes"]
rows = []
def add(**k):
    rows.append({h: k.get(h,"") for h in HDR})

# ---------------------------------------------------------------- 1. segment matrix
F = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings/"
CORP = "challenge/offline-data/deere/filings/"

# (period_end, FY, FQ, PPA, SAT, CF, FS, Total, source_basename, note)
# 3-month rows parsed from the revenue-recognition footnote; FY2019-FY2020H1 pre-date the
# PPA/SAT split, so those quarters carry a combined Agriculture & Turf figure instead.
Q = [
 ("2019-01-27",2019,"Q1",None,None,150,64,762,"2020-02-21__de-us-20200221-q1-10q__468373.md","A&T 548 (pre-PPA/SAT split)",548),
 ("2019-04-28",2019,"Q2",None,None,194,69,1035,"2019-05-17__de-us-20190517-q2-10q__469675.md","A&T 772 (pre-split)",772),
 ("2019-07-28",2019,"Q3",None,None,171,66,945,"2019-08-16__de-us-20190816-q3-10q__469206.md","A&T 708 (pre-split)",708),
 ("2019-10-27",2019,"Q4",None,None,204,73,1143,"2019-11-27__de-us-20191127-q4-10k__469283.md","derived FY-9M; A&T 866 (pre-split)",866),
 ("2020-02-02",2020,"Q1",None,None,159,66,680,"2020-02-21__de-us-20200221-q1-10q__468373.md","A&T 455 (pre-split)",455),
 ("2020-05-03",2020,"Q2",None,None,135,60,653,"2020-05-21__de-us-20200521-q2-10q__469470.md","A&T 458 (pre-split)",458),
 ("2020-08-02",2020,"Q3",512,90,124,51,777,"2021-08-20__de-us-20210820-q3-10q__105837.md","restated PPA/SAT comparative",None),
 ("2020-11-01",2020,"Q4",None,None,135,57,913,"2021-11-24__de-us-20211124-q4-10k__131650.md","derived FY-9M; A&T 721",721),
 ("2021-01-31",2021,"Q1",513,77,170,59,819,"2021-02-19__de-us-20210219-q1-10q__105814.md","",None),
 ("2021-05-02",2021,"Q2",700,103,220,60,1083,"2021-05-21__de-us-20210521-q2-10q__105821.md","",None),
 ("2021-08-01",2021,"Q3",758,125,227,60,1170,"2021-08-20__de-us-20210820-q3-10q__105837.md","",None),
 ("2021-10-31",2021,"Q4",945,151,286,68,1450,"2021-11-24__de-us-20211124-q4-10k__131650.md","derived FY-9M",None),
 ("2022-01-30",2022,"Q1",776,104,228,68,1176,"2022-02-18__de-us-20220218-q1-10q__105834.md","",None),
 ("2022-05-01",2022,"Q2",1126,134,333,73,1666,"2022-05-20__de-us-20220520-q2-10q__105838.md","",None),
 ("2022-07-31",2022,"Q3",1327,155,459,77,2018,"2022-08-19__de-us-20220819-q3-10q__105818.md","",None),
 ("2022-10-30",2022,"Q4",1762,185,447,85,2479,"2022-11-23__de-us-20221123-q4-10k__105816.md","derived FY-9M",None),
 ("2023-01-29",2023,"Q1",1237,156,339,95,1827,"2023-02-17__de-us-20230217-q1-10q__105813.md","",None),
 ("2023-04-30",2023,"Q2",1543,201,388,106,2238,"2023-05-19__de-us-20230519-q2-10q__105852.md","",None),
 ("2023-07-30",2023,"Q3",1326,220,371,117,2034,"2023-08-18__de-us-20230818-q3-10q__105835.md","",None),
 ("2023-10-29",2023,"Q4",1502,130,331,135,2098,"2023-11-22__de-us-20231122-q4-10k__105844.md","derived FY-9M",None),
 ("2024-01-28",2024,"Q1",819,98,256,130,1303,"2024-02-15__de-us-20240215-q1-10q__105826.md","",None),
 ("2024-04-28",2024,"Q2",850,103,334,122,1409,"2024-05-16__de-us-20240516-q2-10q__105820.md","",None),
 ("2024-07-28",2024,"Q3",841,125,305,94,1365,"2024-08-15__de-us-20240815-q3-10q__105828.md","",None),
 ("2024-10-27",2024,"Q4",972,107,275,107,1461,"2024-11-21__de-us-20241121-q4-10k__105810.md","derived FY-9M",None),
 ("2025-01-26",2025,"Q1",715,80,205,96,1096,"2025-02-13__de-us-20250213-q1-10q__105832.md","",None),
 ("2025-04-27",2025,"Q2",995,116,220,41,1372,"2025-05-15__de-us-20250515-q2-10q__105831.md","FS step-down: Bradesco 50% JV closed Q2 FY25",None),
 ("2025-07-27",2025,"Q3",1055,124,252,28,1459,"2025-08-14__de-us-20250814-q3-10q__155834.md","Q3 FY26 comparative base",None),
 ("2025-11-02",2025,"Q4",1256,133,259,32,1680,"2025-11-26__de-us-20251126-q4-10k__469216.md","derived FY-9M",None),
 ("2026-02-01",2026,"Q1",684,95,231,32,1042,"2026-02-19__de-us-20260219-q1-10q__648937.md","",None),
 ("2026-05-03",2026,"Q2",828,128,280,32,1268,"2026-05-21__de-us-20260521-q2-10q__1055929.md","matches verified matrix",None),
]
for pe,fy,fq,ppa,sat,cf,fs,tot,src,note,at in Q:
    for seg,val in (("PPA",ppa),("SAT",sat),("CF",cf),("FS",fs),("TOTAL",tot),("AT_COMBINED",at)):
        if val is None: continue
        add(series_id="de_rev606_latam", period_end=pe, fiscal_year=fy, fiscal_quarter=fq,
            geography="Latin America", country="", segment=seg, value=val, units="USDm",
            source_type="filing", source=CORP+src,
            notes=("revenue from contracts with customers (ASC 606 footnote), NOT segment net sales. "+note).strip())

# fiscal-year totals straight from the 10-K footnote
FY = [(2019,"2019-10-27",None,None,719,272,3885,"2019-11-27__de-us-20191127-q4-10k__469283.md",2894),
      (2020,"2020-11-01",1902,334,553,234,3023,"2021-11-24__de-us-20211124-q4-10k__131650.md",None),
      (2021,"2021-10-31",2916,456,903,247,4522,"2022-11-23__de-us-20221123-q4-10k__105816.md",None),
      (2022,"2022-10-30",4991,578,1467,303,7339,"2022-11-23__de-us-20221123-q4-10k__105816.md",None),
      (2023,"2023-10-29",5608,707,1429,453,8197,"2023-11-22__de-us-20231122-q4-10k__105844.md",None),
      (2024,"2024-10-27",3482,433,1170,453,5538,"2024-11-21__de-us-20241121-q4-10k__105810.md",None),
      (2025,"2025-11-02",4021,453,936,197,5607,"2025-11-26__de-us-20251126-q4-10k__469216.md",None)]
for fy,pe,ppa,sat,cf,fs,tot,src,at in FY:
    for seg,val in (("PPA",ppa),("SAT",sat),("CF",cf),("FS",fs),("TOTAL",tot),("AT_COMBINED",at)):
        if val is None: continue
        add(series_id="de_rev606_latam_fy", period_end=pe, fiscal_year=fy, fiscal_quarter="FY",
            geography="Latin America", country="", segment=seg, value=val, units="USDm",
            source_type="filing", source=CORP+src, notes="fiscal-year total, ASC 606 revenue-recognition footnote")

# ---------------------------------------------------------------- 2. FRED FX, averaged over Deere fiscal quarters
FQP = {("2024","Q3"):("2024-04-29","2024-07-28"),("2024","Q4"):("2024-07-29","2024-10-27"),
 ("2025","Q1"):("2024-10-28","2025-01-26"),("2025","Q2"):("2025-01-27","2025-04-27"),
 ("2025","Q3"):("2025-04-28","2025-07-27"),("2025","Q4"):("2025-07-28","2025-11-02"),
 ("2026","Q1"):("2025-11-03","2026-02-01"),("2026","Q2"):("2026-02-02","2026-05-03"),
 ("2026","Q3"):("2026-05-04","2026-08-02")}
FRED = {"DEXBZUS":("BRL per USD, daily noon rate","Brazil","fx_usdbrl_avg"),
        "DEXMXUS":("MXN per USD, daily noon rate","Mexico","fx_usdmxn_avg"),
        "DCOILBRENTEU":("USD per barrel, Brent","","brent_avg")}
def fred(sid):
    url=f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
    req=urllib.request.Request(url,headers={"User-Agent":"deere-latam-desk research cor@salomo.io"})
    d={}
    for r in csv.DictReader(io.StringIO(urllib.request.urlopen(req,timeout=60).read().decode())):
        v=list(r.values()); 
        try: d[v[0]]=float(v[1])
        except ValueError: pass
    return d
for sid,(unit,ctry,sname) in FRED.items():
    s=fred(sid)
    for (fy,fq),(a,b) in FQP.items():
        vals=[v for dt,v in s.items() if a<=dt<=b]
        if not vals: continue
        add(series_id=sname, period_end=b, fiscal_year=fy, fiscal_quarter=fq,
            geography="Latin America", country=ctry, segment="", value=round(statistics.mean(vals),4),
            units=unit, source_type="macro",
            source=f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid} (accessed 2026-08-16)",
            notes=f"mean of {len(vals)} daily obs over Deere fiscal quarter {a}..{b}")

# ---------------------------------------------------------------- 3. hand-keyed country / policy series
HAND = [
 # series_id, period_end, fy, fq, country, segment, value, units, source_type, source, notes
 ("br_crop_grain_total","2026-08-13",2026,"Q4","Brazil","",360.75,"million tonnes","macro",
  "https://www.otempo.com.br/agro/2026/8/13/conab-estima-safra-de-graos-de-360-8-milhoes-de-toneladas-em-2025-26 (2026-08-13)",
  "CONAB 11th survey, 2025/26 crop, record, +2.4% YoY; area 83.5m ha +2.1%"),
 ("br_crop_soybean","2026-08-13",2026,"Q4","Brazil","",180.5,"million tonnes","macro",
  "https://www.otempo.com.br/agro/2026/8/13/conab-estima-safra-de-graos-de-360-8-milhoes-de-toneladas-em-2025-26 (2026-08-13)",
  "CONAB 11th survey 2025/26 soybeans, record"),
 ("br_crop_corn_total","2026-08-13",2026,"Q4","Brazil","",142.96,"million tonnes","macro",
  "https://forbes.com.br/forbes-agro/2026/08/conab-eleva-projecao-recorde-para-safra-de-milho-do-brasil-em-25-26/ (2026-08)",
  "CONAB 2025/26 all-crop corn, record"),
 ("br_crop_corn_safrinha","2026-08-13",2026,"Q4","Brazil","",111.03,"million tonnes","macro",
  "https://forbes.com.br/forbes-agro/2026/08/conab-eleva-projecao-recorde-para-safra-de-milho-do-brasil-em-25-26/ (2026-08)",
  "second-crop (safrinha) corn 2025/26; vs 113.27 in 2024/25 per same source"),
 ("br_safrinha_harvest_pct_midjuly","2026-07-15",2026,"Q3","Brazil","",42.0,"percent harvested","macro",
  "https://www.farmprogress.com/commentary/market-forecast-brazil-calls-the-shots (2026-07, citing CONAB)",
  "vs 74% mid-July 2025 and 51% five-year average; heavy June rain delayed harvest -- falls inside Deere FQ3"),
 ("br_plano_safra_total","2026-06-30",2026,"Q3","Brazil","",525.1,"BRL billion","policy",
  "https://www.cnnbrasil.com.br/agro/governo-oficializa-plano-safra-2026-27-empresarial-de-r-5251-bilhoes/ (2026-06-30)",
  "Plano Safra 2026/27 commercial agriculture; +R$8.9bn / +1.72% nominal vs 2025/26 (R$516.2bn) = real-terms cut"),
 ("br_plano_safra_investimento","2026-06-30",2026,"Q3","Brazil","",140.2,"BRL billion","policy",
  "https://digital.agrishow.com.br/gesto/plano-safra-2026-27-veja-os-principais-pontos-anunciados-para-o-credito-rural/ (2026-07)",
  "investment tranche (the machinery-relevant bucket) vs R$101.5bn in 2025/26 = +38%"),
 ("br_plano_safra_custeio","2026-06-30",2026,"Q3","Brazil","",384.9,"BRL billion","policy",
  "https://digital.agrishow.com.br/gesto/plano-safra-2026-27-veja-os-principais-pontos-anunciados-para-o-credito-rural/ (2026-07)",
  "custeio + comercializacao vs R$414.7bn in 2025/26 = -7%"),
 ("br_moderfrota_alloc","2026-06-30",2026,"Q3","Brazil","",5.8,"BRL billion","policy",
  "https://digital.agrishow.com.br/gesto/plano-safra-2026-27-veja-os-principais-pontos-anunciados-para-o-credito-rural/ (2026-07)",
  "Moderfrota R$3.7bn @12.5% + Moderfrota Pronamp R$2.1bn @11.5%; one secondary source reports this as -54% YoY -- UNVERIFIED against primary MAPA text"),
 ("br_rate_custeio_empresarial","2026-06-30",2026,"Q3","Brazil","",12.5,"percent per annum","policy",
  "https://www.infomoney.com.br/politica/plano-safra-reduz-juros-para-ate-9-ao-ano-e-amplia-credito-para-r-525-bilhoes/ (2026-06/07)",
  "down from 14.0% in Plano Safra 2025/26; headline cut of up to 1.5pp; floor rate 8%, Pronamp cap 9%"),
 ("br_selic","2026-06-17",2026,"Q3","Brazil","",14.25,"percent per annum","macro",
  "https://agenciabrasil.ebc.com.br/economia/noticia/2026-06/copom-reduz-taxa-selic-para-1425-ao-ano (2026-06-17)",
  "third consecutive cut; from 14.50%; peak of cycle was 15.00%"),
 ("br_agmach_domestic_rev","2026-06-30",2026,"Q3","Brazil","",4.97,"BRL billion","industry",
  "https://www.cnnbrasil.com.br/agro/vendas-de-maquinas-agricolas-caem-mais-de-22-em-junho-diz-abimaq/ (2026-07)",
  "ABIMAQ June 2026 ag machinery sales, -22.3% YoY, +8.3% vs May; buyers waiting on Plano Safra rates"),
 ("br_agmach_domestic_rev_h1","2026-06-30",2026,"Q3","Brazil","",26.64,"BRL billion","industry",
  "https://www.cnnbrasil.com.br/agro/vendas-de-maquinas-agricolas-caem-mais-de-22-em-junho-diz-abimaq/ (2026-07)",
  "ABIMAQ H1 CY2026, -21.3% YoY; ABIMAQ keeps full-year -20% call"),
 ("br_agmach_units_q1cy26","2026-03-31",2026,"Q2","Brazil","",9.8,"thousand units","industry",
  "https://istoedinheiro.com.br/vendas-de-maquinas-agricolas-caem-13-no-1o-tri-na-comparacao-anual-diz-anfavea (2026-04)",
  "ANFAVEA Q1 CY2026 domestic ag machine sales, -13.1% YoY vs 11.3k"),
 ("br_agmach_units_fy_fcst","2026-12-31",2026,"FY","Brazil","",46.7,"thousand units","industry",
  "https://br.investing.com/news/world-news/anfavea-ve-queda-de-62-nas-vendas-de-maquinas-agricolas-no-brasil-em-2026-com-guerra-e-juros-altos-1898781 (2026-04)",
  "ANFAVEA CY2026 forecast, -6.2% YoY; cites Iran war fertilizer/freight costs and high rates"),
 ("br_agri_judicial_recovery","2026-03-31",2026,"Q2","Brazil","",474,"filings","industry",
  "https://www.canalrural.com.br/economia/recuperacao-judicial-no-agro-sobe-219-no-1o-trimestre-de-2026 (2026)",
  "Serasa Experian Q1 CY2026 agribusiness judicial-recovery filings, +21.9% YoY; rural producers as legal entities 196, +73.5%"),
 ("br_urea_price","2026-06-30",2026,"Q3","Brazil","",453,"USD per tonne","macro",
  "https://www.ifpri.org/blog/the-iran-war-farmers-in-brazil-and-argentina-face-rising-fertilizer-and-energy-prices/ (2026)",
  "urea spiked from ~USD400 to >USD850/t in April 2026 then fell back to USD453/t in June -- eased AFTER Deere's 21-May guide"),
 ("ar_crop_total","2026-05-22",2026,"Q3","Argentina","",163.2,"million tonnes","macro",
  "https://www.argentina.gob.ar/noticias/la-produccion-de-granos-alcanzo-una-cosecha-record-que-supero-las-163-millones-de-toneladas (2026-05)",
  "Secretaria de Agricultura: record 2025/26 crop, +21.25% YoY"),
 ("ar_crop_corn","2026-05-22",2026,"Q3","Argentina","",71.5,"million tonnes","macro",
  "https://www.argentina.gob.ar/noticias/la-produccion-de-maiz-marca-un-record-historico-con-715-millones-de-toneladas (2026-05)",
  "record; area 9.2m -> 11.6m ha (+26.1%), yield 6900 -> 7240 kg/ha"),
 ("ar_crop_soy","2026-05-22",2026,"Q3","Argentina","",49.9,"million tonnes","macro",
  "https://ruralnet.com.ar/cosecha-soja-argentina-2025-26-produccion-50-millones-toneladas/ (2026)",
  "2025/26 soybeans; average yield 32.3 qq/ha, second-best on record"),
 ("ar_export_tax_wheat","2026-06-03",2026,"Q3","Argentina","",5.5,"percent","policy",
  "https://www.fas.usda.gov/data/gain/2026/06/argentina-argentina-further-cuts-agricultural-export-taxes (2026-06)",
  "cut from 7.5%, effective June 2026 (announced 21 May, gazetted 3 June); soy stays 24% with gradual cuts only from Jan 2027"),
 ("ar_export_tax_soy","2026-06-03",2026,"Q3","Argentina","",24.0,"percent","policy",
  "https://www.fas.usda.gov/data/gain/2026/06/argentina-argentina-further-cuts-agricultural-export-taxes (2026-06)",
  "unchanged through the Deere FQ3 window; monthly step-downs promised from Jan 2027 to 21% by Dec 2027"),
]
for sid,pe,fy,fq,ctry,seg,val,unit,st,src,note in HAND:
    add(series_id=sid, period_end=pe, fiscal_year=fy, fiscal_quarter=fq, geography="Latin America",
        country=ctry, segment=seg, value=val, units=unit, source_type=st, source=src, notes=note)

# ---------------------------------------------------------------- 4. Deere Brazil operational facts
add(series_id="de_br_combine_output_cut", period_end="2026-07-31", fiscal_year=2026, fiscal_quarter="Q3",
    geography="Latin America", country="Brazil", segment="PPA", value=-30, units="percent",
    source_type="industry",
    source="https://agfeed.com.br/negocios/a-espera-da-recuperacao-john-deere-da-ferias-coletivas-e-layoff-a-trabalhadores-e-reduz-producao-no-rs/ (2026-02)",
    notes="Horizontina (combines/planters, RS): collective holidays from 12 Mar 2026, contract suspension (layoff) from 1 Apr for 2-5 months, up to 887 workers; ~30% cut to combine output over the period -- spans essentially all of Deere FQ3")
add(series_id="de_br_industry_retail_6m", period_end="2026-04-30", fiscal_year=2026, fiscal_quarter="Q2",
    geography="Latin America", country="Brazil", segment="PPA", value=-15, units="percent",
    source_type="transcript",
    source=CORP.replace("filings/","call-transcripts/")+"2026-05-21__de-us-20260521-call-qna__1042775.md",
    notes="management: Brazilian tractor+combine industry retail down ~15% over the first six months of FY2026; Deere down less than industry; small/mid tractors resilient, large tractors and combines down more")

with open(OUT,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=HDR); w.writeheader(); w.writerows(rows)
print("wrote",OUT,len(rows),"rows")
