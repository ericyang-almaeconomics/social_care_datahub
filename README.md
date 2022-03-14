# Social Care Datahub
## Background
This project will implement a simple web application using demographic/socioeconomic data from ONS as well as social care data from NHS Digital's Measures from the Adult Social Care Outcomes Framework and Skills for Care's workforce estimates. Using this web application, users can:
- Select a general theme (workforce demand or supply for services), choose a specific indicator and input a specific region. This will return a table with the selected indicator.
- Select a local authority (or region) and year. This will return a regional profile that provides background demographic/socioeconomic data (using the ONS API) as well as key social care indicators for the chosen year.
- Demographic indicators should include total population, qualifications and average income.
- View forecasted values (using a simple AR model) for the next three years for the indicators selected as inputs
- Download results for the selected inputs

## Key links
- NHS Digital data: https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-outcomes-framework-ascof/england-2020-21
- ONS API: https://developer.ons.gov.uk/
