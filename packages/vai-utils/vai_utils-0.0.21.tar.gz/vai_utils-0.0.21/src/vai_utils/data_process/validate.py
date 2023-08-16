import pandas as pd, numpy as np
from scipy.stats import tstd

def main(d_params, dataset):
    """ FORMAT THE DATA & SAVE VARIABLES FOR LATER REFERENCE

    Args: 
        d_params: data parameters, see train_model() above
        dataset: pd.DataFrame - table of all of the samples (training, validation, & testing)

    Returns:
        x_train: dictionary - see above load_dataset()"""

    # Cannot Train W/O Labels

    dataset = dataset.dropna(subset=list(d_params["y"])).reset_index(drop=True)

    data_mapping = {}
    for k, val in {**d_params["x"], **d_params["y"]}.items():

        if val["type"] == "NUMBER":  # NUMERICAL

            dataset[k] = pd.to_numeric(dataset[k], errors='coerce').astype(float) # change dtype

            # Create a Histogram
            tmp = dataset[k].copy().dropna()  # cant use nan for number histograms
            minim, maxim = min(tmp), max(tmp)  # max-min does not persist
            if not minim == maxim:
                bins = int(round((maxim - minim) / (3.49 * tstd(tmp) * (len(tmp) ** -.333333))))
                tmp = np.histogram(tmp, bins, range=(minim, maxim))
                hist_a = list(tmp[0]/tmp[0].sum())
                data_mapping = {**data_mapping, k: {"min": minim, "max": maxim, "hist": hist_a, "type": val["type"], "bins": bins}}
            else:
                data_mapping = {**data_mapping, k: {"min": minim, "max": maxim, "hist": [maxim], "type": val["type"], "bins": 1}}

            if "null" in list(val): # TODO: derive additional imputation support (not urgent) 
                if val["null"] == "mean":
                    dataset[k] = dataset[k].fillna(dataset[k].mean())  # assume mean value
                else:
                    raise Exception(f"Error: {val['null']} not valid for {k}")
            else:
                dataset = dataset[dataset[k].notna()]  # drop nans

        elif val["type"] == "CATEGORY":  # CATEGORICAL, data shall be enumerated
            
            dataset[k] = dataset[k].astype(str)  # in case inconsistent input types with same value (e.g. 9 and "9")

            # Create analytics from non-nan
            if k in d_params["x"].keys():  # for inputs
                categories = ['nan'] + [i for i in sorted(list(set(dataset[k]))) if i != 'nan']
                dataset[k] = dataset[k].replace({val: k for k, val in enumerate(categories)}).astype('int')
                tmp = dataset[k][dataset[k] != 0].copy() # dont use nan b/c ruin analytics for sparse
            elif k in d_params["y"].keys():  # for outputs
                categories = [i for i in sorted(list(set(dataset[k]))) if i != 'nan']
                dataset[k] = dataset[k].replace({val: k for k, val in enumerate(categories)}).astype('int')
                tmp = dataset[k].copy()
            else:
                raise Exception(f"Error: problem with column {k} on learn.py data_validation()")

            # Histogram
            tmp = np.histogram(tmp, bins=len(categories)) # disclude nan cat.
            hist_a = list(tmp[0]/tmp[0].sum())
            data_mapping = {**data_mapping, k: {"hist": hist_a, "cats": categories, "type": val["type"]}}


        elif val["type"] == "STRING":  # STRING (cannot create histogram from non-categorical text)

            dataset[k] = dataset[k].astype(str).replace({"": 'nan'})  # TODO: is this right order?
            data_mapping = {**data_mapping, k: {"type": val["type"]}}

        else:
            raise Exception(f"dtype '{val['type']}' is not valid")

    dataset.reset_index(inplace=True, drop=True)

    return dataset[list(d_params["x"])], dataset[list(d_params["y"])], data_mapping
