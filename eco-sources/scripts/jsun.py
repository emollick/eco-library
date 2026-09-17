import re
_esc={'n':'\n','r':'\r','t':'\t','b':'\b','f':'\f','"':'"',"'":"'",'\\':'\\','/':'/'}
def js_unescape(s):
    out=[]; i=0; n=len(s)
    while i<n:
        c=s[i]
        if c=='\\' and i+1<n:
            d=s[i+1]
            if d=='u' and i+5<n: out.append(chr(int(s[i+2:i+6],16))); i+=6; continue
            if d=='x' and i+3<n: out.append(chr(int(s[i+2:i+4],16))); i+=4; continue
            out.append(_esc.get(d,d)); i+=2; continue
        out.append(c); i+=1
    return ''.join(out)
def dwr_html(t):
    m=re.search(r'html:"((?:[^"\\]|\\.)*)"', t)
    return js_unescape(m.group(1)) if m else None
