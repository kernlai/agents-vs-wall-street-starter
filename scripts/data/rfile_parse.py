import re,html,os,json
def parse_rfile(path):
    t=open(path,encoding='utf-8',errors='ignore').read()
    tbl=re.search(r'<table[^>]*>.*?</table>',t,re.S)
    if not tbl: return None,None,[]
    seg=tbl.group(0)
    rows=[]
    for r in re.findall(r'<tr.*?</tr>',seg,re.S):
        cells=[]
        for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>',r,re.S):
            x=html.unescape(re.sub(r'<[^>]+>',' ',c))
            x=x.replace('\xa0',' ').replace('​','')
            x=re.sub(r'\s+',' ',x).strip()
            cells.append(x)
        rows.append(cells)
    return seg,None,rows
def num(s):
    s=s.strip()
    # older R files append the XBRL element name after the value
    m=re.match(r'^(\(?\$?\s*-?[\d,]+(?:\.\d+)?\)?)\s*(?:[a-zA-Z][\w\-]*_\w+.*)?$',s)
    if m: s=m.group(1).strip()
    if s in ('','$'): return None
    neg = s.startswith('(') and s.endswith(')')
    s=s.strip('()').replace('$','').replace(',','').replace('%','').strip()
    if not re.fullmatch(r'-?\d+(\.\d+)?',s): return None
    v=float(s)
    return -v if neg else v
if __name__=='__main__':
    import sys
    _,_,rows=parse_rfile(sys.argv[1])
    for r in rows:
        r=[c for c in r if c!='']
        if r: print(r)
