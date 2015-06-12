# -*- coding: utf-8 -*-
import re
from decimal import Decimal
import glob

'''
generuej warstwy po dociaganiu
potrzebne:
    plik wyciagniety z bazy
    plik zasysany do bazy

'''



class GenerujWarstwy(object):
    def __init__(self, dociag_File, raw_File, final_File):
        self.dociag_File = dociag_File
        self.out_File = self.dociag_File[:-4]+'_out.txt'
        self.in_File = self.out_File
        self.raw_File = raw_File
        self.final_File = final_File
        self.log_file = 'error_log.txt'
        
        
    def format_e(self,n, e_val):
        """
        input n as string and e_val as int
        retrun value in scientific notation with E=e_val as string
        or None when input parameters are incorrect
        """
        try:        
            int(e_val)
            x = Decimal(n)
            return str(x/pow(10, e_val))+'E+000'+str(e_val)
        except:
            return None
        
        
    def make_index(self, raw_list):
        """
        return index list as dic        
        """
           
        my_dic = {}
        for i, row in  enumerate(raw_list):
            my_dic[int(row.split(';')[0])] = i
        return my_dic
    
    
    def replace_xy(self, new_xy_list, row):
        """
        replace old xy to new xy
        return new row
        """
    
        n_x1, n_y1, n_x2, n_y2 = new_xy_list
        pattern = '\s+(\d+\.\d+E\+0006)'
        o_x1 = re.findall(pattern, row)[0]
        o_y1 =  re.findall(pattern, row)[1]
        o_x2 = re.findall(pattern, row)[2]
        o_y2 = re.findall(pattern, row)[3]
        row = row.replace(o_x1, n_x1)
        row = row.replace(o_x2, n_x2)
        row = row.replace(o_y2, n_y2)
        row = row.replace(o_y1, n_y1)
        return row
        
    def get_my_data_list(self):
        with open(self.dociag_File) as f:
            my_data_list = [ line.rstrip('\n').split(';')[:2] for line in f]
        return my_data_list
    
    
    def make_out_file(self):
        
        with open(self.out_File, 'w') as f:           
            for line in self.get_my_data_list():
                tmpval = ';'.join(re.split('\(+|\s|,|\)+', line[1])[1:-1])
    
                f.write(';'.join([line[0],tmpval])+'\n')
        
    def get_in_list(self):
        with open(self.in_File) as f:
            return [ line.rstrip('\n') for line in f]
        
        
    def get_raw_list(self):
        with open(self.raw_File) as f:
            return [ line.rstrip('\n') for line in f]
    
    def runApp(self):
        
        
        self.make_out_file()        
        index_dic = self.make_index(self.get_in_list())
        index_tem_list = index_dic.keys()
        in_list = self.get_in_list()        
        with open(self.final_File, 'w') as f:
            for i, raw_row in enumerate(self.get_raw_list()):
                element_index = int(raw_row.split(' ')[0])
                if element_index in index_tem_list:
                    
                    try:
                        split_in_row = in_list[index_dic[element_index]].split(';')
                        del index_dic[element_index]
                        x1 = self.format_e(split_in_row[2], 6)
                        y1 = self.format_e(split_in_row[1], 6)
                        x2 = self.format_e(split_in_row[4], 6)
                        y2 = self.format_e(split_in_row[3], 6)
                        f.write(re.sub('^\d+\s+', '',(self.replace_xy([x1,y1,x2,y2], raw_row)))+'\n')
                                        
                    except Exception as err:
                        f.write(re.sub('^\d+\s+', '', raw_row)+'\n')
                        print 'error', err, 'in', i
                        logfile = open(self.log_file, 'a')
                        logfile.write(raw_row+'\n')
                        logfile.close()
                        
                else:
                    f.write(re.sub('^\d+\s+', '', raw_row)+'\n') 
                    
if __name__ == '__main__':
    txt_list = glob.glob('*.txt')
    for i, file_name in enumerate(txt_list):
        print i+1, file_name
    plik_bazy = raw_input('podaj nr pliku z bazy')
    pli_zrodlowy = raw_input('podaj nr pliku zrodlowego')
    if pli_zrodlowy =='' and plik_bazy == '':
        plik_bazy = 'linie_dociagniete.txt'
        pli_zrodlowy = 'linie_temp.txt'
    else:
        try:
            plik_bazy = txt_list[int(plik_bazy)-1]
            pli_zrodlowy = txt_list[int(pli_zrodlowy)-1]
        except:
            raw_input('cos poszlo nie tak')
    print 'start z plikami %s (plik z bazy) oraz\n%s (plik zrodlowy)' % (plik_bazy,pli_zrodlowy)

    x = GenerujWarstwy(plik_bazy, pli_zrodlowy, 'warstwy_dociagniete.txt' )
    x.runApp()
    
    