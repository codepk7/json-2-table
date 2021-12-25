import pandas as pd
from pandas.core.indexes.base import Index
import sys
from pathlib import Path, PurePath

#Check if all the argument are passed
if len(sys.argv) != 3:
    sys.exit("Usage: python3 [path to your program] [input file path] [output file path]")


json_file_name = sys.argv[1]
output_file_name = Path(sys.argv[2])
output_dir = output_file_name.parent

#Check if the input file exists
if not Path(json_file_name).is_file():
    sys.exit("Input Json file doesn't exist")

# #Check if the output directory exists, else create it
if not output_dir.is_dir() & output_dir.exists():
    output_dir.mkdir()
    print("Created output directory: ",str(output_dir))

#Create output file
output_file_name.touch(exist_ok=True)


#Read the input json file
df = pd.read_json(json_file_name)

#Create dataframes for Toppings and Batter
result_toppings = pd.json_normalize(df['items']['item'], 'topping',["id","name","type"],record_prefix='_')
result_batter = pd.json_normalize(df['items']['item'],['batters','batter'],["id","name","type"],record_prefix='_')

#Drop the columns which are not needed and rename the Columns
result_toppings.drop("_id",axis=1,inplace=True)
result_toppings.rename(columns = {'_type':'Topping','id':'Id','type':'Type','name':'Name'}, inplace = True)

result_batter.drop("_id",axis=1,inplace=True)
result_batter.rename(columns = {'_type':'Batter','id':'Id','type':'Type','name':'Name'}, inplace = True)


#Merge the dataframes
result = pd.merge(result_batter,result_toppings, on=['Id','Name','Type'])

#Re-order the columns as specified in the example and set index as needed
result = result.reindex(columns=['Id', 'Type', 'Name', 'Batter', 'Topping'])
result = result.set_index(['Id'])

#Output to the dataframe to csv file
result.to_csv(output_file_name)
print("Output at: ", str(Path(output_file_name).resolve()))