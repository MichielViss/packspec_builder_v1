import pandas as pd
import numpy as np

#define the data structure of the packspec (this could be a class that then returns our dataframe of the correct size)

packaging_spec_data_key = ["DL_RECTYPE", "PS Sequence", "DL_LEVEL_SEQ", "DL_REC_SEQ", "DL_FILLER"]
packaging_spec_data_header = ["Pack. Spec.","Description", "Pack. Spec. Group", "CREATED_BY", "CREATED_AT", "ORIG_SYSTEM", "CHANGED_BY", "CHANGED_AT", "Upper Limit (D.Qty)", "Lower Rnd.Lmt(D.Qty)", "Up. Limit (%MnthDem)", "Low. Limit (%MthDem)", "Min. Qty for Suppl.", "Rounding Method", "Documents Exist", "Level Set"]
packaging_spec_data_content = ["Product ID", "Product", "Unit", "Quantity", "Base Unit", "Ref. Mix Allowed", "Batch Mix Allowed", "Pack. Spec."]
packaging_spec_data_level = ["Level Seq. No.", "Target Qty", "Min. Qty", "Layer Qty", "Qty Classific.", "HU Type", "Rnd-Up Lim.(%PckSze)", "Rnd-D. Lim.(%PckSze)", "Minimum Pack Size", "Total Weight", "Loading Weight", "Weight Unit", "HU Tare Weight", "Weight Unit", "Total Volume", "Loading Volume", "Volume Unit", "Tare Volume", "Volume Unit",  "Total Capacity", "Net Capacity", "Tare Cap.", "Length", "Width", "Height", "Unit	Maximum Weight", "Excess Wgt Tolerance", "Tare Wt Var.", "Max. Volume", "Excess Volume Tol.", 	"Closed Pack.", "Max. Capacity", "Excess Cap. Tol.", "Max. Length", "Max. Width", "Max. Height", "Unit of Measure", "Minimum Volume", "Minimum Weight",	"Min. Capacity", "Operative UoM", "Level Type", "Weight Man." "Volume Man.", "Dim. Man.", "Capa. Man.", "Performing Ent.", "Print Long Text", "HU Crea.", "External Step", "Fill Up", "BAND_RND_UP", "BAND_RND_DOWN", "BAND_RND_NEAREST"]
packaging_spec_data_element = ["Product ID", "Product", "HU Relevance", "Unit", "Quantity", "Elem. Seq. No.", "Element Type", "Work Step"]
packaging_spec_data_condition = ["Cond.Table", "Condition Type", "Valid From", "Valid To", "Condition Seq.", "Log. Condition", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value", "Field name", "Value"]

#### read the input file to determine the size, shape and column header details   
packspec_layout = pd.read_csv("sd.CSV")
packspec_layout = pd.DataFrame(columns=packspec_layout.columns)

#### read the MARM files and group by articles
material_master = pd.read_excel("Excel/dev_test.XLSX")
material_grouped = material_master.groupby("Article", sort=True)

total_packspecs = len(material_grouped)
temp_count = 1 
seq_count = 1

for x, y in material_grouped:
    df_y = y.sort_values(by="Numer.")
    group_size = (len(y)*2)+3
    temp_four_pack = pd.DataFrame(np.nan, index = range(group_size), columns=packspec_layout.columns)
    if len(y) == 2:
         #from a memory allocation perspective i dont think this is necessary?
        if (df_y["AUn"]== "PAL").any(): #this determines what packspec group we are going to use
            h_data = {
                    "DL_RECTYPE"        : "H",
                    "PS Sequence"       : seq_count,
                    "DL_LEVEL_SEQ"      : temp_count,
                    "DL_REC_SEQ"        : temp_count,
                    "Description"       : f"Packspec for {x}",
                    "Pack. Spec. Group" : "PL2A",
                    "Level Set"         : "2-LEVEL A"
            }

            key_row = pd.DataFrame([h_data], columns=temp_four_pack.columns)
        #############################################################################################
            c_data = {
                    "DL_RECTYPE"        : "C",
                    "PS Sequence"       : seq_count,
                    "DL_LEVEL_SEQ"      : temp_count,
                    "DL_REC_SEQ"        : temp_count,
                    "Product"           : f"{df_y["Article"].iloc[temp_count-1]}"   , 
                    "Unit"              : df_y["AUn"].iloc[temp_count-1],
                    "Quantity"          : df_y["Numer."].iloc[temp_count-1]
            }

            header_row = pd.DataFrame([c_data], columns=temp_four_pack.columns)
        ##############################################################################################

            level_row = pd.DataFrame(index = range(len(y)), columns=temp_four_pack.columns)
            xd=0

            for i in range(len(y)):
                level_row.loc[i, 'DL_RECTYPE'] = "L"
                level_row.loc[i, 'PS Sequence'] = seq_count
                level_row.loc[i, 'DL_LEVEL_SEQ'] = i+1
                level_row.loc[i, 'DL_REC_SEQ'] = "1"
                level_row.loc[i, 'Level Seq. No.'] = i+1
                level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]
                level_row.loc[i, 'Total Weight'] = df_y["Gross Weight"].iloc[xd]
                level_row.loc[i, 'Total Volume'] = df_y["Volume"].iloc[xd]
                level_row.loc[i, 'Length'] = df_y["Length"].iloc[xd]
                level_row.loc[i, 'Width'] = df_y["Width"].iloc[xd]
                level_row.loc[i, 'Height'] = df_y["Height"].iloc[xd]
                level_row.loc[i, 'Unit.1'] = df_y["Unit of Dimension"].iloc[xd]
                if(i == 1):
                    level_row.loc[i, 'Level Type'] = "EACH"
                    level_row.loc[i, 'HU Type'] = "YN00"
                if(i == 2):
                    level_row.loc[i, 'Level Type'] = "PAL"
                    level_row.loc[i, 'HU Type'] = "YN01"
                    level_row.loc[i, 'Minimum Pack Size'] = "X"
                            
                xd=xd+1

            element_row = pd.DataFrame(index = range(len(y)), columns=temp_four_pack.columns)
            xf = 1
            for j in range(len(y)):
                element_row.loc[j, 'DL_RECTYPE'] = "E"
                element_row.loc[j, 'PS Sequence'] = seq_count
                element_row.loc[j, 'DL_LEVEL_SEQ'] = xf
                element_row.loc[j, 'DL_REC_SEQ'] = "1"
                element_row.loc[j, 'Level Seq. No.'] = xf
                if(j == 1):
                    element_row.loc[j, 'Element Type'] = "WTVL"
                if(j == 2):
                    element_row.loc[j, 'Element Type'] = "PACK"
                    element_row.loc[j, 'HU Relevance'] = "X"
                xf=xf+1
            
            r_data = {
                "DL_RECTYPE"        : "R",
                "PS Sequence"       : seq_count, #this is your counter in the larger files
                "DL_LEVEL_SEQ"      : "1",
                "DL_REC_SEQ"        : "1",
                "Cond.Table"        : "SAPPAL01",
                "Condition Type"    : "0PAL",
                "Condition Seq."    : "1",  
                "Field name"        : "PAK_LOCNO", 
                "Value"             : "DCW005_S4",
                "Field name.1"      : "PAK_MATNR", 
                "Value.1"           : f"{df_y["Article"].iloc[temp_count-1]}",
                "Valid From"        : "20250101", #need to include the date here dynamically
                "Valid To"          : "99991231"
                
            }
            record_row_1 = pd.DataFrame([r_data], columns=temp_four_pack.columns)

        
        if (df_y["AUn"] == "CS").any():

            h_data = {
                    "DL_RECTYPE"        : "H",
                    "PS Sequence"       : seq_count,
                    "DL_LEVEL_SEQ"      : temp_count,
                    "DL_REC_SEQ"        : temp_count,
                    "Description"       : f"Packspec for {x}",
                    "Pack. Spec. Group" : "PL2B",
                    "Level Set"         : "2-LEVEL B"
            }

            key_row = pd.DataFrame([h_data], columns=temp_four_pack.columns)
        #############################################################################################
            c_data = {
                    "DL_RECTYPE"        : "C",
                    "PS Sequence"       : seq_count,
                    "DL_LEVEL_SEQ"      : temp_count,
                    "DL_REC_SEQ"        : temp_count,
                    "Product"           : f"{df_y["Article"].iloc[temp_count-1]}"   , 
                    "Unit"              : df_y["AUn"].iloc[temp_count-1],
                    "Quantity"          : df_y["Numer."].iloc[temp_count-1]
            }

            header_row = pd.DataFrame([c_data], columns=temp_four_pack.columns)
        ##############################################################################################

            level_row = pd.DataFrame(index = range(len(y)), columns=temp_four_pack.columns)
            xd=0

            for i in range(len(y)):
                level_row.loc[i, 'DL_RECTYPE'] = "L"
                level_row.loc[i, 'PS Sequence'] = seq_count
                level_row.loc[i, 'DL_LEVEL_SEQ'] = i+1
                level_row.loc[i, 'DL_REC_SEQ'] = "1"
                level_row.loc[i, 'Level Seq. No.'] = i+1
                level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]
                level_row.loc[i, 'Total Weight'] = df_y["Gross Weight"].iloc[xd]
                level_row.loc[i, 'Total Volume'] = df_y["Volume"].iloc[xd]
                level_row.loc[i, 'Length'] = df_y["Length"].iloc[xd]
                level_row.loc[i, 'Width'] = df_y["Width"].iloc[xd]
                level_row.loc[i, 'Height'] = df_y["Height"].iloc[xd]
                level_row.loc[i, 'Unit.1'] = df_y["Unit of Dimension"].iloc[xd]
                if(i == 1):
                    level_row.loc[i, 'Level Type'] = "EACH"
                    level_row.loc[i, 'HU Type'] = "YN00"
                if(i == 2):
                    level_row.loc[i, 'Level Type'] = "CS"
                    level_row.loc[i, 'HU Type'] = "YN02"
                    level_row.loc[i, 'Minimum Pack Size'] = "X"
                            
                xd=xd+1

            element_row = pd.DataFrame(index = range(len(y)), columns=temp_four_pack.columns)
            xf = 1
            for j in range(len(y)):
                element_row.loc[j, 'DL_RECTYPE'] = "E"
                element_row.loc[j, 'PS Sequence'] = seq_count
                element_row.loc[j, 'DL_LEVEL_SEQ'] = xf
                element_row.loc[j, 'DL_REC_SEQ'] = "1"
                element_row.loc[j, 'Level Seq. No.'] = xf
                if(j == 1):
                    element_row.loc[j, 'Element Type'] = "WTVL"
                if(j == 2):
                    element_row.loc[j, 'Element Type'] = "PACK"
                    element_row.loc[j, 'HU Relevance'] = "X"
                xf=xf+1
            
            r_data = {
                "DL_RECTYPE"        : "R",
                "PS Sequence"       : seq_count, #this is your counter in the larger files
                "DL_LEVEL_SEQ"      : "1",
                "DL_REC_SEQ"        : "1",
                "Cond.Table"        : "SAPPAL01",
                "Condition Type"    : "0PAL",
                "Condition Seq."    : "1",  
                "Field name"        : "PAK_LOCNO", 
                "Value"             : "DCW005_S4",
                "Field name.1"      : "PAK_MATNR", 
                "Value.1"           : f"{df_y["Article"].iloc[temp_count-1]}",
                "Valid From"        : "20250101", #need to include the date here dynamically
                "Valid To"          : "99991231"
                
            }
            record_row_1 = pd.DataFrame([r_data], columns=temp_four_pack.columns)

        if (df_y["AUn"] == "SW").any():

            h_data = {
                    "DL_RECTYPE"        : "H",
                    "PS Sequence"       : seq_count,
                    "DL_LEVEL_SEQ"      : temp_count,
                    "DL_REC_SEQ"        : temp_count,
                    "Description"       : f"Packspec for {x}",
                    "Pack. Spec. Group" : "PL2C",
                    "Level Set"         : "2-LEVEL C"
            }

            key_row = pd.DataFrame([h_data], columns=temp_four_pack.columns)
        #############################################################################################
            c_data = {
                    "DL_RECTYPE"        : "C",
                    "PS Sequence"       : seq_count,
                    "DL_LEVEL_SEQ"      : temp_count,
                    "DL_REC_SEQ"        : temp_count,
                    "Product"           : f"{df_y["Article"].iloc[temp_count-1]}"   , 
                    "Unit"              : df_y["AUn"].iloc[temp_count-1],
                    "Quantity"          : df_y["Numer."].iloc[temp_count-1]
            }

            header_row = pd.DataFrame([c_data], columns=temp_four_pack.columns)
        ##############################################################################################

            level_row = pd.DataFrame(index = range(len(y)), columns=temp_four_pack.columns)
            xd=0

            for i in range(len(y)):
                level_row.loc[i, 'DL_RECTYPE'] = "L"
                level_row.loc[i, 'PS Sequence'] = seq_count
                level_row.loc[i, 'DL_LEVEL_SEQ'] = i+1
                level_row.loc[i, 'DL_REC_SEQ'] = "1"
                level_row.loc[i, 'Level Seq. No.'] = i+1
                level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]
                level_row.loc[i, 'Total Weight'] = df_y["Gross Weight"].iloc[xd]
                level_row.loc[i, 'Total Volume'] = df_y["Volume"].iloc[xd]
                level_row.loc[i, 'Length'] = df_y["Length"].iloc[xd]
                level_row.loc[i, 'Width'] = df_y["Width"].iloc[xd]
                level_row.loc[i, 'Height'] = df_y["Height"].iloc[xd]
                level_row.loc[i, 'Unit.1'] = df_y["Unit of Dimension"].iloc[xd]
                if(i == 1):
                    level_row.loc[i, 'Level Type'] = "EACH"
                    level_row.loc[i, 'HU Type'] = "YN00"
                if(i == 2):
                    level_row.loc[i, 'Level Type'] = "SW"
                    level_row.loc[i, 'HU Type'] = "YN00"
                    level_row.loc[i, 'Minimum Pack Size'] = "X"
                            
                xd=xd+1

            element_row = pd.DataFrame(index = range(len(y)), columns=temp_four_pack.columns)
            xf = 1
            for j in range(len(y)):
                element_row.loc[j, 'DL_RECTYPE'] = "E"
                element_row.loc[j, 'PS Sequence'] = seq_count
                element_row.loc[j, 'DL_LEVEL_SEQ'] = xf
                element_row.loc[j, 'DL_REC_SEQ'] = "1"
                element_row.loc[j, 'Level Seq. No.'] = xf
                if(j == 1):
                    element_row.loc[j, 'Element Type'] = "WTVL"
                if(j == 2):
                    element_row.loc[j, 'Element Type'] = "PACK"
                    element_row.loc[j, 'HU Relevance'] = "X"
                xf=xf+1
            
            r_data = {
                "DL_RECTYPE"        : "R",
                "PS Sequence"       : seq_count, #this is your counter in the larger files
                "DL_LEVEL_SEQ"      : "1",
                "DL_REC_SEQ"        : "1",
                "Cond.Table"        : "SAPPAL01",
                "Condition Type"    : "0PAL",
                "Condition Seq."    : "1",  
                "Field name"        : "PAK_LOCNO", 
                "Value"             : "DCW005_S4",
                "Field name.1"      : "PAK_MATNR", 
                "Value.1"           : f"{df_y["Article"].iloc[temp_count-1]}",
                "Valid From"        : "20250101", #need to include the date here dynamically
                "Valid To"          : "99991231"
                
            }
            record_row_1 = pd.DataFrame([r_data], columns=temp_four_pack.columns)
        temp_four_pack = pd.concat([key_row, header_row, level_row, element_row, record_row_1], ignore_index=True)
        if seq_count == 1:
            temp_four_pack.to_csv("huh2.csv", mode = 'w', index=False)
            seq_count = seq_count + 1
        else:
            temp_four_pack.to_csv("huh2.csv", mode = 'a', header=False,  index=False)
            seq_count = seq_count + 1   

    if len(y) == 3:
        df_y = y.sort_values(by="Numer.") #try and sort it by numerator in the grouping [TO DO] - check the name of the column numerator for future reference
        group_size = (len(y)*2)+3
        temp_four_pack = pd.DataFrame(np.nan, index = range(group_size), columns=packspec_layout.columns)
        considered_uoms_3 = ["EA", "CS", "PAL"]
        y_cleansed_3 = df_y[df_y['AUn'].isin(considered_uoms_3)]
        if len(y_cleansed_3) == 3:
                h_data = {
                    "DL_RECTYPE"        : "H",
                    "PS Sequence"       : seq_count,
                    "DL_LEVEL_SEQ"      : temp_count,
                    "DL_REC_SEQ"        : temp_count,
                    "Description"       : f"Packspec for {x}",
                    "Pack. Spec. Group" : "PL3A",
                    "Level Set"         : "3-LEVEL A"
                }

                key_row = pd.DataFrame([h_data], columns=temp_four_pack.columns)
            #############################################################################################
                c_data = {
                        "DL_RECTYPE"        : "C",
                        "PS Sequence"       : seq_count,
                        "DL_LEVEL_SEQ"      : temp_count,
                        "DL_REC_SEQ"        : temp_count,
                        "Product"           : f"{df_y["Article"].iloc[temp_count-1]}"   , 
                        "Unit"              : df_y["AUn"].iloc[temp_count-1],
                        "Quantity"          : df_y["Numer."].iloc[temp_count-1]
                }

                header_row = pd.DataFrame([c_data], columns=temp_four_pack.columns)
            ##############################################################################################

                level_row = pd.DataFrame(index = range(len(y)), columns=temp_four_pack.columns)
                xd=0#counter of the MARM record
                #consider we might need to add quantity classification

                for i in range(len(y)):
                    level_row.loc[i, 'DL_RECTYPE'] = "L"
                    level_row.loc[i, 'PS Sequence'] = seq_count
                    level_row.loc[i, 'DL_LEVEL_SEQ'] = i+1
                    level_row.loc[i, 'DL_REC_SEQ'] = "1"
                    level_row.loc[i, 'Level Seq. No.'] = i+1
                    level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]
                    level_row.loc[i, 'Total Weight'] = df_y["Gross Weight"].iloc[xd]
                    level_row.loc[i, 'Total Volume'] = df_y["Volume"].iloc[xd]
                    level_row.loc[i, 'Length'] = df_y["Length"].iloc[xd]
                    level_row.loc[i, 'Width'] = df_y["Width"].iloc[xd]
                    level_row.loc[i, 'Height'] = df_y["Height"].iloc[xd]
                    level_row.loc[i, 'Unit.1'] = df_y["Unit of Dimension"].iloc[xd]
                    if(i == 1):
                        level_row.loc[i, 'Level Type'] = "EACH"
                        level_row.loc[i, 'HU Type'] = "YN00" #have issues that this is hardcoded here like this
                    if(i == 2):
                        level_row.loc[i, 'Level Type'] = "CS"
                        level_row.loc[i, 'HU Type'] = "YN02"
                    if(i == 3):
                        level_row.loc[i, 'Level Type'] = "PAL"
                        level_row.loc[i, 'HU Type'] = "YN01"
                        level_row.loc[i, 'Minimum Pack Size'] = "X"
                    xd=xd+1

                element_row = pd.DataFrame(index = range(len(y)), columns=temp_four_pack.columns)
                xf = 1
                for j in range(len(y)):
                    element_row.loc[j, 'DL_RECTYPE'] = "E"
                    element_row.loc[j, 'PS Sequence'] = seq_count
                    element_row.loc[j, 'DL_LEVEL_SEQ'] = xf
                    element_row.loc[j, 'DL_REC_SEQ'] = "1"
                    element_row.loc[j, 'Level Seq. No.'] = xf
                    if(j == 1):
                        element_row.loc[j, 'Element Type'] = "WTVL"
                    if(j == 2):
                        element_row.loc[j, 'Element Type'] = "WTVL"
                    if(j == 3):
                        element_row.loc[j, 'Element Type'] = "WTVL"
                    if(j == 4):
                        element_row.loc[j, 'Element Type'] = "PACK"
                        element_row.loc[j, 'HU Relevance'] = "X"
                    xf=xf+1
                
                r_data = {
                    "DL_RECTYPE"        : "R",
                    "PS Sequence"       : seq_count, #this is your counter in the larger files
                    "DL_LEVEL_SEQ"      : "1",
                    "DL_REC_SEQ"        : "1",
                    "Cond.Table"        : "SAPPAL01",
                    "Condition Type"    : "0PAL",
                    "Condition Seq."    : "1",  
                    "Field name"        : "PAK_LOCNO", 
                    "Value"             : "DCW005_S4",
                    "Field name.1"      : "PAK_MATNR", 
                    "Value.1"           : "41090",
                    "Valid From"        : "20250101", #need to include the date here dynamically
                    "Valid To"          : "99991231"
                    
                }
                record_row_1 = pd.DataFrame([r_data], columns=temp_four_pack.columns)
                temp_four_pack = pd.concat([key_row, header_row, level_row, element_row, record_row_1], ignore_index=True)
                if seq_count == 1:
                    temp_four_pack.to_csv("huh2.csv", mode = 'w', index=False)
                    seq_count = seq_count + 1
                else:
                    temp_four_pack.to_csv("huh2.csv", mode = 'a', header=False,  index=False)
                    seq_count = seq_count + 1
                
    if len(y) >= 4:
        #then only consider the following units of measure from y
        considered_uoms = ['EA','CS', 'SW', 'PAL' ] #what are we going to do if they dont have a PAL uom at all? 
        y_cleansed = df_y[df_y['AUn'].isin(considered_uoms)]
        
        h_data = {
                "DL_RECTYPE"        : "H",
                "PS Sequence"       : seq_count,
                "DL_LEVEL_SEQ"      : temp_count,
                "DL_REC_SEQ"        : temp_count,
                "Description"       : f"Packspec for {x}",
                "Pack. Spec. Group" : "PL4A",
                "Level Set"         : "4-LEVEL A"
        }

        key_row = pd.DataFrame([h_data], columns=temp_four_pack.columns)
    #############################################################################################
        c_data = {
                "DL_RECTYPE"        : "C",
                "PS Sequence"       : seq_count,
                "DL_LEVEL_SEQ"      : temp_count,
                "DL_REC_SEQ"        : temp_count,
                "Product"           : f"{y_cleansed["Article"].iloc[temp_count-1]}"   , 
                "Unit"              : y_cleansed["AUn"].iloc[temp_count-1],
                "Quantity"          : y_cleansed["Numer."].iloc[temp_count-1]
        }

        header_row = pd.DataFrame([c_data], columns=temp_four_pack.columns)
    ##############################################################################################

        level_row = pd.DataFrame(index = range(len(y_cleansed)), columns=temp_four_pack.columns)
       
        xd = 0
        for i in range(len(y_cleansed)):
            level_row.loc[i, 'DL_RECTYPE'] = "L"
            level_row.loc[i, 'PS Sequence'] = seq_count
            level_row.loc[i, 'DL_LEVEL_SEQ'] = i+1
            level_row.loc[i, 'DL_REC_SEQ'] = "1"
            level_row.loc[i, 'Level Seq. No.'] = i+1
            level_row.loc[i, 'Target Qty'] = y_cleansed["Numer."].iloc[xd]        
            level_row.loc[i, 'Total Weight'] = y_cleansed["Gross Weight"].iloc[xd]
            level_row.loc[i, 'Total Volume'] = y_cleansed["Volume"].iloc[xd]
            level_row.loc[i, 'Length'] = y_cleansed["Length"].iloc[xd]
            level_row.loc[i, 'Width'] = y_cleansed["Width"].iloc[xd]
            level_row.loc[i, 'Height'] = y_cleansed["Height"].iloc[xd]
            level_row.loc[i, 'Unit.1'] = y_cleansed["Unit of Dimension"].iloc[xd]
            if(i == 1):
                level_row.loc[i, 'Level Type'] = "EACH"
                level_row.loc[i, 'HU Type'] = "YN00" #have issues that this is hardcoded here like this
            if(i == 2):
                level_row.loc[i, 'Level Type'] = "SW"
                level_row.loc[i, 'HU Type'] = "YN00"
            if(i == 3):
                level_row.loc[i, 'Level Type'] = "CS"
                level_row.loc[i, 'HU Type'] = "YN02"
            if(i == 4):
                level_row.loc[i, 'Level Type'] = "PAL"
                level_row.loc[i, 'HU Type'] = "YN01"
                level_row.loc[i, 'Minimum Pack Size'] = "X"
            xd=xd+1

        element_row = pd.DataFrame(index = range(len(y_cleansed)), columns=temp_four_pack.columns)
        xf = 1
        for j in range(len(y_cleansed)):
            element_row.loc[j, 'DL_RECTYPE'] = "E"
            element_row.loc[j, 'PS Sequence'] = seq_count
            element_row.loc[j, 'DL_LEVEL_SEQ'] = xf
            element_row.loc[j, 'DL_REC_SEQ'] = "1"
            element_row.loc[j, 'Level Seq. No.'] = xf
            if(j == 1):
                element_row.loc[j, 'Element Type'] = "WTVL"
            if(j == 2):
                element_row.loc[j, 'Element Type'] = "WTVL"
            if(j == 3):
                element_row.loc[j, 'Element Type'] = "WTVL"
            if(j == 4):
                element_row.loc[j, 'Element Type'] = "PACK"
                element_row.loc[j, 'HU Relevance'] = "X"
        xf=xf+1
        
        r_data = {
            "DL_RECTYPE"        : "R",
            "PS Sequence"       : seq_count, #this is your counter in the larger files
            "DL_LEVEL_SEQ"      : "1",
            "DL_REC_SEQ"        : "1",
            "Cond.Table"        : "SAPPAL01",
            "Condition Type"    : "0PAL",
            "Condition Seq."    : "1",  
            "Field name"        : "PAK_LOCNO", 
            "Value"             : "DCW005_S4",
            "Field name.1"      : "PAK_MATNR", 
            "Value.1"           : "41090",
            "Valid From"        : "20250101", #need to include the date here dynamically
            "Valid To"          : "99991231"
        }
        record_row_1 = pd.DataFrame([r_data], columns=temp_four_pack.columns)
        temp_four_pack = pd.concat([key_row, header_row, level_row, element_row, record_row_1], ignore_index=True)
        if seq_count == 1:
            temp_four_pack.to_csv("huh2.csv", mode = 'w', index=False)
            seq_count = seq_count + 1
        else:
            temp_four_pack.to_csv("huh2.csv", mode = 'a', header=False,  index=False)
            seq_count = seq_count + 1


# temp_four_pack = pd.concat([key_row, header_row, level_row, element_row, record_row_1], ignore_index=True)
# temp_four_pack.to_csv("huh2.csv", index=False)