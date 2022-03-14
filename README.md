# Social Care Datahub
## Background
This project will implement a simple web application using demographic/socioeconomic data from ONS as well as social care data from NHS Digital's Measures from the Adult Social Care Outcomes Framework and Skills for Care's workforce estimates. 

## User stories
Using this web application, users can:
- Select a specific indicator (users should have the ability to choose more than one). This will return a table with the selected indicator aggregated to all of England.
- Select a local authority and year. This will return a profile that provides background demographic/socioeconomic data (using the ONS API) as well as key social care indicators for the chosen year.
- Demographic indicators should include total population, Index of Multiple Deprivation (average rank) and average annual pay.
- Download results for the selected inputs

## Features to implement later
- Allow users to select multiple years
- View forecasted values (using a simple AR model) for the next three years for the indicators selected as inputs
- Integrate results into a Plotly/Dash application so users can view graphs/charts as well

## Key links
- NHS Digital data: https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-outcomes-framework-ascof/england-2020-21
- ONS API: https://developer.ons.gov.uk/
