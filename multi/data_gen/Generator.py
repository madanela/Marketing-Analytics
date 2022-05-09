import numpy as np
import pandas as pd
it = 0
basic_names = ["user_id","version","minutes_play","day_1_active","day_7_active","cost","gain"]
def Generate_Sample_data(number_of_datapoints, cost_min,cost_max,gain,version,):
    global it
    data = np.array([1000*it + np.arange(number_of_datapoints)+1,
                     [version]*number_of_datapoints,
                     np.random.random(size =(number_of_datapoints),) * 100 ,
                     np.random.randint(2,size = number_of_datapoints),
                     np.random.randint(2,size = number_of_datapoints),
                     [np.random.randint(cost_min,cost_max)]*number_of_datapoints,
                     [gain] * number_of_datapoints
                     ]).T
    it+=1
    return data
def create_dataframe(num_of_datapoints,cost_min,cost_max,gain,feature_names,version):
    return pd.DataFrame(
    data = Generate_Sample_data(num_of_datapoints,cost_min,cost_max,gain,version = version),
 
    columns= feature_names)
    
    
def generate_dataset(num_of_groups,num_of_datapoints,cost_min,cost_max,gain,feature_names = basic_names):
    control_group = create_dataframe(num_of_datapoints,cost_min,cost_max,gain,feature_names,"control")
    Treatment_groups = [create_dataframe(num_of_datapoints,
                                     cost_min,cost_max,gain,feature_names,"treatment_"+str(i+1)) for i in range(num_of_groups)]
    data = pd.concat([control_group,pd.concat(Treatment_groups)])
    for each in data.columns:
        if each == 'user_id':
           data[each] = np.int64(data[each])
        elif each!='version':
            data[each]=np.float64(data[each])
    return data
def generte_treatment_results(num_of_groups,num_of_datapoints,cost_min,cost_max,gain,feature_names = basic_names):
    return np.array([np.random.randint(2,size = num_of_datapoints) for i in range(num_of_groups)])