
import os
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
from wand.api import library

import gc
import re


import ctypes
#from wand.image import Image


class word_search_engine():
    
    def find_inn(self,txt):
        self.txt=txt
        i=0
        inn=''
        for txtpart in self.txt:
            for accrloc in self.find_all(txtpart.lower(), 'инн'):
                if accrloc>0:
                    innm = re.findall('\d{10}', txtpart[accrloc:accrloc+50])
                    if len(innm)>1:
                        inn = innm[1]
                    if len(innm)>0:
                        inn = innm[0]
                    #print(i)
                i+=1
        return inn

    def find_depo(self,txt):
        self.txt=txt
        i=0
        accr= []
        page_depo = []
        cntc = 0
        strg = []
        for txtpart in self.txt:
            cntc+=1
            for accrloc in self.find_all(txtpart.lower(), 'депозит'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+150])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_depo.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30])
            i+=1
        return accr, page_depo, strg

    def find_all(self,a_str, sub):
        self.a_str=a_str
        self.sub=sub
        
        start = 0
        while True:
            start = self.a_str.lower().find(self.sub.lower(), start)
            if start == -1: return
            yield start
            start += len(self.sub)


    def find_rs(self,txt):
        self.txt=txt
        
        i=0
        accr = []
        page_rs = []
        cntc = 0
        strg = []
        for txtpart in self.txt:
            cntc+=1
            for accrloc in self.find_all(txtpart.lower(), 'расчетные счета'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+150])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_rs.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30])
            for accrloc in self.find_all(txtpart.lower(), 'текущие счета'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+150])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_rs.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30])
            for accrloc in self.find_all(txtpart.lower(), 'расчетных счетах'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+150])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_rs.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30])
            for accrloc in self.find_all(txtpart.lower(), 'текущих счетах'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+150])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_rs.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30])
            for accrloc in self.find_all(txtpart.lower(), 'денежные эквиваленты'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+150])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_rs.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30])
            for accrloc in self.find_all(txtpart.lower(), 'касс'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+150])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_rs.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30])
        return accr, page_rs, strg


    def find_gar(self,txt):
        self.txt=txt
        
        i=0
        gar= []
        page_gar = []
        cntc = 0
        strg = []
        for txtpart in self.txt:
            cntc+=1
            for accrloc in self.find_all(txtpart.lower(), 'гаран'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+50])
                    cnt = int(len(accrm)/3)
                    gar.append(''.join(accrm[0:cnt]))
                    page_gar.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30])
            i+=1
        return gar, page_gar, strg


    def find_por(self,txt):
        
        self.txt=txt
        
        i=0
        accr= []
        page_accr = []
        cntc = 0
        strg = []
        for txtpart in self.txt:
            cntc+=1
            for accrloc in self.find_all(txtpart.lower(), 'обеспечение обязательств'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+50])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_accr.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30]) 
            for accrloc in self.find_all(txtpart.lower(), 'поручительства по обязательств'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+50])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_accr.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30])
            for accrloc in self.find_all(txtpart.lower(), '5800'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+50])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_accr.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30]) 
        return accr, page_accr, strg


    def find_accr(self,txt):
        
        self.txt=txt
        
        i=0
        accr= []
        page_accr = []
        cntc = 0
        strg = []
        for txtpart in self.txt:
            cntc+=1
            for accrloc in self.find_all(txtpart.lower(), 'аккре'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+50])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_accr.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30]) 
            i+=1
        return accr, page_accr, strg


    def find_debit(self,txt):
        
        self.txt=txt
        
        accr= []
        page_accr = []
        cntc = 0
        strg = []
        for txtpart in self.txt:
            cntc+=1
            for accrloc in self.find_all(txtpart.lower(), 'авансы выданные'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+50])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_accr.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30]) 
            for accrloc in self.find_all(txtpart.lower(), 'прочая задолж'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+50])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_accr.append(cntc)        
                    strg.append(txtpart[accrloc-30:accrloc+30]) 
            for accrloc in self.find_all(txtpart.lower(), 'прочая дебиторская'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+50])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_accr.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30]) 
            for accrloc in self.find_all(txtpart.lower(), 'прочие дебитор'):
                if accrloc>0:
                    accrm = re.findall('\d+', txtpart[accrloc:accrloc+50])
                    cnt = int(len(accrm)/3)
                    accr.append(''.join(accrm[0:cnt]))
                    page_accr.append(cntc)
                    strg.append(txtpart[accrloc-30:accrloc+30]) 
        return accr, page_accr, strg
        
        
        
