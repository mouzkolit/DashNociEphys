from physioweb.models import IpscMrna
import pandas as pd
import csv

def run():
    csv = pd.read_csv("all_mrna.csv")
    IpscMrna.objects.all().delete()
    for i in csv.itertuples():
        row = i[1:]
        ipsc = IpscMrna(GeneName = row[0],
                        sample_01 = row[1],
                        sample_02 = row[2],
                        sample_03 = row[3],
                        sample_04 = row[4],
                        sample_05 = row[5],
                        sample_06 = row[6],
                        sample_07 = row[7],
                        sample_08 = row[8],
                        sample_09 = row[9],
                        sample_10 = row[10],
                        sample_11 = row[11],
                        sample_12 = row[12],
                        sample_13 = row[13],
                        sample_14 = row[14],
                        sample_15 = row[15],
                        sample_16 = row[16],
                        sample_17 = row[17],
                        sample_18 = row[18],
                        sample_19 = row[19],
                        sample_20 = row[20],
                        sample_21 = row[21],
                        sample_22 = row[22],
                        sample_23 = row[23],
                        sample_24 = row[24],
                        sample_25 = row[25],
                        sample_26 = row[26],
                        sample_27 = row[27],
                        sample_28 = row[28],
                        sample_29 = row[29],
                        sample_30 = row[30],
                        sample_31 = row[31],
                        sample_32 = row[32],
                        sample_33 = row[33],
                        sample_34 = row[34],
                        sample_35 = row[35],
                        sample_36 = row[36],
                        sample_37 = row[37],
                        sample_38 = row[38],
                        sample_39 = row[39],
                        sample_40 = row[40],
                        sample_41 = row[41],
                        sample_42 = row[42],
                        sample_43 = row[43],
                        sample_44 = row[44],
                        sample_45 = row[45],
                        sample_46 = row[46],
                        sample_47 = row[47],
                        sample_48 = row[48],
                        sample_49 = row[49],
                        sample_50 = row[50],
                        sample_51 = row[51],
                        sample_52 = row[52],
                        sample_53 = row[53],
                        sample_54 = row[54])
   
        ipsc.save()

