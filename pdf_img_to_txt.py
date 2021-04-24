
import os
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
from wand.api import library

import gc



import ctypes
#from wand.image import Image



class obrabotka_pdf():

    
    library.MagickNextImage.argtypes = [ctypes.c_void_p]
    library.MagickNextImage.restype = ctypes.c_int



    from wand.resource import limits

    # Use 100MB of ram before writing temp data to disk.
    limits['memory'] = 1024 * 1024 * 100

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"


    # pdf = wi(filename = "Downloads/НК Роснефть_РСБУ_2020.pdf", resolution = 300)
    # pdfImg=pdf.convert('jpeg')

    imgBlobs=[]
    extracted_text=[]

    def Get_text_from_image(self,pdf_path):
        
        self.pdf_path=pdf_path
        
        pdf=wi(filename=self.pdf_path,resolution=300)
        pdfImg=pdf.convert('jpeg')
        imgBlobs=[]
        extracted_text=[]
        try:
            for img in pdfImg.sequence:
                page=wi(image=img)
                imgBlobs.append(page.make_blob('jpeg'))
        finally:
            pdfImg.destroy()

        for imgBlob in imgBlobs:
            im=Image.open(io.BytesIO(imgBlob))
            text=pytesseract.image_to_string(im,lang='rus')
            extracted_text.append(text)

        return (extracted_text)


    def extract_text_by_page(self,pdf_path):
        
        self.pdf_path=pdf_path
        
        with open(self.pdf_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh, 
                                          caching=True,
                                          check_extractable=True):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(resource_manager, fake_file_handle)
                page_interpreter = PDFPageInterpreter(resource_manager, converter)
                page_interpreter.process_page(page)
     
                text = fake_file_handle.getvalue()
                yield text
     
                # close open handles
                converter.close()
                fake_file_handle.close()

                
    def extract_text(self,pdf_path):
        
        self.pdf_path=pdf_path
        
        pdf_txt=[]
        for page in self.extract_text_by_page(self.pdf_path):
            pdf_txt.append(page)
        return pdf_txt




    
    def Get_text_from_image_aggregator(self,list_df,df_tmp_name,df_tmp_time_name,pdfminer_status,tesseract_status):


        self.list_df=list_df
        self.df_tmp_name=df_tmp_name
        self.df_tmp_time_name=df_tmp_time_name

        self.pdfminer_status=pdfminer_status
        self.tesseract_status=tesseract_status

        list_inn=[]
        list_txt_pdfminer=[]
        list_txt_pdfminer_count=[]
        list_txt_pdfminer_full_count=[]
        list_txt_tesseract=[]
        list_txt_tesseract_count=[]
        list_txt_tesseract_full_count=[]


        list_time_operation=[]
        list_time_sec=[]
        list_time_ns=[]
        list_time_inn=[]


        #df_tmp_name='name_file22.pickle'
        #df_tmp_time_name='name_time.pickle'

        for index,tmp_file in enumerate(self.list_df):



            

            inn=tmp_file[-14:-4]

            list_time_operation.append('iteration start')
            list_time_sec.append(time.time())
            list_time_ns.append(time.time_ns())
            list_time_inn.append(inn)



            list_inn.append(inn)

            list_time_operation.append('pdf_miner start')
            list_time_sec.append(time.time())
            list_time_ns.append(time.time_ns())
            list_time_inn.append(inn)

            if (self.pdfminer_status):
                try:
                    txt_pdfminer=self.extract_text(tmp_file)
                    #txt_pdfminer = pdfminer.high_level.extract_text(tmp_file)
                except:
                    txt_pdfminer='error'
            else:
                txt_pdfminer='disabled'

            list_time_operation.append('pdf_miner end')
            list_time_sec.append(time.time())
            list_time_ns.append(time.time_ns())
            list_time_inn.append(inn)

            #print('pdfminer finish')

            list_txt_pdfminer.append(txt_pdfminer)
            list_txt_pdfminer_count.append(len(txt_pdfminer))
            list_txt_pdfminer_full_count.append(len("".join(map(str,txt_pdfminer))))


            list_time_operation.append('tesseract start')
            list_time_sec.append(time.time())
            list_time_ns.append(time.time_ns())
            list_time_inn.append(inn)

            if (self.tesseract_status):
                try:
                    txt_tesseract = self.Get_text_from_image(tmp_file)
                except:
                    txt_tesseract='error'
            else:
                txt_tesseract='disabled'


            list_time_operation.append('tesseract end')
            list_time_sec.append(time.time())
            list_time_ns.append(time.time_ns())
            list_time_inn.append(inn)


            list_txt_tesseract.append(txt_tesseract)
            list_txt_tesseract_count.append(len(txt_tesseract))
            list_txt_tesseract_full_count.append(len("".join(map(str,txt_tesseract))))


            list_time_operation.append('we create df')
            list_time_sec.append(time.time())
            list_time_ns.append(time.time_ns())
            list_time_inn.append(inn)


            df_tmp=pd.DataFrame(zip(list_inn
                                    ,list_txt_pdfminer
                                    ,list_txt_pdfminer_count
                                    ,list_txt_pdfminer_full_count
                                    ,list_txt_tesseract
                                    ,list_txt_tesseract_count
                                    ,list_txt_tesseract_full_count
                                   )
                                ,columns=['inn'
                                          ,'list_txt_pdfminer'
                                          ,'list_txt_pdfminer_count'
                                          ,'list_txt_pdfminer_full_count'
                                          ,'list_txt_tesseract'
                                          ,'list_txt_tesseract_count'
                                          ,'list_txt_tesseract_full_count'])


            list_time_operation.append('df is created')
            list_time_sec.append(time.time())
            list_time_ns.append(time.time_ns())
            list_time_inn.append(inn)



            with open(self.df_tmp_name,'wb') as f:
                pickle.dump(df_tmp,f)

            list_time_operation.append('dump is finish')
            list_time_sec.append(time.time())
            list_time_ns.append(time.time_ns())
            list_time_inn.append(inn)


            df_tmp_time=pd.DataFrame(zip(list_time_operation
                                        ,list_time_sec
                                        ,list_time_ns
                                        ,list_time_inn
                                        )
                                    ,columns=['list_time_operation'
                                              ,'list_time_sec'
                                              ,'list_time_ns'
                                              ,'list_time_inn'])


            with open(self.df_tmp_time_name,'wb') as f:
                pickle.dump(df_tmp_time,f)
        return df_tmp,df_tmp_time

    

        
        
        
        
