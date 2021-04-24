
import os
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
from wand.api import library
import gc
import ctypes


import pandas as pd
import numpy as np
import time
import glob
import pickle



#инициализируем объект для парсинга        
obrabotka_pdf_object=obrabotka_pdf()



#предполагается, что все pdf лежат в одной папке, с помощью glob вытаскиваем их и добавляем в list_df. 
path='nikita/1904_01/pdf/*.pdf'

list_df=glob.glob(path)



#название выходного файла с текстами, содержание : inn,txt_pdfminer,txt_pdfminer_count,txt_pdfminer_full_count, txt_tesseract,txt_tesseract_count,txt_tesseract_full_count
df_tmp_name='your_name.pickle'

#название выходного файла с логами
df_tmp_time_name='your_name2.pickle'

#используем пдфмайнер? True or False
pdfminer_status=True

#используем тессеракт? True or False
tesseract_status=True


#вызов метода для перевода пдф в текст
df_with_txt,df_with_log=obrabotka_pdf_object.Get_text_from_image_aggregator(list_df,df_tmp_name,df_tmp_time_name,pdfminer_status,tesseract_status)


#Каждый новый обработанный пдф сразу же сгружается в df_tmp_name, формата .pickle. Это работает очень быстро и почти не влияет на производительность.
#Дополнительно оно выгружается в переменную df_with_txt. 
#мы можем сразу же находить нужные нам ключевые слова, а можем подождать окончания работы метода.









#Загружаем наш файл для нахождения ключевых слов

#логи
path='nikita/1904_01/pickle\\1904_01_time.pickle'
with open(path,'rb') as f:
    df_with_log=pickle.load(f)
   

#инн и текст
path='nikita/1904_01/pickle\\1904_01.pickle'
with open(path,'rb') as f:
    df_with_txt=pickle.load(f)
    
    
#инициализируем класс поиска ключевых слов
word_search_engine_object=word_search_engine()


#можно посмотреть какие методы доступны. Исключаем вспомогательные методы
list_of_method=['word_search_engine_object.'+x for x in dir(word_search_engine_object) if (x[:1]!='_') and x!='find_all' and x!='find_por']
list_of_method



#Вызываем методы и записываем результаты в этот же фрейм. Ниже вариант и с пдфмайнером и с тессерактом


df_with_txt['tesseract_accr']=df_with_txt['list_txt_tesseract'].apply(word_search_engine_object.find_accr)
df_with_txt['tesseract_debit']=df_with_txt['list_txt_tesseract'].apply(word_search_engine_object.find_debit)
df_with_txt['tesseract_depo']=df_with_txt['list_txt_tesseract'].apply(word_search_engine_object.find_depo)
df_with_txt['tesseract_gar']=df_with_txt['list_txt_tesseract'].apply(word_search_engine_object.find_gar)
df_with_txt['tesseract_inn']=df_with_txt['list_txt_tesseract'].apply(word_search_engine_object.find_inn)
df_with_txt['tesseract_por']=df_with_txt['list_txt_tesseract'].apply(word_search_engine_object.find_por)
df_with_txt['tesseract_rs']=df_with_txt['list_txt_tesseract'].apply(word_search_engine_object.find_rs)



df_with_txt['pdfminer_accr']=df_with_txt['list_txt_pdfminer'].apply(word_search_engine_object.find_accr)
df_with_txt['pdfminer_debit']=df_with_txt['list_txt_pdfminer'].apply(word_search_engine_object.find_debit)
df_with_txt['pdfminer_depo']=df_with_txt['list_txt_pdfminer'].apply(word_search_engine_object.find_depo)
df_with_txt['pdfminer_gar']=df_with_txt['list_txt_pdfminer'].apply(word_search_engine_object.find_gar)
df_with_txt['pdfminer_inn']=df_with_txt['list_txt_pdfminer'].apply(word_search_engine_object.find_inn)
df_with_txt['pdfminer_por']=df_with_txt['list_txt_pdfminer'].apply(word_search_engine_object.find_por)
df_with_txt['pdfminer_rs']=df_with_txt['list_txt_pdfminer'].apply(word_search_engine_object.find_rs)



#отбираем нужные нам столбцы и выгружаем
list_export_columns=[x for x in df_with_txt.columns if x=='inn' or x.startswith('pdfminer') or x.startswith('tesseract')]


#выгружаем в эксель
path='tmp.xlsx'
df_with_txt[list_export_columns].to_excel(path,index=False)