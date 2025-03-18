import csv

def prepare_dict_from_csv(file_path):
    data_dict = {}
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                data_dict[row['ID']] = row['CO2']
        

        return data_dict
    
    except FileNotFoundError:
        print(f"Fails '{file_path}' netika atrasts.")
        return None
    except Exception as e:
        print(f"Notikusi kļūda: {e}")
        return None


if __name__ == "__main__":
    pass