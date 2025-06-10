ABOUT
This folder contains scripts and instructions to create the various gss code lookups needed in the package and for testing.
This should be done every time a new code history database has been published by ONS (typically May and December)

Workflow of saving rds files from data and then saving all to sysdata.rda as a final step is following best practice suggested by jennybc here:
r-lib/usethis#1091


INSTRUCTIONS
When updating the code history data, the 1.'ChangeHistory.csv', 2.'Changes.csv' and 3.the date str on the database file from most recent ONS Code History Database download.
there is a when scrap tool in the firts script in data-raw in 1_package_data please update the url with the lastest version at the moment it is set tourl = "https://www.arcgis.com/sharing/rest/content/items/3acc892515aa49a8885c2deb734ebd3d/data"




then the script in data-raw can be ran into order to pull and process the lookups from 1 to 3

Run all R files in numerical order to create the internal package data that contains the code lookups and datasets for the testthat testing

Update the testthat tests to test on the latest code changes