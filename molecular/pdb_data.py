import bpy
import requests
from . pdb_chain import Chain
import time
import zlib
import xml.etree.ElementTree as ET

class PDB_Data:
    __current__ = None

    def __init__(self, pdb_id):
       # self.initPDB(pdb_id)
        self.initXML(pdb_id)


    def initXML(self, pdb_id):
        PDB_Data.__current__ = self
        self.id = pdb_id

        def decompress_stream(stream):
            o = zlib.decompressobj(16 + zlib.MAX_WBITS)

            for chunk in stream:
                yield o.decompress(chunk)

            yield o.flush()

        r = requests.get('https://files.rcsb.org/download/'+pdb_id+'.xml.gz', stream=True)

        t = decompress_stream(r.iter_content(1024))

        xml = ''
        for l in t:
            xml += l.decode()


        root = ET.fromstring(xml)
        for site in root[0]:
            x = float(site[1].text)
            #print(x)
        
        
    def initPDB(self, pdb_id):
        PDB_Data.__current__ = self

        self.id = pdb_id
        self.compounds = {}
        self.chains = {}

        currentCmpnd = None
        pastCmpnd = False

        t = time.time()

        r = requests.get("https://files.rcsb.org/view/" + self.id + ".pdb", stream=True)
        for l in r.iter_lines():
            l = l.decode()
            if l[:4] == "HEAD":
                self.header = l[10:-30]
            elif l[:6] == "COMPND":
                i = -1
                if pastCmpnd:
                    i = -2
                pastCmpnd = True

                if l[9-i:15-i] == 'MOL_ID':
                    if currentCmpnd is not None:
                        self.compounds.update({currentCmpnd[0]: currentCmpnd[1:]})
                    currentCmpnd = [l[17-i:].split(';')[0]]
                
                elif l[11:17] == 'MOLECU':
                    currentCmpnd.append(l[21:].split(';')[0].split(',')[0])
                elif l[11:16] == 'CHAIN':
                    currentCmpnd.append([x[0] for x in l[18:].split(';')[0].split(', ')])
            elif pastCmpnd:
                pastCmpnd = False
                self.compounds.update({currentCmpnd[0]: currentCmpnd[1:]})
                for c in self.compounds:
                    for ch in self.compounds[c][1]:
                        ch = ch[0]
                        self.chains.update({ch:Chain(ch)})
                        self.chains[ch].compound = c
            elif l[:4] == "ATOM":
                d = [int(l[6:11]), l[12:16], l[16], l[17:20], l[21], int(l[22:26]), l[26], float(l[30:38]), float(l[38:46]), float(l[46:54]), float(l[54:60]), float(l[60:66]), l[72:76], l[76:78]]
                self.chains[d[4]].atoms.append(d)

       
        t2 = time.time()
        print('Loading data took ' + str(t2-t) + ' \n')