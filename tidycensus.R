# Install required packages if not already installed
if (!require("tidycensus")) install.packages("tidycensus")

# Set your Census API key (replace "YOUR_API_KEY" with your actual key)
#Acquire here https://api.census.gov/data/key_signup.html
census_api_key("Census_API_Key")

# Specify variables
geography <- "block group"
variables <- c("vari_ables")
state <- "ST"
county <- "County"
year <- 2020

###Run these lines if you are not sure what variable names you need to use
# vars <- load_variables(2020, "dhc")
# print(vars)
# write.csv(vars, file = "out_path")


# Specify desired data
library(tidycensus)
census_data <- get_decennial(
  geography = geography,
  variables = variables,
  state = state,
  county = county,
  year = year,
  summary_var = "P1_001",  # We're retrieving data from Summary File 1
  summary_file = "sf1"     # Decennial SF1 data
)

# Explore the data
head(census_data)

# Save data
write.csv(census_data, file = "out_path", row.names = TRUE)