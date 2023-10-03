
import pandas as pd

## PATH: locate file in file explorer, right-click>properties to find the path 
## data = pd.read_csv(r'PATH\filename.csv')

data = pd.read_csv(r'C:\Users\SnigdhaRamkumar\Downloads\Aegon_Drop2.csv') 

## DESTINATION: path where the json file should be written
## data.to_json('DESTINATION\JSON-File-Name.json',orient = 'records', lines = 'True')

data.to_json(r'C:\Users\SnigdhaRamkumar\Downloads\Aegon_JSONFile.json', orient = 'records', lines = 'True') 

print('Success!')