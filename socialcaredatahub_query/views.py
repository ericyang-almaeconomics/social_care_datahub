from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Output
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import xlwt
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
# Create your views here.

from .forms import UserInput




@login_required
def search(request):
    form = UserInput
    return render(request,'search.html', {'form':form})

@login_required
def results(request):
    if request.method=='POST':
        form = UserInput(request.POST)
        if form.is_valid:

            #check that only one of the fileds 'Local Authority', 'Region', 'England' is filled
            if (form['local_authority'].value() and not form['region'].value() and not form['england'].value()) or (not form['local_authority'].value() and form['region'].value() and not form['england'].value()) or (not form['local_authority'].value() and not form['region'].value() and form['england'].value()):
                if form['local_authority'].value():
                    geographical_description = form['local_authority'].value()
                elif form['region'].value():
                    geographical_description = form['region'].value()
                else:
                    geographical_description = ['England']
                years = form['year'].value()

                # check which fields have input in order to make the correct query
                if form['disaggregation'].value() and form['measure_group_description'].value():
                    disaggregation_level =  form['disaggregation'].value()
                    measure_group_description = form['measure_group_description'].value()
                    return_query = Output.objects.filter(geographical_description__in = geographical_description, year__in = years, disaggregation_level__in = disaggregation_level, measure_group_description = measure_group_description)
                elif form['disaggregation'].value() and  not form['measure_group_description'].value():
                    disaggregation_level =  form['disaggregation'].value()
                    return_query = Output.objects.filter(geographical_description__in = geographical_description, year__in = years, disaggregation_level__in = disaggregation_level) 
                elif not form['disaggregation'].value() and form['measure_group_description'].value():
                    measure_group_description = form['measure_group_description'].value()
                    return_query = Output.objects.filter(geographical_description__in = geographical_description, year__in = years, measure_group_description = measure_group_description)
                else:
                    return_query = Output.objects.filter(geographical_description__in = geographical_description, year__in = years)
                
                if return_query.count()>0:
                    return_query_df = pd.DataFrame.from_records(return_query.values())
                    graphs = []

                    #if the user chooses only one geographical area and only one year, we don't return any graphs
                    if len(years)>1 or len(geographical_description)>1:
                        
                        #we create a graph for every unique combination of [Measure Group Description, Disaggregation Level]
                        for measure_group in return_query_df['measure_group_description'].unique():
                            for disaggregation in return_query_df[return_query_df['measure_group_description']==measure_group]['disaggregation_level'].unique():
                                fig = go.Figure()
                                data = return_query_df[(return_query_df['measure_group_description']==measure_group) & (return_query_df['disaggregation_level']==disaggregation)]
                                data.sort_values(by=['year'],inplace=True, ignore_index=False)
                                #we create a Bar graph for every area through years
                                for area in data['geographical_description'].unique():
                                    fig.add_trace(
                                        go.Bar(
                                            name = area,
                                            x = data[data['geographical_description']==area]['year'].astype(str),
                                            y = data[data['geographical_description']==area]['measure_value'], 
                                        )  
                                    )
                                

                                #we group the Bar graphs for different areas for each combination [Measure Group Description, Disaggregation Level]
                                title = f'{measure_group}<br>Disaggregation: {disaggregation}'
                                fig.update_layout(width=1200,title = title, title_font_size = 15, title_x=0.5, barmode = 'group', bargap=0.25,bargroupgap=0.10)
                                fig.update_yaxes(title_text='Measure Value')
                                fig.update_xaxes(title_text='Year')
                                graphs.append(fig.to_html())
                                fig.data = []
                                fig.layout = {}


                    return render(request, 'results.html', {'results': return_query.values(), 'form':form, 'graphs':graphs})


                else:
                    messages.info(request, 'No results')
                    
                    return redirect('search')


            
            #if the user input is invalid we return the form with an error message
            else:
                
                messages.warning(request, 'You must fill in either only one of the fields Local Authority and Region or tick the England checkbox')
                return redirect('search')
    
    #if the user types the URL /results he/she gets redirected to the search page
    else:
        return redirect('search')


@login_required
def download_excel(request):
    if request.method=='POST':
        form = UserInput(request.POST)
  
        if form.is_valid:
            columns =[]

            #When the fields of the form are hidden, they return '['content','content']' instead of ['content','content']
            local_authority = [group.strip("''") for  group in form['local_authority'].value()[0].strip('][').split(', ')]
            if local_authority == ['']:
                    local_authority = []   

            region = [group.strip("''") for  group in form['region'].value()[0].strip('][').split(', ')]
            if region == ['']:
                    region = [] 
            
            disaggregation_level = [group.strip("''") for  group in form['disaggregation'].value()[0].strip('][').split(', ')]
            if disaggregation_level == ['']:
                    disaggregation_level = []
            
            
            measure_group_description = form['measure_group_description'].value().strip('][')
            if measure_group_description == ['']:
                    measure_group_description = [] 
            
            #check that only one of the fileds 'Local Authority', 'Region', 'England' is filled
            if (local_authority and not region and not form['england'].value()) or (not local_authority and region and not form['england'].value()) or (not local_authority and not region and form['england'].value()):
                if local_authority:
                    geographical_description = local_authority
                    columns.append('Local Authority')
                elif form['region'].value():
                    geographical_description = region
                    columns.append('Region')
                else:
                    geographical_description = ['England']
                    columns.append('Country')
                year = form['year'].value()
                
                
                if disaggregation_level and measure_group_description:
                    return_query = Output.objects.filter(geographical_description__in = geographical_description, year = year, disaggregation_level__in = disaggregation_level, measure_group_description = measure_group_description)
                elif disaggregation_level and  not measure_group_description:
                    return_query = Output.objects.filter(geographical_description__in = geographical_description, year = year, disaggregation_level__in = disaggregation_level) 
                elif not disaggregation_level and measure_group_description:
                    return_query = Output.objects.filter(geographical_description__in = geographical_description, year = year, measure_group_description = measure_group_description)
                else:
                    return_query = Output.objects.filter(geographical_description__in = geographical_description, year = year)
                
                
                
                columns.extend(['Year','Disaggregation','Measure Group Description','Measure Value','IMD - Average rank','Annual Pay Mean','Population'])

                #create an excel file as a response
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="report.xls"'
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet("sheet1")
                row_num = 0
                font_style = xlwt.XFStyle()
                # headers are bold
                font_style.font.bold = True

                #column header names, you can use your own headers here
                #write column headers in sheet
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)

                # Sheet body, remaining rows
                font_style = xlwt.XFStyle()
                
                
                for result in return_query.values():
                    row_num = row_num + 1
                    ws.write(row_num, 0, result['geographical_description'], font_style)
                    ws.write(row_num, 1, result['year'], font_style)
                    ws.write(row_num, 2, result['disaggregation_level'], font_style)
                    ws.write(row_num, 3, result['measure_group_description'], font_style)
                    ws.write(row_num, 4, result['measure_value'], font_style)
                    ws.write(row_num, 5, result['imd_average_rank'], font_style)
                    ws.write(row_num, 6, result['annual_pay_mean'], font_style)
                    ws.write(row_num, 7, result['population'], font_style)


                wb.save(response)
                return response
            
    else:
        return redirect('search')


            


