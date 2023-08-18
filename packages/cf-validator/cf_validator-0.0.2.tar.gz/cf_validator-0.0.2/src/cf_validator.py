def cf_validator():

    import json
    import sys
    import yaml

    def is_valid_json(json_str):
        try:
            json.loads(json_str)
            return True, None
        except json.JSONDecodeError as e:
            return False, f"Error:JSON file is not in correct format. Line {e.lineno}, column {e.colno}: {e.msg}."

    def is_valid_yaml(file_path):
        try:
            file=open(file_path, 'r')
            yaml.safe_load(file)
            return True
        except yaml.YAMLError as e:
            words=str(e)
            check=words.split()
            for i in check:
                if i in intrinsic:
                    signal=True
                else:
                    signal=False
                if signal:
                    break
            if signal:
                return True
            else:
                return "Error:JSON file is not in correct format."+str(e)
            
    def replace_s_exclamation(dictionary):
        new_dict = {}
        for key, value in dictionary.items():
            if isinstance(value, dict):
                new_dict[key] = replace_s_exclamation(value)
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, str):
                        new_list.append(item.replace('s!', '!'))
                    elif isinstance(item, dict):
                        new_list.append(replace_s_exclamation(item))
                    else:
                        new_list.append(item)
                new_dict[key] = new_list
            elif isinstance(value, str):
                new_dict[key] = value.replace('s!', '!')
            else:
                new_dict[key] = value
        return new_dict

    def extract_ref_values(data):
        ref_values = []
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "Ref":
                    ref_values.append(value)
                else:
                    ref_values.extend(extract_ref_values(value))
        elif isinstance(data, list):
            for item in data:
                ref_values.extend(extract_ref_values(item))
        return ref_values

    def has_intrinsic_functions_in_parameters(template):  
        if "Parameters" in template:
            parameters = template["Parameters"]
            for param_name, param_details in parameters.items():
                for func in intrinsic_functions:
                    if func in param_details.get("Default", ""):
                        return True
        return False

    checklist=[]

    parameter_types=[]

    intrinsic_functions = ['Ref', 'Fn::Sub', 'Fn::GetAtt', 'Fn::Join', 'Fn::If', 'Fn::ImportValue', 'Fn::FindInMap']

    intrinsic=["'!Ref'", "'!Sub'", "'!GetAtt'", "'!ImportValue'", "'!Join'", "'!Select'", 
            "'!Split'", "'!Base64'", "'!Cidr'", "'!Transform'", "'!Not'", "'!Equals'", "'!FindInMap'", "'!If'"]

    path=input()

    start=len(path)-4
    end=len(path)

    if path[start:end] in ['json','yaml']:
        file=path[start:end]
        extension=True

    else:
        print('Error: Invalid input file format.')
        extension=False

    if extension==True:

        if file=='json':
            f=open(path)
            json_data=f.read()
            val=is_valid_json(json_data)
            
            if val[0]==False:
                print(val[1])
                sys.exit()
            
            else:
                data=json.loads(json_data)
                key_list=list(data.keys())
                ref_values=extract_ref_values(data)
                
                resources=data.get("Resources",{})
                l=resources.keys() 

                for i in l:
                    checklist.append(i)

                parameters=data.get("Parameters",{})
                m=parameters.keys()

                for i in m:
                    checklist.append(i)

                types=parameters.values()
                
                for i in types:
                    parameter_types.append(i.get('Type'))
                        
                if 'Resources' in key_list:
                    for i in key_list:
                        if i=='AWSTemplateFormatVersion':
                            if type(data['AWSTemplateFormatVersion'])==str:
                                continue
                            else:
                                print("Error: AWSTemplateFormatVersion should be a string containing the date.")
                                sys.exit()

                        elif i=='Description':
                            if type(data['Description'])==str:
                                continue
                            else:
                                print("Error: Description should be a string.")
                                sys.exit()

                        elif i=='Metadata':
                            continue

                        elif i=='Resources':                    
                            for k in ref_values:
                                if k in checklist:
                                    continue
                                else:
                                    print("Error: Reference",k,"is not present.")
                                    sys.exit()

                        elif i=='Parameters':
                            for i in parameter_types:
                                if i in ['String', 'Number', 'List<Number>', 'CommaDelimitedList']:
                                    continue
                                else:
                                    print("Error: Invalid 'Type' in 'Parameters'.")
                                    sys.exit()
                            
                            has_intrinsic_in_params = has_intrinsic_functions_in_parameters(data)

                            if has_intrinsic_in_params:
                                print("Error: The 'Parameters' dictionary contains intrinsic functions.")
                                sys.exit()

                            else:
                                continue

                        elif i=='Rules':
                            continue

                        elif i=='Mappings':
                            continue

                        elif i=='Conditions':
                            continue
                        
                        elif i=='Transform':
                            continue
                                        
                        elif i=='Outputs':
                            continue
                        
                        else:
                            print("Error: Unknown data",i,"found.")
                            sys.exit()

                else:
                    print("Error: Resource data missing in the file")
                    sys.exit()

                print("Validation successful, the input file is valid.")
        

        else:

            f=open(path)  
            if is_valid_yaml(path)==True:
                read=f.read()
                l=read.split("!")
                read_data=""
                for i in l:
                    read_data+=i+"s!"
                read_data=read_data[:-2]
                input_dict=yaml.safe_load(read_data) 
                modified_dict = replace_s_exclamation(input_dict)
                
                key_list=list(modified_dict.keys())
                ref_values=extract_ref_values(modified_dict)
                
                resources=modified_dict.get("Resources",{})
                l=resources.keys() 

                for i in l:
                    checklist.append(i)

                parameters=modified_dict.get("Parameters",{})
                m=parameters.keys()

                for i in m:
                    checklist.append(i)

                types=parameters.values()
                for i in types:
                    parameter_types.append(i.get('Type'))
                
                if 'Resources' in key_list:
                    for i in key_list:
                        if i=='AWSTemplateFormatVersion':
                            if type(modified_dict['AWSTemplateFormatVersion'])==str:
                                continue
                            else:
                                print("Error: AWSTemplateFormatVersion should be a string containing the date.")
                                sys.exit()

                        elif i=='Description':
                            if type(modified_dict['Description'])==str:
                                continue
                            else:
                                print("Error: Description should be a string.")
                                sys.exit()

                        elif i=='Metadata':
                            continue

                        elif i=='Resources':                    
                            for k in ref_values:
                                if k in checklist:
                                    continue
                                else:
                                    print("Error: Reference",k,"is not present.")
                                    sys.exit()

                        elif i=='Parameters':
                            for i in parameter_types:
                                if i in ['String', 'Number', 'List<Number>', 'CommaDelimitedList']:
                                    continue
                                else:
                                    print("Error: Invalid 'Type' in 'Parameters'.")
                                    sys.exit()
                            
                            has_intrinsic_in_params = has_intrinsic_functions_in_parameters(modified_dict)

                            if has_intrinsic_in_params:
                                print("Error: The 'Parameters' dictionary contains intrinsic functions.")
                                sys.exit()

                            else:
                                continue

                        elif i=='Rules':
                            continue

                        elif i=='Mappings':
                            continue

                        elif i=='Conditions':
                            continue
                        
                        elif i=='Transform':
                            continue
                                        
                        elif i=='Outputs':
                            continue
                        
                        else:
                            print("Error: Unknown data",i,"found.")
                            sys.exit()

                else:
                    print("Error: Resource data missing in the file")
                    sys.exit()

                print("Validation successful, the input file is valid.")

            else:
                print(is_valid_yaml(path))
                sys.exit()

