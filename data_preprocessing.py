import pandas as pd

MEASURE_GROUP_DESCRIPTION = {
'Proportion of adults in contact with secondary mental health services in paid employment' : 'The proportion of adults in contact with secondary mental health services in paid employment',
'Proportion of adults in contact with secondary mental health services who live independently, with or without support' : 'The proportion of adults in contact with secondary mental health services living independently, with or without support',
'Proportion of adults with learning disabilities in paid employment' : 'The proportion of adults with a learning disability in paid employment',
'Proportion of adults with learning disabilities who live in their own home or with their family' : 'The proportion of adults with a learning disability who live in their own home or with their family',
'Proportion of carers who receive direct payments' : 'The proportion of carers who receive direct payments',
'Proportion of carers who receive self-directed support' : 'The proportion of carers who receive self-directed support',
'Proportion of older people 65 and over who were still at home 91 days after discharge from hospital into reablement/rehabilitation services effectiveness of the service' :'The proportion of older people (aged 65 and over) who were still at home 91 days after discharge from hospital into reablement/rehabilitation services',
'Proportion of people using social care who receive direct payments' : 'The proportion of people who use services who receive direct payments',
'Proportion of people who use services who say that those services have made them feel safe and secure' : 'The proportion of people who use services who say that those services have made them feel safe and secure',
'Proportion of people who use services who feel safe' : 'The proportion of people who use services who feel safe',
'Proportion of people using social care who receive self-directed support' : 'The proportion of people who use services who receive self-directed support',
'Proportion of people who use services who have control over their daily life' : 'The proportion of people who use services who have control over their daily life',
'Long-term support needs of older adults aged 65 and over met by admission to residential and nursing care homes, per 100,000 population' : 'Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population',
'Long-term support needs of younger adults aged 18-64 met by admission to residential and nursing care homes, per 100,000 population' : 'Long-term support needs of younger adults (aged 18-64) met by admission to residential and nursing care homes, per 100,000 population',
'Delayed transfers of care from hospital, per 100,000 population' : 'Delayed transfers of care from hospital per 100,000 population',
'Delayed transfers of care from hospital that are attributable to adult social care, per 100,000 population' : 'Delayed transfers of care from hospital which are attributable to adult social care per 100,000 population',
'Delayed transfers of care from hospital that are jointly attributable to NHS and adult social care, per 100,000 population' : 'Delayed transfers of care from hospital which are jointly attributable to the NHS and adult social care per 100,000 population'
}


def calculate_outcome_manually(local_authority):
    if local_authority['Disaggregation Level'].isin(['Total','Male','Female','18-64','65 and over']).all():
        return local_authority[['Disaggregation Level','Measure Value']]
    numerator_sum = 0
    denominator_sum = 0
    outcome = {'Disaggregation Level': [], 'Measure Value': []}
    for index, item in local_authority['Disaggregation Level'].iteritems():
        if item in ['Total','Male','Female','18-64','65 and over']:
            outcome['Disaggregation Level'].append(item)
            outcome['Measure Value'].append(local_authority.loc[index,'Measure Value'])
        else:
            if local_authority.loc[index,'Measure Type'] == 'Numerator':
                numerator_sum += local_authority.loc[index,'Measure Value']
            else:
                denominator_sum += local_authority.loc[index,'Measure Value']
    outcome['Disaggregation Level'].append('65 and over')
    if denominator_sum!=0:
        outcome['Measure Value'].append(round(numerator_sum*100/denominator_sum, 2))
    else:
        outcome['Measure Value'].append(None)

    return pd.DataFrame(outcome)





def preprocess(nhs, population_persons, population_males, population_females, imd, annual_pay, year):
    print(year)
    #drop the columns we don't need
    nhs.drop(['Geographical Code','ASCOF Measure Code','Measure Group'], axis=1, inplace=True)

    #drop the rows that Geographical Level is equal to Council Type
    nhs.drop(nhs[(nhs['Geographical Level']=='Council Type') | (nhs['Geographical Level']=='Council type')].index, inplace=True)

    #drop the missing values from Measure Value
    nhs.dropna(subset = 'Measure Value', inplace=True)

    #Replace '64 and under' with '18-64' for compatibility reasons
    nhs['Disaggregation Level'].replace({'64 and under':'18-64'}, inplace=True)

    nhs.drop(nhs[~nhs['Measure Type'].isin(['Numerator','Denominator','Outcome'])].index , inplace=True)
    nhs.drop(nhs[nhs['Measure Type'].isin(['Numerator','Denominator']) & nhs['Disaggregation Level'].isin(['Total','Male','Female','18-64','65 and over'])].index, inplace=True)
    nhs.drop(nhs[nhs['Measure Type'].isin(['Outcome']) & ~nhs['Disaggregation Level'].isin(['Total','Male','Female','18-64','65 and over'])].index, inplace=True)

    nhs['Measure Value'] = nhs['Measure Value'].astype(float)
    nhs = nhs.groupby(['Geographical Description', 'Geographical Level','ONS Code','Measure Group Description']).apply(calculate_outcome_manually).reset_index()
    nhs.dropna(subset=['Measure Value'],inplace=True)
    nhs.drop(['level_4'],axis=1,inplace=True)

    #keep only the rows that Code exists in ONS Codes from NHS dataset
    population_persons.drop(population_persons[~population_persons['Code'].isin(nhs['ONS Code'])].index, inplace=True)
    population_males.drop(population_males[~population_males['Code'].isin(nhs['ONS Code'])].index, inplace=True)
    population_females.drop(population_females[~population_females['Code'].isin(nhs['ONS Code'])].index, inplace=True)


    #drop the columns that count the population between 0 and 17 years old
    if year!=2016:
        labels = ['Name','Geography','All ages']
    else:
        labels = ['Name','All ages']
    labels.extend([str(i) for i in range(18)])
    population_persons.drop( labels, axis=1, inplace=True)
    population_males.drop( labels, axis=1, inplace=True)
    population_females.drop( labels, axis=1, inplace=True)

    #sum the population size in two groups (18-64 and 65+) and keep only these two columns
    population_persons['Sum 18-64'] = population_persons.loc[:,[str(i) for i in range(18,65)]].sum(axis=1)
    population_persons['Sum 65 and over'] = population_persons.loc[:,[str(i) for i in range(65,90)]+['90+']].sum(axis=1)
    population_persons['Total'] = population_persons['Sum 18-64'] + population_persons['Sum 65 and over']
    population_persons.drop([str(i) for i in range(18,90)]+['90+'],axis=1,inplace=True)

    population_males['Total Males'] = population_males.loc[:,[str(i) for i in range(18,90)]+['90+']].sum(axis=1)
    population_females['Total Females'] = population_females.loc[:,[str(i) for i in range(18,90)]+['90+']].sum(axis=1)
    population_males.drop([str(i) for i in range(18,90)]+['90+'],axis=1,inplace=True)
    population_females.drop([str(i) for i in range(18,90)]+['90+'],axis=1,inplace=True)

    population = population_persons.merge(population_males, on = 'Code', how = 'outer')
    population = population.merge(population_females, on = 'Code', how = 'outer')

    annual_pay.dropna(inplace=True)
    annual_pay.drop(annual_pay[~annual_pay['Code'].isin(nhs['ONS Code'])].index, inplace=True)


    #create the final dataframe
    if year>=2019:
        final_data = nhs.merge(imd, left_on = 'ONS Code', right_on = 'Upper Tier Local Authority District code (2019)', how = 'left')
        final_data.drop(['Upper Tier Local Authority District code (2019)'], axis = 1,inplace=True)
    else:
        final_data = nhs.merge(imd, left_on = 'ONS Code', right_on = 'Upper Tier Local Authority District code (2013)', how = 'left')
        final_data.drop(['Upper Tier Local Authority District code (2013)'], axis = 1,inplace=True)

    
    final_data = final_data.merge(annual_pay, left_on = 'ONS Code', right_on = 'Code', how = 'left')
    final_data.drop(['Code'], axis = 1,inplace=True)
    final_data.rename(columns = {'Mean' : 'Annual Pay Mean'}, inplace=True)


    population_list = []
    for i, row in final_data.iterrows():
        if row['ONS Code'] in population['Code'].tolist():
            if row['Disaggregation Level']=='Total':
                population_list.append(population[population['Code']==row['ONS Code']]['Total'].iloc[0])
            elif row['Disaggregation Level']=='18-64':
                population_list.append(population[population['Code']==row['ONS Code']]['Sum 18-64'].iloc[0])
            elif row['Disaggregation Level']=='65 and over':
                population_list.append(population[population['Code']==row['ONS Code']]['Sum 65 and over'].iloc[0])
            elif row['Disaggregation Level']=='Male':
                population_list.append(population[population['Code']==row['ONS Code']]['Total Males'].iloc[0])
            else:
                population_list.append(population[population['Code']==row['ONS Code']]['Total Females'].iloc[0])
            
        else:
            population_list.append(None)
    final_data['Population'] = population_list
    final_data['Year'] = year

    final_data.replace({'x':None},inplace=True)

    return final_data


def main():
    #2021
    nhs = pd.read_excel(r"Data/2021/meas-from-asc-of-eng-2021-open-data-csv_v2.xlsx", na_values = ['[x]','[c]'])
    population_persons = pd.read_excel(r'Data/2021/ukpopestimatesmid2020on2021geography.xls', sheet_name = 'MYE2 - Persons', skiprows = range(7))
    population_males = pd.read_excel(r'Data/2021/ukpopestimatesmid2020on2021geography.xls', sheet_name = 'MYE2 - Males', skiprows = range(7))
    population_females = pd.read_excel(r'Data/2021/ukpopestimatesmid2020on2021geography.xls', sheet_name = 'MYE2 - Females', skiprows = range(7))
    imd = pd.read_excel(r'Data/2021/File_11_-_IoD2019_Local_Authority_District_Summaries__upper-tier__.xlsx', sheet_name = 'IMD', usecols = ['Upper Tier Local Authority District code (2019)','IMD - Average rank '])
    imd.rename(columns = {'IMD - Average rank ':'IMD - Average rank'},inplace=True)
    annual_pay = pd.read_excel(r'Data/2021/PROV - Home Geography Table 8.7a   Annual pay - Gross 2021.xls', sheet_name = 'All', skiprows = range(4),usecols=['Code','Mean'])
    final_data_2021 = preprocess(nhs, population_persons, population_males, population_females, imd, annual_pay, 2021)

    #2020
    nhs = pd.read_csv(r"Data/2020/meas-from-asc-of-eng-1920-open-data-csv.csv",encoding='cp1252', na_values = [':','c'])
    population_persons = pd.read_excel(r'Data/2020/ukpopestimatesmid2020on2021geography.xls', sheet_name = 'MYE2 - Persons', skiprows = range(7))
    population_males = pd.read_excel(r'Data/2020/ukpopestimatesmid2020on2021geography.xls', sheet_name = 'MYE2 - Males', skiprows = range(7))
    population_females = pd.read_excel(r'Data/2020/ukpopestimatesmid2020on2021geography.xls', sheet_name = 'MYE2 - Females', skiprows = range(7))
    imd = pd.read_excel(r'Data/2020/File_11_-_IoD2019_Local_Authority_District_Summaries__upper-tier__.xlsx', sheet_name = 'IMD', usecols = ['Upper Tier Local Authority District code (2019)','IMD - Average rank '])
    imd.rename(columns = {'IMD - Average rank ':'IMD - Average rank'},inplace=True)    
    annual_pay = pd.read_excel(r'Data/2020/Home Geography Table 8.7a   Annual pay - Gross 2020.xls', sheet_name = 'All', skiprows = range(4),usecols=['Code','Mean'])
    final_data_2020 = preprocess(nhs, population_persons, population_males, population_females, imd, annual_pay, 2020)

    #2019
    nhs = pd.read_csv(r"Data/2019/meas-from-asc-of-eng-1819-open-data-csv-v2.csv",encoding='cp1252', na_values = ['c'])
    nhs.rename(columns = {'ONS Area Code' : 'ONS Code'},inplace=True)
    population_persons = pd.read_excel(r'Data/2019/ukmidyearestimates20192020ladcodes.xls', sheet_name = 'MYE2 - Persons', skiprows = range(4))
    population_males = pd.read_excel(r'Data/2019/ukmidyearestimates20192020ladcodes.xls', sheet_name = 'MYE2 - Males', skiprows = range(4))
    population_females = pd.read_excel(r'Data/2019/ukmidyearestimates20192020ladcodes.xls', sheet_name = 'MYE2 - Females', skiprows = range(4))
    population_persons.rename(columns = {'Geography1' : 'Geography'},inplace=True)
    population_males.rename(columns = {'Geography1' : 'Geography'},inplace=True)
    population_females.rename(columns = {'Geography1' : 'Geography'},inplace=True)
    population_persons.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    population_males.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    population_females.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    imd = pd.read_excel(r'Data/2019/File_11_-_IoD2019_Local_Authority_District_Summaries__upper-tier__.xlsx', sheet_name = 'IMD', usecols = ['Upper Tier Local Authority District code (2019)','IMD - Average rank '])
    imd.rename(columns = {'IMD - Average rank ':'IMD - Average rank'},inplace=True)
    annual_pay = pd.read_excel(r'Data/2019/Home Geography Table 8.7a   Annual pay - Gross 2019.xls', sheet_name = 'All', skiprows = range(4),usecols=['Code','Mean'])
    final_data_2019 = preprocess(nhs, population_persons, population_males, population_females, imd, annual_pay, 2019)
    
    #2018
    nhs = pd.read_csv(r"Data/2018/meas-from-asc-of-17-18-open-data.csv",encoding='cp1252', na_values = [':','c'])
    nhs.rename(columns = {'ONS Area Code' : 'ONS Code'},inplace=True)
    population_persons = pd.read_excel(r'Data/2018/ukmidyearestimates20182019ladcodes.xls', sheet_name = 'MYE2-All', skiprows = range(4))
    population_males = pd.read_excel(r'Data/2018/ukmidyearestimates20182019ladcodes.xls', sheet_name = 'MYE2 - Males', skiprows = range(4))
    population_females = pd.read_excel(r'Data/2018/ukmidyearestimates20182019ladcodes.xls', sheet_name = 'MYE2 - Females', skiprows = range(4))
    population_persons.rename(columns = {'Geography1' : 'Geography'},inplace=True)
    population_males.rename(columns = {'Geography1' : 'Geography'},inplace=True)
    population_females.rename(columns = {'Geography1' : 'Geography'},inplace=True)
    population_persons.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    population_males.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    population_females.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    population_persons.rename(columns = {90:'90+'},inplace=True)
    population_males.rename(columns = {90:'90+'},inplace=True)
    population_females.rename(columns = {90:'90+'},inplace=True)
    imd = pd.read_excel(r'Data/2018/File_11_ID_2015_Upper-tier_Local_Authority_Summaries.xlsx', sheet_name = 'IMD', usecols = ['Upper Tier Local Authority District code (2013)','IMD - Average rank'])
    annual_pay = pd.read_excel(r'Data/2018/Home Geography Table 8.7a   Annual pay - Gross 2018.xls', sheet_name = 'All', skiprows = range(4),usecols=['Code','Mean'])
    final_data_2018 = preprocess(nhs, population_persons, population_males, population_females, imd, annual_pay, 2018)

    #2017
    nhs = pd.read_csv(r"Data/2017/meas-from-asc-of-1617-open-data-csv.csv",encoding='cp1252',low_memory=False)
    nhs.rename(columns = {'ONS Area Code' : 'ONS Code'},inplace=True)
    population_persons = pd.read_excel(r'Data/2017/ukmidyearestimates2017finalversion.xls', sheet_name = 'MYE2 - All', skiprows = range(4))
    population_males = pd.read_excel(r'Data/2017/ukmidyearestimates2017finalversion.xls', sheet_name = 'MYE2 - M', skiprows = range(4))
    population_females = pd.read_excel(r'Data/2017/ukmidyearestimates2017finalversion.xls', sheet_name = 'MYE2 - F', skiprows = range(4))
    population_persons.rename(columns = {'Geography1' : 'Geography'},inplace=True)
    population_males.rename(columns = {'Geography1' : 'Geography'},inplace=True)
    population_females.rename(columns = {'Geography1' : 'Geography'},inplace=True)
    population_persons.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    population_males.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    population_females.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    population_persons.rename(columns = {90:'90+'},inplace=True)
    population_males.rename(columns = {90:'90+'},inplace=True)
    population_females.rename(columns = {90:'90+'},inplace=True)
    imd = pd.read_excel(r'Data/2017/File_11_ID_2015_Upper-tier_Local_Authority_Summaries.xlsx', sheet_name = 'IMD', usecols = ['Upper Tier Local Authority District code (2013)','IMD - Average rank'])
    annual_pay = pd.read_excel(r'Data/2017/Home Geography Table 8.7a   Annual pay - Gross 2017.xls', sheet_name = 'All', skiprows = range(4),usecols=['Code','Mean'])
    final_data_2017 = preprocess(nhs, population_persons, population_males, population_females, imd, annual_pay, 2017)

    #2016
    nhs = pd.read_csv(r"Data/2016/2015-16 ASCOF open data csv file.csv",encoding='cp1252', na_values = ' ')
    nhs.rename(columns = {'ONS Area Code' : 'ONS Code'},inplace=True)
    population_persons = pd.read_excel(r'Data/2016/ukmidyearestimates2016.xls', sheet_name = 'MYE2 - All', skiprows = range(4))
    population_males = pd.read_excel(r'Data/2016/ukmidyearestimates2016.xls', sheet_name = 'MYE2 - M', skiprows = range(4))
    population_females = pd.read_excel(r'Data/2016/ukmidyearestimates2016.xls', sheet_name = 'MYE2 - F', skiprows = range(4))
    population_persons.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    population_males.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    population_females.rename(columns = {i:str(i) for i in range(90)},inplace=True)
    population_persons.rename(columns = {90:'90+'},inplace=True)
    population_males.rename(columns = {90:'90+'},inplace=True)
    population_females.rename(columns = {90:'90+'},inplace=True)
    imd = pd.read_excel(r'Data/2016/File_11_ID_2015_Upper-tier_Local_Authority_Summaries.xlsx', sheet_name = 'IMD', usecols = ['Upper Tier Local Authority District code (2013)','IMD - Average rank'])
    annual_pay = pd.read_excel(r'Data/2016/Home Geography Table 8.7a   Annual pay - Gross 2016.xls', sheet_name = 'All', skiprows = range(4),usecols=['Code','Mean'])
    final_data_2016 = preprocess(nhs, population_persons, population_males, population_females, imd, annual_pay, 2016)   


    final_data = pd.concat([final_data_2021, final_data_2020, final_data_2019, final_data_2018, final_data_2017, final_data_2016], ignore_index=True)
    final_data.replace(MEASURE_GROUP_DESCRIPTION, inplace = True)


    print(final_data.info(),'\n')
    print(final_data.head(10),'\n')
    print([(i,i) for i in final_data[final_data['Geographical Level']=='Council']['Geographical Description'].unique()],'\n')
    print([(i,i) for i in final_data[final_data['Geographical Level']=='Region']['Geographical Description'].unique()],'\n')
    print([(i,i) for i in final_data['Measure Group Description'].unique()],'\n')

    final_data.to_csv(r'Data/final_data.csv', index=False)
   



if __name__=='__main__':
    main()
