import json
from bs4 import BeautifulSoup
import requests

def html_parser(html_file):
    try:
        with open(html_file, "r") as html_file:
            file= BeautifulSoup(html_file, "html.parser")
        return file
    except Exception as e:
        return (f"Error in parsing HTML file:{e}")

data = []

def table_count(html_content):
    num_tables= len(html_content.find_all("table"))
    return num_tables
             
def data_extractor(table_num,html_content):
    try:
        tables=html_content.find_all("table")
        table=tables[table_num]
        trs=table.find_all("tr")
        data=[]
        for tr in trs[1:]:
            try:
                tds=tr.find_all("td")
                if len(tds) == 6:
                    metabolic_profile = str(tds[0].text.strip())
                    rA = float(tds[1].text.strip())
                    range_value = str(tds[2].text.strip())
                    remarks = str(tds[3].text.strip())
                    curation = str(tds[4].text.strip())
                    recommendation = str(tds[5].text.strip())
                    data.append({
                                    "metabolicProfile": metabolic_profile,
                                    "rA": rA,
                                    "range": range_value,
                                    "remarks": remarks,
                                    "curation": curation,
                                    "recommendation": recommendation
                                })
            except IndexError as e:
                print("Error in td of html file") 
        return data
    except Exception as e:
        return (f"Error in data extraction from html file:{e}")       
    
def html_to_json(json_file_path, final_data):
    try:
        with open(json_file_path, 'w') as json_file:
            return json.dump(final_data, json_file, indent=2)
    except Exception as e:
        return (f"Error in convertion to json:{e}")
    
     

def main():
    try:
        global scfa_data, gut_brain_data, gas_data, lipid_data, metabolism_data, vitamin_data
        html_file_path = (r"C:\Users\shaima_ahmed\Documents\Pipeline_Optimisation\Function_NB04_000246723.html")
        html_content = html_parser(html_file_path)
        tab= table_count(html_content)
        for table_num in list(range(tab)):
            if table_num==0:
                scfa_data=[data_extractor(table_num,html_content)]
            elif table_num==1:
                gut_brain_data=[data_extractor(table_num,html_content)]
            elif table_num==2:
                gas_data=[data_extractor(table_num,html_content)]
            elif table_num==3:
                lipid_data=[data_extractor(table_num,html_content)]
            elif table_num==4:
                metabolism_data=[data_extractor(table_num,html_content)]
            elif table_num==5:
                vitamin_data=[data_extractor(table_num,html_content)]
    except Exception as e:
        print(f"An error occured in data allocation to respective lists:{e}")
            
    #Create the dict
    func_data = {
        "scfa": scfa_data,
        "gutBrain": gut_brain_data,
        "gas": gas_data,
        "lipid": lipid_data,
        "metabolism": metabolism_data,
        "vitamin": vitamin_data
    }
    json_file_path=r"C:\Users\shaima_ahmed\Documents\Pipeline_Optimisation\Function_file.json"
    html_to_json(json_file_path, func_data)
        
if __name__ == "__main__":
    main()