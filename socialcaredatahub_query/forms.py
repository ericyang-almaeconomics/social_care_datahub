from email.policy import default
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Field
from django.urls import reverse


    
REGION_SELECTION_CHOICES = (
    ('East Midlands', 'East Midlands'),
    ('East of England', 'East of England'),
    ('London', 'London'),
    ('North East', 'North East'),
    ('North West', 'North West'),
    ('South East', 'South East'),
    ('South West', 'South West'),
    ('West Midlands', 'West Midlands'),
    ('Yorkshire and the Humber', 'Yorkshire and the Humber')
)



LOCAL_AUTHORITY_SELECTION_CHOICES = (
    ('Barking and Dagenham', 'Barking and Dagenham'),
    ('Barnet', 'Barnet'),
    ('Barnsley', 'Barnsley'),
    ('Bath and North East Somerset', 'Bath and North East Somerset'),
    ('Bedford', 'Bedford'),
    ('Bexley', 'Bexley'),
    ('Birmingham', 'Birmingham'),
    ('Blackburn with Darwen', 'Blackburn with Darwen'),
    ('Blackpool', 'Blackpool'),
    ('Bolton', 'Bolton'),
    ('Bournemouth', 'Bournemouth'),
    ('Bournemouth, Christchurch and Poole','Bournemouth, Christchurch and Poole'),
    ('Bracknell Forest', 'Bracknell Forest'),
    ('Bradford', 'Bradford'),
    ('Brent', 'Brent'),
    ('Brighton and Hove', 'Brighton and Hove'),
    ('Bristol, City of', 'Bristol, City of'),
    ('Bromley', 'Bromley'),
    ('Buckinghamshire', 'Buckinghamshire'),
    ('Bury', 'Bury'),
    ('Calderdale', 'Calderdale'),
    ('Cambridgeshire', 'Cambridgeshire'),
    ('Camden', 'Camden'),
    ('Central Bedfordshire', 'Central Bedfordshire'),
    ('Cheshire East', 'Cheshire East'),
    ('Cheshire West and Chester', 'Cheshire West and Chester'),
    ('City of London', 'City of London'),
    ('Cornwall', 'Cornwall'),
    ('County Durham', 'County Durham'),
    ('Coventry', 'Coventry'),
    ('Croydon', 'Croydon'),
    ('Cumbria', 'Cumbria'),
    ('Darlington', 'Darlington'),
    ('Derby', 'Derby'),
    ('Derbyshire', 'Derbyshire'),
    ('Devon', 'Devon'),
    ('Doncaster', 'Doncaster'),
    ('Dorset', 'Dorset'),
    ('Dudley', 'Dudley'),
    ('Ealing', 'Ealing'),
    ('East Riding of Yorkshire', 'East Riding of Yorkshire'),
    ('East Sussex', 'East Sussex'),
    ('Enfield', 'Enfield'),
    ('Essex', 'Essex'),
    ('Gateshead', 'Gateshead'),
    ('Gloucestershire', 'Gloucestershire'),
    ('Greenwich', 'Greenwich'),
    ('Hackney', 'Hackney'),
    ('Halton', 'Halton'),
    ('Hammersmith and Fulham', 'Hammersmith and Fulham'),
    ('Hampshire', 'Hampshire'),
    ('Haringey', 'Haringey'),
    ('Harrow', 'Harrow'),
    ('Hartlepool', 'Hartlepool'),
    ('Havering', 'Havering'),
    ('Herefordshire, County of', 'Herefordshire, County of'),
    ('Hertfordshire', 'Hertfordshire'),
    ('Hillingdon', 'Hillingdon'),
    ('Hounslow', 'Hounslow'),
    ('Isle of Wight', 'Isle of Wight'),
    ('Isles of Scilly', 'Isles of Scilly'),
    ('Islington', 'Islington'),
    ('Kensington and Chelsea', 'Kensington and Chelsea'),
    ('Kent', 'Kent'),
    ('Kingston upon Hull, City of', 'Kingston upon Hull, City of'),
    ('Kingston upon Thames', 'Kingston upon Thames'),
    ('Kirklees', 'Kirklees'),
    ('Knowsley', 'Knowsley'),
    ('Lambeth', 'Lambeth'),
    ('Lancashire', 'Lancashire'),
    ('Leeds', 'Leeds'),
    ('Leicester', 'Leicester'),
    ('Leicestershire', 'Leicestershire'),
    ('Lewisham', 'Lewisham'),
    ('Lincolnshire', 'Lincolnshire'),
    ('Liverpool', 'Liverpool'),
    ('Luton', 'Luton'),
    ('Manchester', 'Manchester'),
    ('Medway', 'Medway'),
    ('Merton', 'Merton'),
    ('Middlesbrough', 'Middlesbrough'),
    ('Milton Keynes', 'Milton Keynes'),
    ('Newcastle upon Tyne', 'Newcastle upon Tyne'),
    ('Newham', 'Newham'),
    ('Norfolk', 'Norfolk'),
    ('North East Lincolnshire', 'North East Lincolnshire'),
    ('North Lincolnshire', 'North Lincolnshire'),
    ('North Somerset', 'North Somerset'),
    ('North Tyneside', 'North Tyneside'),
    ('North Yorkshire', 'North Yorkshire'),
    ('Northamptonshire', 'Northamptonshire'),
    ('Northumberland', 'Northumberland'),
    ('Nottingham', 'Nottingham'),
    ('Nottinghamshire', 'Nottinghamshire'),
    ('Oldham', 'Oldham'),
    ('Oxfordshire', 'Oxfordshire'),
    ('Peterborough', 'Peterborough'),
    ('Plymouth', 'Plymouth'),
    ('Poole', 'Poole'),
    ('Portsmouth', 'Portsmouth'),
    ('Reading', 'Reading'),
    ('Redbridge', 'Redbridge'),
    ('Redcar and Cleveland', 'Redcar and Cleveland'),
    ('Richmond upon Thames', 'Richmond upon Thames'),
    ('Rochdale', 'Rochdale'),
    ('Rotherham', 'Rotherham'),
    ('Rutland', 'Rutland'),
    ('Salford', 'Salford'),
    ('Sandwell', 'Sandwell'),
    ('Sefton', 'Sefton'),
    ('Sheffield', 'Sheffield'),
    ('Shropshire', 'Shropshire'),
    ('Slough', 'Slough'),
    ('Solihull', 'Solihull'),
    ('Somerset', 'Somerset'),
    ('South Gloucestershire', 'South Gloucestershire'),
    ('South Tyneside', 'South Tyneside'),
    ('Southampton', 'Southampton'),
    ('Southend-on-Sea', 'Southend-on-Sea'),
    ('Southwark', 'Southwark'),
    ('St. Helens', 'St. Helens'),
    ('Staffordshire', 'Staffordshire'),
    ('Stockport', 'Stockport'),
    ('Stockton-on-Tees', 'Stockton-on-Tees'),
    ('Stoke-on-Trent', 'Stoke-on-Trent'),
    ('Suffolk', 'Suffolk'),
    ('Sunderland', 'Sunderland'),
    ('Surrey', 'Surrey'),
    ('Sutton', 'Sutton'),
    ('Swindon', 'Swindon'),
    ('Tameside', 'Tameside'),
    ('Telford and Wrekin', 'Telford and Wrekin'),
    ('Thurrock', 'Thurrock'),
    ('Torbay', 'Torbay'),
    ('Tower Hamlets', 'Tower Hamlets'),
    ('Trafford', 'Trafford'),
    ('Wakefield', 'Wakefield'),
    ('Walsall', 'Walsall'),
    ('Waltham Forest', 'Waltham Forest'),
    ('Wandsworth', 'Wandsworth'),
    ('Warrington', 'Warrington'),
    ('Warwickshire', 'Warwickshire'),
    ('West Berkshire', 'West Berkshire'),
    ('West Sussex', 'West Sussex'),
    ('Westminster', 'Westminster'),
    ('Wigan', 'Wigan'),
    ('Wiltshire', 'Wiltshire'),
    ('Windsor and Maidenhead', 'Windsor and Maidenhead'),
    ('Wirral', 'Wirral'),
    ('Wokingham', 'Wokingham'),
    ('Wolverhampton', 'Wolverhampton'),
    ('Worcestershire', 'Worcestershire'),
    ('York', 'York')
)


DISAGGREGATION_CHOICES =(
    ("Total", "Total"),
    ("18-64", "18-64"),
    ("65 and over", "65 and over"),
    ("Male", "Male"),
    ("Female","Female")
)




YEAR_CHOICES = (
    ("2021",2021),
    ("2020",2020),
    ("2019",2019),
    ("2018",2018),
    ("2017",2017),
    ("2016",2016),
    ("2015",2015)
)

MEASURE_GROUP_SELECTION_CHOICES = (
    ('',''),
    ('Adjusted Social care-related quality of life – impact of Adult Social Care services','Adjusted Social care-related quality of life – impact of Adult Social Care services'),
    ('Carer-reported quality of life score','Carer-reported quality of life score'),
    ('Delayed transfers of care from hospital that are attributable to adult social care, per 100,000 population','Delayed transfers of care from hospital that are attributable to adult social care, per 100,000 population'),
    ('Delayed transfers of care from hospital which are jointly attributable to the NHS and adult social care per 100,000 population','Delayed transfers of care from hospital which are jointly attributable to the NHS and adult social care per 100,000 population'),
    ('Delayed transfers of care from hospital, per 100,000 population','Delayed transfers of care from hospital, per 100,000 population'),
    ('Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population','Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population'),
    ('Long-term support needs of younger adults (aged 18-64) met by admission to residential and nursing care homes, per 100,000 population','Long-term support needs of younger adults (aged 18-64) met by admission to residential and nursing care homes, per 100,000 population'),
    ('Overall satisfaction of carers with social services','Overall satisfaction of carers with social services'),
    ('Overall satisfaction of people who use services with their care and support','Overall satisfaction of people who use services with their care and support'),
    ('Proportion of adults in contact with secondary mental health services in paid employment','Proportion of adults in contact with secondary mental health services in paid employment'),
    ('Proportion of adults in contact with secondary mental health services who live independently, with or without support','Proportion of adults in contact with secondary mental health services who live independently, with or without support'),
    ('Proportion of adults with learning disabilities in paid employment','Proportion of adults with learning disabilities in paid employment'),
    ('Proportion of adults with learning disabilities who live in their own home or with their family','Proportion of adults with learning disabilities who live in their own home or with their family'),
    ('Proportion of people who use services who feel safe','Proportion of people who use services who feel safe'),
    ('Proportion of people who use services who have control over their daily life','Proportion of people who use services who have control over their daily life'),
    ('Proportion of people who use services who reported that they had as much social contact as they would like','Proportion of people who use services who reported that they had as much social contact as they would like'),
    ('Proportion of people who use services who say that those services have made them feel safe and secure','Proportion of people who use services who say that those services have made them feel safe and secure'),
    ('Proportion of those that received a short term service during the year where the sequel to service was either no ongoing support or support of a lower level','Proportion of those that received a short term service during the year where the sequel to service was either no ongoing support or support of a lower level'),
    ('Social care-related quality of life','Social care-related quality of life'),
    ('The proportion of carers who find it easy to find information about services','The proportion of carers who find it easy to find information about services'),
    ('The proportion of carers who receive direct payments','The proportion of carers who receive direct payments'),
    ('The proportion of carers who receive self-directed support','The proportion of carers who receive self-directed support'),
    ('The proportion of carers who report that they have been included or consulted in discussion about the person they care for','The proportion of carers who report that they have been included or consulted in discussion about the person they care for'),
    ('The proportion of carers who reported that they had as much social contact as they would like','The proportion of carers who reported that they had as much social contact as they would like'),
    ('The proportion of older people (aged 65 and over) who received reablement/rehabilitation services after discharge from hospital','The proportion of older people (aged 65 and over) who received reablement/rehabilitation services after discharge from hospital'),
    ('The proportion of older people (aged 65 and over) who were still at home 91 days after discharge from hospital into reablement/rehabilitation services','The proportion of older people (aged 65 and over) who were still at home 91 days after discharge from hospital into reablement/rehabilitation services'),
    ('The proportion of people who use services who find it easy to find information about support','The proportion of people who use services who find it easy to find information about support'),
    ('The proportion of people who use services who receive direct payments','The proportion of people who use services who receive direct payments'),
    ('The proportion of people who use services who receive self-directed support','The proportion of people who use services who receive self-directed support')
)

class UserInput(forms.Form):
    local_authority = forms.CharField(label = 'Local Authority', widget = forms.SelectMultiple(choices = LOCAL_AUTHORITY_SELECTION_CHOICES), required = False)
    region = forms.CharField(label = 'Region',widget = forms.SelectMultiple(choices = REGION_SELECTION_CHOICES), required = False)
    england = forms.BooleanField(required=False)
    year = forms.IntegerField(label= 'Year', widget = forms.SelectMultiple(choices = YEAR_CHOICES), required = True, initial = 2021)
    disaggregation = forms.ChoiceField(label = 'Disaggregation',choices=DISAGGREGATION_CHOICES, widget = forms.CheckboxSelectMultiple, required=False)
    measure_group_description = forms.CharField(label = 'Variable Name', widget=forms.Select(choices=MEASURE_GROUP_SELECTION_CHOICES),required=False)


#I tried this in order to place Local Authority and Region in the same row but it didn't work

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('results')
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        "local_authority",
                    ),
                    css_class="form-group col-lg-6",
                ),
                Column(
                    Field('region'),
                    css_class="form-group col-lg-6",
                )
            ),
            'england',
            'year',
            'disaggregation',
            'measure_group_description',
            Submit('submit','Search', css_id="search_button")
        )


