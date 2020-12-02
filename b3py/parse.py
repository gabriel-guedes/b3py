import json
with open('./b3py/filemap.json', 'r') as fp:
    filemap = json.load(fp)

def get_values(raw: str)->dict:
    values = {}
    for key in filemap:
        begin = filemap[key]['begin']
        end = filemap[key]['end']
        value = raw[begin:end].strip()
        if filemap[key]['type'] == 'float' and value:
            value = float(value)/100
        elif filemap[key]['type'] == 'integer' and value:
            value = int(value)
        
        values.update({key: value})
    
    return values