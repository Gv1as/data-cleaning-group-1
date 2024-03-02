
def clean_df(df):
    df = df.rename(columns=lambda x: x.rstrip())
    
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    df = df.dropna(how='all')
    
    df = df[df['country'] == 'AUSTRALIA']
    
    df = df[df["year"] > 2000]
    
    columns_to_drop = ['unnamed:_11', 'unnamed:_21', 'unnamed:_22', 'case_number',
                      'case_number.1', 'href', 'href_formula', 'pdf', 'original_order']
    df = df.drop(columns_to_drop, axis=1)
    
    df.reset_index(drop=True, inplace=True)
    
    return df

def map_type(df):
    mapping = {
        "unconfirmed": "Invalid",
        "Unverified": "Invalid",
        "?": "Invalid",
        "Unconfirmed": "Invalid",
        "Provoked": "Provoked",
        "Boat": "Invalid",
        "Under investigation": "Invalid",
        "Questionable": "Invalid"
    }
    
    df["type_mapped"] = df['type'].replace(mapping)
    
    return df

def map_states(df):
    mapping = {
        "New  South Wales": "New South Wales",
        "New South ales": "New South Wales",
        "New South Wales ": "New South Wales",
        "Westerm Australia": "Western Australia",
        "Western  Australia": "Western Australia",
        "Northern Territory ": "Northern Territory"
    }

    df["state_mapped"] = df['state'].replace(mapping)

    return df

def sort_activity(df):
    df["activity"].fillna("Invalid", inplace=True)
    df["activity"] = df["activity"].str.lower().str.replace(' ', '_')

    df["activity"] = df["activity"].apply(lambda x: "fishing" if "fishing" in x else x)
    df["activity"] = df["activity"].apply(lambda x: "swimming" if "swimm" in x else x)
    df["activity"] = df["activity"].apply(lambda x: "surfing" if "surf" in x else x)
    df["activity"] = df["activity"].apply(lambda x: "snorkeling" if "snorkeling" in x else x)
    df["activity"] = df["activity"].apply(lambda x: "diving" if "diving" in x else x)
    df["activity"] = df["activity"].apply(lambda x: "kayaking" if "kayaking" in x else x)


    keywords = ["fishing", "swimming", "surfing", "snorkeling", "diving", "kayaking"]
    df["activity"] = df["activity"].apply(lambda x: "other_activities" if not any(keyword in x for keyword in keywords) else x)
    
    return df

def simplify_species(name):
    if 'white' in name:
        return 'white shark'
    elif 'thought to' in name:
        return 'not sure of species'
    elif 'involvement not confirmed' in name:
        return 'not a shark attack'
    elif 'no shark involvement' in name:
        return 'not a shark attack'
    elif 'not a' in name:
        return 'not a shark attack'
    elif 'shark involvement prior to death was not confirmed' in name:
        return 'not a shark attack'
    elif 'questionable' in name:
        return 'not a shark attack'
    elif 'jet ski bitten' in name:
        return 'not a shark attack'
    elif 'tiger' in name:
        return 'tiger shark'
    elif 'bull' in name:
        return 'bull shark'
    elif 'bronze whaler' in name:
        return 'copper shark'
    elif 'broze' in name:
        return 'copper shark'
    elif 'blacktip' in name:
        return 'blacktip shark'
    elif 'wobbegong' in name:
        return 'wobbegong shark'
    elif 'sandtiger' in name:
        return 'sandtiger shark'
    elif 'Blacktip reef' in name:
        return 'blacktip reef shark'
    elif 'zebra reef' in name:
        return 'zebra shark'
    elif 'sevengill' in name:
        return 'sevengill shark'
    elif 'grey nurse' in name:
        return 'greynurse shark'
    elif 'reef' in name:
        return 'grey reef shark'
    elif 'lemon' in name:
        return'lemon shark'
    elif 'sickelfin' in name:
        return'lemon shark'
    elif 'raggedtooth' in name:
        return 'raggedtooth shark'
    elif 'copper' in name:
        return 'copper shark'
    elif 'whitetip' in name:
        return 'whitetip shark'
    elif 'hammerhead' in name:
        return 'hammerhead shark'
    elif 'carcharhinus tilstoni' in name:
        return 'Carcharhinus tilstoni shark'
    elif 'blind' in name:
        return 'blind shark'
    elif 'mako' in name:
        return 'mako shark'
    elif 'wfite shark' in name:
        return  'white shark'
    elif 'tawny nurse' in name:
        return 'tawny nurse shark'
    else:
        return 'other'

# Function to categorize injury
def categorize_injury(injury):
    if isinstance(injury, str):
        lower_injury = injury.lower()
        if any(word in lower_injury for word in ['bitten', 'severe injuries', 'multiple injuries', 'severe injurys', 'severe injury', 'severe','severely', 'significant' ]):
            return 'Severe'
        elif 'fatal' in lower_injury or 'remains' in lower_injury:
            return 'Fatal'
        elif any(word in lower_injury for word in ['lacerations', 'minor injury', 'no injury', 'injury', 'injured']):
            return 'Minor/No Injury'
        else:
            return 'Unknown'
    else:
        return 'Unknown'

def clean_time(df):
    """ Cleaning and formatting of "time" column data"""
    
    df["time"].fillna("invalid", inplace=True)
    df["time"] = df["time"].str.lower().str.replace(' ', '_')
    
    mapping_time1 = {"midday" : "morning",
                "after_noon":"afternoon",
                "late_afternoon": "afternoon",
                "--" : "invalid",
                "sunset":"evening",
                "p.m." : "afternoon"}

    df["time"] = df['time'].replace(mapping_time1)
    
    return df   

def new_time(df):
    
    """Creating a new column with time categories"""
    
    #First defines a new column containing only entries showing the letter "h" or NaN values
    
    df["time_hour"] = df["time"].apply(lambda x: x if "h" in x else "0")
    
    # Formatting the mispelled or inconsistent values        
    mapping_time = {"before_10h00" : "10h00",
                    "-16h30":"16h00",
                    "0": "24h00",
                    "night" : "24h00",
                    "19h00,_dusk" : "19h00",
                    "midnight" : "24h00" ,
                    "sometime_between_06h00_&_08hoo"  : "07h00",
                    "before_07h00" : "06h00",
                    "09h00_-10h00" : "09h00",
                    "20h45_(sunset)" : "20h45"}
    
    df["time_hour"] = df['time_hour'].replace(mapping_time)
    
    # Including in the new column only the hour so the first numbers before "h" and converting the numbers to integers
    
    df["time_hour"] = df["time_hour"].apply(lambda x: x.split("h")[0])
    df["time_hour"] = df["time_hour"].astype(int)
    
    # Createing time categories in the new column associated with the hours of column "time"
        
    def combine_time_columns(row):
    
        """ Combines the two columns of time = "time" and "time_hour" 
        by considering first the entries of the column "time_hour". 
        The function returns the Dataframe with the complete new column time_hour """
    
        if row["time"] == "invalid":
            return "invalid"
        if row["time"] == "morning":
            return "morning"
        if row["time"] == "afternoon":
            return "afternoon"
        if row["time"] == "evening":
            return "evening"
        else:
            return row["time_hour"]
    
    df["time_of_day"] = df.apply(combine_time_columns, axis=1)  
    
    return df

def categorize_time(hour):
    """Categorizes the hour into time of day"""
    if isinstance(hour, int):
        if 6 <= hour <= 12:
            return "morning"
        elif 12 < hour <= 18:
            return "afternoon"
        elif 18 < hour <= 24:
            return "evening"
        elif 1 < hour <= 5:
            return "night"
        else:
            return "invalid"
    else:
        return "invalid"

def check_provoked(injury):
    if isinstance(injury, str) and 'provoked' in injury.lower():
        return 'Provoked'
    else:
        return 'Unprovoked'