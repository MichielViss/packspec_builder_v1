import pandas as pd
import numpy as np

#### read the input file to determine the size, shape and column header details   
packspec_layout = pd.read_csv("sd.CSV")
packspec_layout = pd.DataFrame(columns=packspec_layout.columns)

#### read the MARM files and group by articles
material_master = pd.read_excel("Excel/dev_test.XLSX")
material_grouped = material_master.groupby("Article", sort=True)

########## global variable declarations #######################
total_packspecs = len(material_grouped)
seq_count = 1
temp_count = 1
temp_four_pack = pd.DataFrame(np.nan, index = range(2), columns=packspec_layout.columns)
pack_update = pd.DataFrame(np.nan, index = range(2), columns=packspec_layout.columns)
###############################################################

######### two level packspec data ##############
def level_2(df_y, counter, temp_count, temp_four_pack):
    temp_count = 1
    if (df_y["AUn"] == "PAL").any(): #this determines what packspec group we are going to use
        h_data = {
            "DL_RECTYPE"        : "H",
            "PS Sequence"       : counter,
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
            "PS Sequence"       : counter,
            "DL_LEVEL_SEQ"      : temp_count,
            "DL_REC_SEQ"        : temp_count,
            "Product"           : f"{df_y["Article"].iloc[temp_count-1]}", 
            "Unit"              : df_y["AUn"].iloc[temp_count-1],
            "Quantity"          : df_y["Numer."].iloc[temp_count-1]
        }
        header_row = pd.DataFrame([c_data], columns=temp_four_pack.columns)
    ##############################################################################################
        level_row = pd.DataFrame(index = range(len(df_y)), columns=temp_four_pack.columns)
        xd=0
        for i in range(len(df_y)):
            level_row.loc[i, 'DL_RECTYPE'] = "L"
            level_row.loc[i, 'PS Sequence'] = counter
            level_row.loc[i, 'DL_LEVEL_SEQ'] = xd+1
            level_row.loc[i, 'DL_REC_SEQ'] = "1"
            level_row.loc[i, 'Level Seq. No.'] = xd+1
            if xd == 0:
                level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]
            else:
                level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]/df_y["Numer."].iloc[xd-1]
            
            level_row.loc[i, 'Total Weight'] = df_y["Gross Weight"].iloc[xd]
            level_row.loc[i, 'Total Volume'] = df_y["Volume"].iloc[xd]
            level_row.loc[i, 'Length'] = df_y["Length"].iloc[xd]
            level_row.loc[i, 'Width'] = df_y["Width"].iloc[xd]
            level_row.loc[i, 'Height'] = df_y["Height"].iloc[xd]
            level_row.loc[i, 'Unit.1'] = df_y["Unit of Dimension"].iloc[xd]
            if(i == 0):
                level_row.loc[i, 'Level Type'] = "EACH"
                level_row.loc[i, 'HU Type'] = "YN00"
            if(i == 1):
                level_row.loc[i, 'Level Type'] = "PAL"
                level_row.loc[i, 'HU Type'] = "YN01"
                level_row.loc[i, 'Minimum Pack Size'] = "X"
                        
            xd=xd+1
    ##############################################################################################
        element_row = pd.DataFrame(index = range(len(df_y)), columns=temp_four_pack.columns)
        xf = 1
        for j in range(len(df_y)):
            element_row.loc[j, 'DL_RECTYPE'] = "E"
            element_row.loc[j, 'PS Sequence'] = counter
            element_row.loc[j, 'DL_LEVEL_SEQ'] = xf
            element_row.loc[j, 'DL_REC_SEQ'] = "1"
            element_row.loc[j, 'Level Seq. No.'] = xf
            if(j == 0):
                element_row.loc[j, 'Element Type'] = "WTVL"
            if(j == 1):
                element_row.loc[j, 'Element Type'] = "PACK"
                element_row.loc[j, 'HU Relevance'] = "X"
            xf=xf+1
        
    ##############################################################################################    
        r_data = {
            "DL_RECTYPE"        : "R",
            "PS Sequence"       : counter, #this is your counter in the larger files
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
        pack = pd.concat([key_row, header_row, level_row, element_row, record_row_1], ignore_index=True)
    
    ##############################################################################################
    if (df_y["AUn"] == "CS").any():
        h_data = {
            "DL_RECTYPE"        : "H",
            "PS Sequence"       : counter,
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
            "PS Sequence"       : counter,
            "DL_LEVEL_SEQ"      : temp_count,
            "DL_REC_SEQ"        : temp_count,
            "Product"           : f"{df_y["Article"].iloc[temp_count-1]}"   , 
            "Unit"              : df_y["AUn"].iloc[temp_count-1],
            "Quantity"          : df_y["Numer."].iloc[temp_count-1]
        }
        header_row = pd.DataFrame([c_data], columns=temp_four_pack.columns)
    ##############################################################################################
        level_row = pd.DataFrame(index = range(len(df_y)), columns=temp_four_pack.columns)
        xd=0
        for i in range(len(df_y)):
            level_row.loc[i, 'DL_RECTYPE'] = "L"
            level_row.loc[i, 'PS Sequence'] = counter
            level_row.loc[i, 'DL_LEVEL_SEQ'] = xd+1
            level_row.loc[i, 'DL_REC_SEQ'] = "1"
            level_row.loc[i, 'Level Seq. No.'] = xd+1
            if xd == 0:
                level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]
            else:
                level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]/df_y["Numer."].iloc[xd-1]
            level_row.loc[i, 'Total Weight'] = df_y["Gross Weight"].iloc[xd]
            level_row.loc[i, 'Total Volume'] = df_y["Volume"].iloc[xd]
            level_row.loc[i, 'Length'] = df_y["Length"].iloc[xd]
            level_row.loc[i, 'Width'] = df_y["Width"].iloc[xd]
            level_row.loc[i, 'Height'] = df_y["Height"].iloc[xd]
            level_row.loc[i, 'Unit.1'] = df_y["Unit of Dimension"].iloc[xd]
            if(i == 0):
                level_row.loc[i, 'Level Type'] = "EACH"
                level_row.loc[i, 'HU Type'] = "YN00"
            if(i == 1):
                level_row.loc[i, 'Level Type'] = "CS"
                level_row.loc[i, 'HU Type'] = "YN02"
                level_row.loc[i, 'Minimum Pack Size'] = "X"                
            xd=xd+1
    ##############################################################################################
        element_row = pd.DataFrame(index = range(len(df_y)), columns=temp_four_pack.columns)
        xf = 1
        for j in range(len(df_y)):
            element_row.loc[j, 'DL_RECTYPE'] = "E"
            element_row.loc[j, 'PS Sequence'] = counter
            element_row.loc[j, 'DL_LEVEL_SEQ'] = xf
            element_row.loc[j, 'DL_REC_SEQ'] = "1"
            element_row.loc[j, 'Level Seq. No.'] = xf
            if(j == 0):
                element_row.loc[j, 'Element Type'] = "WTVL"
            if(j == 1):
                element_row.loc[j, 'Element Type'] = "PACK"
                element_row.loc[j, 'HU Relevance'] = "X"
            xf=xf+1
    ##############################################################################################
        r_data = {
            "DL_RECTYPE"        : "R",
            "PS Sequence"       : counter, #this is your counter in the larger files
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
        pack = pd.concat([key_row, header_row, level_row, element_row, record_row_1], ignore_index=True)
    ##############################################################################################
    if (df_y["AUn"] == "SW").any():
        h_data = {
            "DL_RECTYPE"        : "H",
            "PS Sequence"       : counter,
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
            "PS Sequence"       : counter,
            "DL_LEVEL_SEQ"      : temp_count,
            "DL_REC_SEQ"        : temp_count,
            "Product"           : f"{df_y["Article"].iloc[temp_count-1]}"   , 
            "Unit"              : df_y["AUn"].iloc[temp_count-1],
            "Quantity"          : df_y["Numer."].iloc[temp_count-1]
        }
        header_row = pd.DataFrame([c_data], columns=temp_four_pack.columns)
    ##############################################################################################
        level_row = pd.DataFrame(index = range(len(df_y)), columns=temp_four_pack.columns)
        xd=0
        for i in range(len(df_y)):
            level_row.loc[i, 'DL_RECTYPE'] = "L"
            level_row.loc[i, 'PS Sequence'] = counter
            level_row.loc[i, 'DL_LEVEL_SEQ'] = xd+1
            level_row.loc[i, 'DL_REC_SEQ'] = "1"
            level_row.loc[i, 'Level Seq. No.'] = xd+1
            if xd == 0:
                level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]
            else:
                level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]/df_y["Numer."].iloc[xd-1]
            level_row.loc[i, 'Total Weight'] = df_y["Gross Weight"].iloc[xd]
            level_row.loc[i, 'Total Volume'] = df_y["Volume"].iloc[xd]
            level_row.loc[i, 'Length'] = df_y["Length"].iloc[xd]
            level_row.loc[i, 'Width'] = df_y["Width"].iloc[xd]
            level_row.loc[i, 'Height'] = df_y["Height"].iloc[xd]
            level_row.loc[i, 'Unit.1'] = df_y["Unit of Dimension"].iloc[xd]
            if(i == 0):
                level_row.loc[i, 'Level Type'] = "EACH"
                level_row.loc[i, 'HU Type'] = "YN00"
            if(i == 1):
                level_row.loc[i, 'Level Type'] = "SW"
                level_row.loc[i, 'HU Type'] = "YN00"
                level_row.loc[i, 'Minimum Pack Size'] = "X"                    
            xd=xd+1
    ##############################################################################################
        element_row = pd.DataFrame(index = range(len(df_y)), columns=temp_four_pack.columns)
        xf = 1
        for j in range(len(df_y)):
            element_row.loc[j, 'DL_RECTYPE'] = "E"
            element_row.loc[j, 'PS Sequence'] = counter
            element_row.loc[j, 'DL_LEVEL_SEQ'] = xf
            element_row.loc[j, 'DL_REC_SEQ'] = "1"
            element_row.loc[j, 'Level Seq. No.'] = xf
            if(j == 0):
                element_row.loc[j, 'Element Type'] = "WTVL"
            if(j == 1):
                element_row.loc[j, 'Element Type'] = "PACK"
                element_row.loc[j, 'HU Relevance'] = "X"
            xf=xf+1    
        r_data = {
            "DL_RECTYPE"        : "R",
            "PS Sequence"       : counter, #this is your counter in the larger files
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
        pack = pd.concat([key_row, header_row, level_row, element_row, record_row_1], ignore_index=True)
    return pack
######### three level packspec data ##############
def level_3(df_y, counter, temp_count, temp_four_pack):
    temp_count = 1
    h_data = {
        "DL_RECTYPE"        : "H",
        "PS Sequence"       : counter,
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
            "PS Sequence"       : counter,
            "DL_LEVEL_SEQ"      : temp_count,
            "DL_REC_SEQ"        : temp_count,
            "Product"           : f"{df_y["Article"].iloc[temp_count-1]}", 
            "Unit"              : df_y["AUn"].iloc[temp_count-1],
            "Quantity"          : df_y["Numer."].iloc[temp_count-1]
    }
    header_row = pd.DataFrame([c_data], columns=temp_four_pack.columns)
##############################################################################################
    level_row = pd.DataFrame(index = range(len(df_y)), columns=temp_four_pack.columns)
    xd=0
    for i in range(len(df_y)):
        level_row.loc[i, 'DL_RECTYPE'] = "L"
        level_row.loc[i, 'PS Sequence'] = counter
        level_row.loc[i, 'DL_LEVEL_SEQ'] = xd+1
        level_row.loc[i, 'DL_REC_SEQ'] = "1"
        level_row.loc[i, 'Level Seq. No.'] = xd+1
        if xd == 0:
            level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]
        else:
            level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]/df_y["Numer."].iloc[xd-1]
        level_row.loc[i, 'Total Weight'] = df_y["Gross Weight"].iloc[xd]
        level_row.loc[i, 'Total Volume'] = df_y["Volume"].iloc[xd]
        level_row.loc[i, 'Length'] = df_y["Length"].iloc[xd]
        level_row.loc[i, 'Width'] = df_y["Width"].iloc[xd]
        level_row.loc[i, 'Height'] = df_y["Height"].iloc[xd]
        level_row.loc[i, 'Unit.1'] = df_y["Unit of Dimension"].iloc[xd]
        if(i == 0):
            level_row.loc[i, 'Level Type'] = "EACH"
            level_row.loc[i, 'HU Type'] = "YN00" #have issues that this is hardcoded here like this
        if(i == 1):
            level_row.loc[i, 'Level Type'] = "CS"
            level_row.loc[i, 'HU Type'] = "YN02"
        if(i == 2):
            level_row.loc[i, 'Level Type'] = "PAL"
            level_row.loc[i, 'HU Type'] = "YN01"
            level_row.loc[i, 'Minimum Pack Size'] = "X"
        xd=xd+1
    ##############################################################################################
    element_row = pd.DataFrame(index = range(len(df_y)), columns=temp_four_pack.columns)
    xf = 1
    for j in range(len(df_y)):
        element_row.loc[j, 'DL_RECTYPE'] = "E"
        element_row.loc[j, 'PS Sequence'] = counter
        element_row.loc[j, 'DL_LEVEL_SEQ'] = xf
        element_row.loc[j, 'DL_REC_SEQ'] = "1"
        element_row.loc[j, 'Level Seq. No.'] = xf
        if(j == 0):
            element_row.loc[j, 'Element Type'] = "WTVL"
        if(j == 1):
            element_row.loc[j, 'Element Type'] = "WTVL"
        if(j == 2):
            element_row.loc[j, 'Element Type'] = "WTVL"
        if(j == 3):
            element_row.loc[j, 'Element Type'] = "PACK"
            element_row.loc[j, 'HU Relevance'] = "X"
        xf=xf+1
##############################################################################################  
    r_data = {
        "DL_RECTYPE"        : "R",
        "PS Sequence"       : counter, #this is your counter in the larger files
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
    pack = pd.concat([key_row, header_row, level_row, element_row, record_row_1], ignore_index=True)
    return pack
######### four level packspec data ##############
def level_4(df_y, counter, temp_count, temp_four_pack):
    temp_count = 1
    h_data = {
                "DL_RECTYPE"        : "H",
                "PS Sequence"       : counter,
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
            "PS Sequence"       : counter,
            "DL_LEVEL_SEQ"      : temp_count,
            "DL_REC_SEQ"        : temp_count,
            "Product"           : f"{df_y["Article"].iloc[temp_count-1]}"   , 
            "Unit"              : df_y["AUn"].iloc[temp_count-1],
            "Quantity"          : df_y["Numer."].iloc[temp_count-1]
    }
    header_row = pd.DataFrame([c_data], columns=temp_four_pack.columns)
    ##############################################################################################
    level_row = pd.DataFrame(index = range(len(df_y)), columns=temp_four_pack.columns)
    xd = 0
    for i in range(len(df_y)):
        level_row.loc[i, 'DL_RECTYPE'] = "L"
        level_row.loc[i, 'PS Sequence'] = counter
        level_row.loc[i, 'DL_LEVEL_SEQ'] = xd+1
        level_row.loc[i, 'DL_REC_SEQ'] = "1"
        level_row.loc[i, 'Level Seq. No.'] = xd+1
        if xd == 0:
            level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]
        else:
            level_row.loc[i, 'Target Qty'] = df_y["Numer."].iloc[xd]/df_y["Numer."].iloc[xd-1]        
        level_row.loc[i, 'Total Weight'] = df_y["Gross Weight"].iloc[xd]
        level_row.loc[i, 'Total Volume'] = df_y["Volume"].iloc[xd]
        level_row.loc[i, 'Length'] = df_y["Length"].iloc[xd]
        level_row.loc[i, 'Width'] = df_y["Width"].iloc[xd]
        level_row.loc[i, 'Height'] = df_y["Height"].iloc[xd]
        level_row.loc[i, 'Unit.1'] = df_y["Unit of Dimension"].iloc[xd]
        if(i == 0):
            level_row.loc[i, 'Level Type'] = "EACH"
            level_row.loc[i, 'HU Type'] = "YN00" #have issues that this is hardcoded here like this
        if(i == 1):
            level_row.loc[i, 'Level Type'] = "SW"
            level_row.loc[i, 'HU Type'] = "YN00"
        if(i == 2):
            level_row.loc[i, 'Level Type'] = "CS"
            level_row.loc[i, 'HU Type'] = "YN02"
        if(i == 3):
            level_row.loc[i, 'Level Type'] = "PAL"
            level_row.loc[i, 'HU Type'] = "YN01"
            level_row.loc[i, 'Minimum Pack Size'] = "X"
        xd=xd+1

    element_row = pd.DataFrame(index = range(len(df_y)), columns=temp_four_pack.columns)
    xf = 1
    for j in range(len(df_y)):
        element_row.loc[j, 'DL_RECTYPE'] = "E"
        element_row.loc[j, 'PS Sequence'] = counter
        element_row.loc[j, 'DL_LEVEL_SEQ'] = xf
        element_row.loc[j, 'DL_REC_SEQ'] = "1"
        element_row.loc[j, 'Level Seq. No.'] = xf
        if(j == 0):
            element_row.loc[j, 'Element Type'] = "WTVL"
        if(j == 1):
            element_row.loc[j, 'Element Type'] = "WTVL"
        if(j == 2):
            element_row.loc[j, 'Element Type'] = "WTVL"
        if(j == 3):
            element_row.loc[j, 'Element Type'] = "PACK"
            element_row.loc[j, 'HU Relevance'] = "X"
        xf=xf+1
        
    r_data = {
        "DL_RECTYPE"        : "R",
        "PS Sequence"       : counter, #this is your counter in the larger files
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
    pack = pd.concat([key_row, header_row, level_row, element_row, record_row_1], ignore_index=True)
    
    return pack
##############################################################################################

for x, y in material_grouped: 
    df_y = y.sort_values(by="Numer.")
    considered_uoms = ['EA','CS', 'SW', 'PAL']
    considered_data = df_y[df_y["AUn"].isin(considered_uoms)]
    if len(considered_data) == 2: 
        pack_update = level_2(considered_data, seq_count, temp_count, temp_four_pack)
        if seq_count == 1:
            pack_update.to_csv("huh2.csv", mode = 'w', index=False)
            seq_count = seq_count + 1
        else:
           pack_update.to_csv("huh2.csv", mode = 'a', header=False,  index=False)
           seq_count = seq_count + 1
    if len(considered_data) == 3:
       pack_update = level_3(considered_data, seq_count, temp_count,  temp_four_pack)
       if seq_count == 1:
            pack_update.to_csv("huh2.csv", mode = 'w', index=False)
            seq_count = seq_count + 1
       else:
           pack_update.to_csv("huh2.csv", mode = 'a', header=False,  index=False)
           seq_count = seq_count + 1
    if len(considered_data) == 4:
       pack_update = level_4(considered_data, seq_count, temp_count, temp_four_pack)
       if seq_count == 1:
            pack_update.to_csv("huh2.csv", mode = 'w', index=False)
            seq_count = seq_count + 1
       else:
           pack_update.to_csv("huh2.csv", mode = 'a', header=False,  index=False)
           seq_count = seq_count + 1
    
