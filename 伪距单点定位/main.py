import re
s='APPROX_POSITION：  -2279828.8823,   5004706.5099,   3219777.4476  (m)'
part=re.compile(r'[-+]?\d*\.\d+')
l=part.findall(s)
print(l)