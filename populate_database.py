import pandas as pd
import os
import django
from tqdm import tqdm
import numpy as np
import math 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialcaredatahub.settings')
django.setup()

from socialcaredatahub_query.models import Output

def main():
    final_data = pd.read_csv(r'Data/final_data.csv')

    for i,_ in tqdm(final_data.iterrows()):
        if not math.isnan(final_data.loc[i,'Population']):
            population = final_data.loc[i,'Population']
        else:
            population = None
        if not math.isnan(final_data.loc[i,'IMD - Average rank ']):
            imd_average_rank = final_data.loc[i,'IMD - Average rank ']
        else:
            imd_average_rank = None
        if not math.isnan(final_data.loc[i,'Annual Pay Mean']):
            annual_pay_mean = final_data.loc[i,'Annual Pay Mean']
        else:
            annual_pay_mean = None



        Output.objects.get_or_create(geographical_description = final_data.loc[i,'Geographical Description'], geographical_level = final_data.loc[i,'Geographical Level'], ons_code = final_data.loc[i,'ONS Code'], \
                        measure_group_description = final_data.loc[i,'Measure Group Description'], disaggregation_level = final_data.loc[i,'Disaggregation Level'],\
                        measure_value = final_data.loc[i,'Measure Value'], imd_average_rank = imd_average_rank, annual_pay_mean = annual_pay_mean,\
                        population = population)           

if __name__ == '__main__':
    main()