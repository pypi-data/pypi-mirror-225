import pandas as pd

def dataframe(d_params, credentials, s3=None):
    """LOAD THE CSVS FROM AN S3 BUCKET

    Args:
        d_params: data parameters, see train_model() above
        s3: s3 connection
        credentials: dictionary - confidential information used to access s3 buckets 

    Returns:
        xy: pd.DataFrame - table of input features + outputs
   
    """

    # Download, Concat, & Reset Indices
    datasets = []

    if s3:
        for i, ds in enumerate(d_params["file_paths"]):  # csv's stored by date

            #TODO: whats going on here? different date file path storage in s3 
            # From explain tab time
            # date = ds.replace("_", "/").split("/")[-1].split(".csv")[0]  
            # From learn time 
            date = ds.split("/")[-1].split(".csv")[0]  
            s3.download_file(credentials["bucket"], ds, f"/tmp/{date+'.csv'}")
            dataset = pd.read_csv(f"/tmp/{date+'.csv'}", index_col=False)
            
            # if sorting datetime, need datetime
            if ("timeseries" in d_params) and ("datetime" in d_params["timeseries"]):
                dataset["datetime"] = pd.to_datetime(dataset["HH:MM:SS"]+" "+date)
                dataset.set_index("datetime", inplace=True, drop=True)
            
            datasets += [dataset] 
    else: 
        for i, ds in enumerate(d_params["file_paths"]):  # csv's stored by date
            date = ds.split("/")[-1].split(".csv")[0]
            dataset = pd.read_csv(ds, index_col=False)

            if ("timeseries" in d_params) and ("datetime" in d_params["timeseries"]):
                dataset["datetime"] = pd.to_datetime(dataset["HH:MM:SS"]+" "+date)
                dataset.set_index("datetime", inplace=True, drop=True)
            datasets += [dataset] 
        pass

    # Join datasets
    columns = list({**d_params["x"], **d_params["y"]})
    datasets = pd.concat(datasets)[columns]

    return datasets
    
