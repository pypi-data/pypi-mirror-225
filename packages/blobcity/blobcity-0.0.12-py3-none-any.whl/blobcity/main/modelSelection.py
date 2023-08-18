# Copyright 2021 BlobCity, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import numpy as np
import pandas as pd
from math import isnan
import warnings,itertools
from blobcity.store import Model
from sklearn.metrics import r2_score
from blobcity.config import tuner as Tuner
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import cross_val_score
from blobcity.config import classifier_config,regressor_config,time_config
from blobcity.utils import Progress,scaling_data,AutoFeatureSelection
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import SimpleExpSmoothing,ExponentialSmoothing, Holt
from blobcity.utils import *
import warnings
warnings.filterwarnings("ignore")
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.simplefilter(action='ignore', category=FutureWarning)
    os.environ["PYTHONWARNINGS"] = "ignore"
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    import autokeras as ak
    import tensorflow as tf
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
"""
This python file consists of function to get best performing model for a given dataset.
"""

class CustomCallback(tf.keras.callbacks.Callback):
    def on_train_end(self, logs=None):
        prog.update_progressbar(1)
    def on_epoch_end(self, epoch, logs=None):
        prog.update_progressbar(1)

def getKFold(rows):

    """
    param1: pandas.DataFrame

    return : integer 

    Function returns number of kfold to consider for Cross validation on the basis of dataset row counts
    """

    if(rows>100 and rows<500):k=3
    elif(rows>500 and rows <=5000 ):k=5
    elif(rows>5000 and rows <=50000):k=7
    elif rows>50000: k=10
    else:k=3
    return k

def cv_score(model,X,Y,k):

    """
    param1: sklearn/xgboost/lightgbm/catboost model 
    param2: pandas.DataFrame
    param3: pandas.DataFrame/pandas.Series
    param4: integer for kfold 
    return: float

    function gets above mentioned argument and uses cross_val_score to calculate average accuracy on specified kfolds
    """
    n_jobs = 1 if model.__class__.__name__ in ['XGBClassifier','XGBRegressor','LGBMRegressor','LGBMClassifier','CatBoostRegressor','CatBoostClassifier'] else -1
    accuracy = cross_val_score(model, X, Y, cv = k,n_jobs=n_jobs)
    return accuracy.mean()

def sort_score(modelScore):
    """
    param1: Dictionary
    return: Dictionary

    Function returns a sorted dictionary on the basis of values.
    """
    sorted_dict=dict(sorted(modelScore.items(), key=lambda item: item[1],reverse=True))
    return sorted_dict

def eval_model(models,m,X,Y,k,DictionaryClass):
    """
    param1: dictionary : Dictionary of models
    param2: string : model key
    param3: pd.DataFrame 
    param4: pd.Dataframe/pd.Series/numpy.array
    param5: int : cv split
    param6: Class object
    return: float

    Function to fetch cross validation score for specific models from the dictionary.
    If the model/algorithm belong to distance based prediction and training scale the data to speedup the training.
    """
    X = X if m not in ['SVC','NuSVC','LinearSVC','SVR','NuSVR','LinearSVR','KNeighborsClassifier','KNeighborsRegressor','RadiusNeighborsClassifier','RadiusNeighborsRegressor','NearestCentroid'] else scaling_data(X,DictionaryClass)
    if m in ['XGBClassifier','XGBRegressor']: model=models[m][0](verbosity=0)
    elif m in ['CatBoostRegressor','CatBoostClassifier']: model=models[m][0](verbose=False)
    elif m in ['LGBMClassifier','LGBMRegressor']: model=models[m][0](verbose=-1)
    else:model=models[m][0]()
    return cv_score(model,X,Y,k)

def train_on_sample_data(dataframe,target,models,DictionaryClass,stages):
    """
    param1: pandas.DataFrame
    param2: string
    param3: Dictionary (sklearn/xgboost/lightgbm/catboost model object)
    param4: Class object
    return: Dictionary

    Function returns top 5 models with best accuracy in a dictionary.
    The models where accuracy is calculate on sampled data from the dataset.
    Accuracy is calculated using average cross validation score on specified kfold counts.
    """
    rows=dataframe.shape[0]
    sample_rate=round((500+(((rows-500)*0.2)))/rows,1)
    if DictionaryClass.YAML['problem']['type']=="Image Classification":
        dataframe=dataframe.sample(frac=1,random_state=123)
        df=dataframe.sample(frac=sample_rate,random_state=123)
        X,Y=AutoFeatureSelection.get_reshaped_image(df.values)
        models_List=DictionaryClass.image_models
    else:
        df=dataframe.sample(frac=sample_rate,random_state=123)
        X,Y=df.drop(target,axis=1),df[target]
        models_List=models.keys()
    k=getKFold(rows)
    modelScore={}
    prog.create_progressbar(len(models_List),"Quick Search (Stage 1 of {}) :".format(stages))
    try:
        for m in models_List:
            modelScore[m]=eval_model(models,m,X,Y,k,DictionaryClass)
            prog.update_progressbar(1)
    except:
        pass
    prog.update_progressbar(prog.trials)
    prog.close_progressbar()
    clean_dict = {k: modelScore[k] for k in modelScore if not isnan(modelScore[k])}
    return dict(itertools.islice(sort_score(clean_dict).items(), 5))

def train_on_full_data(X,Y,models,best,DictionaryClass,stages):
    """
    param1: pandas.DataFrame
    param2: pandas.Series/Pandas.DataFrame
    param3: Dictionary (sklearn/xgboost/lightgbm/catboost model object)
    param4: Dictionary (sklearn/xgboost/lightgbm/catboost model class names)
    param5: Class object
    return: Dictionary

    Function returns single best model with best accuracy in a dictionary. 
    Accuracy is calculated using average cross validation score on specified kfold counts.
    """
    k=getKFold(X.shape[0])
    modelScore={}
    if DictionaryClass.YAML['problem']['type']=="Image Classification" and len(best)>5:best=DictionaryClass.image_models
    prog.create_progressbar(len(best),"Deep Search (Stage 2 of {}) :".format(stages))
    for m in best:
        modelScore[m]=eval_model(models,m,X,Y,k,DictionaryClass)
        prog.update_progressbar(1)
    prog.update_progressbar(prog.trials)
    prog.close_progressbar()
    clean_dict = {k: modelScore[k] for k in modelScore if not isnan(modelScore[k])}
    return dict(itertools.islice(sort_score(clean_dict).items(), 1))

def train_on_neural(X,Y,ptype,epochs,max_neural_search,stage,ofstage):
    """
    param1: pandas.DataFrame
    param2: pandas.Series/Pandas.DataFrame
    param3: string
    return: keras model

    Function perform neural network model search and tuning using autokeras api and finally returns selected keras model.
    """
    prog.create_progressbar(n_counters=((max_neural_search+2)*epochs),desc="Neural Networks (stage {} of {})".format(stage,ofstage))
    if ptype!="Image Classification":
        clf = ak.StructuredDataClassifier(overwrite=True,max_trials=max_neural_search) if ptype=='Classification' else ak.StructuredDataRegressor(overwrite=True,max_trials=max_neural_search) 
    else: clf= ak.ImageClassifier(overwrite=True,max_trials=max_neural_search)
    clf.fit(X,Y,verbose=0,epochs=epochs,callbacks=[CustomCallback()],batch_size=8)
    loss,acc=clf.evaluate(X,Y,verbose=0)
    y_pred=clf.predict(X,verbose=0)
    if ptype in ["Classification","Image Classification"]:y_pred= y_pred.astype(np.int)
    if ptype=='Regression':acc=r2_score(Y,y_pred)
    results= Tuner.metricResults(Y,y_pred,ptype,prog)
    plot_data=Tuner.prediction_data(Y, y_pred, ptype,prog)
    prog.update_progressbar(prog.trials)
    prog.close_progressbar()
    return (clf,acc,results,plot_data)

def classic_model(ptype,dataframe,target,X,Y,DictClass,modelsList,accuracy_criteria,stages):
    """
    param1: string : problem type either classification or regression
    param2: pd.DataFrame
    param3: string: target column name
    param4: pd.DataFrame
    param5: pd.DataFrame/pd.Series
    param6: Class object
    param7: dictionary: consist of model class and configuration specific to problem type
    param8: float: accuracy criterion to stop further training process/hyper parameters tuning
    param9: int: stage count for progress par visualization
    return: tuple : tuple consisting of various object and results associated to model object

    Funciton perform model search in two stages,if the dataset has more than 500 entries then first fetch top 5 best performing models on 10% sample dataset 
    then run the top 5 models on full dataset to get single best model for hyper parameter tuning.
    The single model is then sent for hyper parameter tuning to tuneModel function of tuner Class.
    """
    if dataframe.shape[0]>500:
        best=train_on_full_data(X,Y,modelsList,train_on_sample_data(dataframe,target,modelsList,DictClass,stages),DictClass,stages)
    else:
        print("Quick Search(Stage 1 of {}) is skipped".format(stages))
        best = train_on_full_data(X,Y,modelsList,DictClass.image_models,DictClass,stages)if ptype=="Image Classification" else train_on_full_data(X,Y,modelsList,modelsList,DictClass,stages)
    
    if ptype=="Image Classification":
        modelResult = Tuner.tune_model(X,Y,best,modelsList,ptype,accuracy_criteria,DictClass,stages)
    else:
        modelResult = Tuner.tune_model(dataframe,target,best,modelsList,ptype,accuracy_criteria,DictClass,stages)
    return modelResult

def classic_model_records(modelData,modelResult,DictClass):
    """
    param1: Class object
    param2: Tuple
    param3: Class object
    return: Class object

    Function extras different data from modelResult tuple and assigns it to Model Class object attributes.
    Then update YAML configuration data
    """
    modelData.model,modelData.params,acc,modelData.metrics,modelData.plot_data = modelResult
    DictClass.addKeyValue('model',{'type': modelData.model.__class__.__name__})
    DictClass.UpdateNestedKeyValue('model','parameters',modelResult[1])
    modelData.scaler=DictClass.Scaler
    return modelData

def neural_model_records(modelData,neural_network,DictClass,ptype,dataframe,target):
    """
    param1: Class object
    param2: Tuples
    param3: Class object
    param4: String : problem Type either Classification or Regression
    param5: pd.DataFrame
    param6: String : Target Columns name
    return: Class object
    Function extras different data from neural_network tuple and assigns it to Model Class object attributes.
    Then update YAML configuration data
    """

    modelData.model,acc,modelData.metrics,modelData.plot_data = neural_network
    DictClass.addKeyValue('model',{'type':'TF'})
    if ptype in ["Classification", "Image Classification"]:
        n_labels=dataframe[target].nunique(dropna=False)
        cls_type='binary' if n_labels<=2 else 'multiclass'
        DictClass.UpdateNestedKeyValue('model','classification_type',cls_type)
        DictClass.UpdateNestedKeyValue('model','save_type',"h5")
    if ptype=='Regression':DictClass.UpdateNestedKeyValue('model','save_type',"pb")
    return modelData

def model_search(dataframe=None,target=None,DictClass=None,disable_colinearity=False,model_types="all",accuracy_criteria=0.99,epochs=20,max_neural_search=10):
    """
    param1: pandas.DataFrame
    param2: string
    param3: Class object
    param4: boolean
    param5: string : Option to selection model selection on either neural networks or Classic GOFAI models
    param6: float : Ranges between 0.1 to 1.0
    param7: int: Number of epoches for Neural Network training
    param8: int: Max number of Neural Network Models to try on.
    return: Class object

    Function first fetches model dictionary which consists of model object and required parameter,
    on the basis of problem type a specific class variable for dictionary is fetched.
    After model search and training the model object and model tuning parameters are assigned to class variable in model class.
    Then update YAML dictionary with appropriate model details such has selected type and parameters.
    Function finally return a model class object.
    """
    global prog
    prog=Progress()
    modelData=Model()
    ptype=DictClass.getdict()['problem']["type"]
    cls_types,prob_types= ["Classification","Image Classification"],["Classification","Regression"]
    if ptype in cls_types :modelsList=classifier_config().models
    else:modelsList= regressor_config().models

    if ptype in prob_types: X,Y=dataframe.drop(target,axis=1),dataframe[target]
    if ptype =="Image Classification":X,Y=AutoFeatureSelection.get_reshaped_image(dataframe.values)
    if ptype in cls_types:modelData.target_encode=DictClass.get_encoded_label()
    if ptype in prob_types: modelData.featureList=dataframe.drop(target,axis=1).columns.to_list()

    if model_types=='classic':
        modelResult=classic_model(ptype,dataframe,target,X,Y,DictClass,modelsList,accuracy_criteria,3)
        DictClass.accuracy=round(modelResult[2],3)
        modelData=classic_model_records(modelData,modelResult,DictClass)
        class_name=modelData.model.__class__.__name__

    elif model_types=='neural':
        if ptype =="Image Classification":X=X.reshape(DictClass.original_shape)
        gpu_num=tf.config.list_physical_devices('GPU')
        if len(gpu_num)==0: print("No GPU was detected on your system. Defaulting to CPU. Consider running on a GPU plan on BlobCity AI Cloud for faster training. https://cloud.blobcity.com")
        neural_network=train_on_neural(X,Y,ptype,epochs,max_neural_search,1,1)
        DictClass.accuracy=round(neural_network[1],3)
        modelData=neural_model_records(modelData,neural_network,DictClass,ptype,dataframe,target)
        class_name="Neural Network"

    elif model_types=='all':
        modelResult=classic_model(ptype,dataframe,target,X,Y,DictClass,modelsList,accuracy_criteria,4)
        if modelResult[2]<accuracy_criteria:
            gpu_num=tf.config.list_physical_devices('GPU')
            if len(gpu_num)==0: print("No GPU was detected on your system. Defaulting to CPU. Consider running on a GPU plan on BlobCity AI Cloud for faster training. https://cloud.blobcity.com")
            neural_network=train_on_neural(X,Y,ptype,epochs,max_neural_search,4,4)
            if modelResult[2]>neural_network[1]:
                DictClass.accuracy=round(modelResult[2],3)
                modelData=classic_model_records(modelData,modelResult,DictClass)
                class_name=modelData.model.__class__.__name__
            else:
                if 'cleaning' in DictClass.YAML.keys():
                    if 'rescale' in DictClass.YAML['cleaning'].keys():
                        del DictClass.YAML['cleaning']['rescale']
                if ptype =="Image Classification":X=X.reshape(DictClass.original_shape)
                DictClass.accuracy=round(neural_network[1],3)
                modelData=neural_model_records(modelData,neural_network,DictClass,ptype,dataframe,target)
                class_name="Neural Network"
        else:
            print("Neural Network Search(Stage 4 of 4) is skipped")
            DictClass.accuracy=round(modelResult[2],3)
            modelData=classic_model_records(modelData,modelResult,DictClass)
            class_name=modelData.model.__class__.__name__

    if not disable_colinearity and ptype!="Image Classification":
        if DictClass.accuracy< 0.8:  print("Recommendation: Disable Colinearity in train function")

    if class_name !="Neural Network":print("Selected Model :- {} \nCV Score : {:.2f}".format(class_name,DictClass.accuracy)) 
    else:print("Selected Model :- {} \nAccuracy Score : {:.2f}".format(class_name,DictClass.accuracy)) 
    
    return modelData


def time_model(dataframe,DictClass,accuracy_criteria=None):
    modelsList=time_config().models
    train_data, test_data=spliter(dataframe)
    modelkey = model_search_time(train_data, test_data)
    modelResult = Tuner.time_tuner(train_data, test_data,modelkey,modelsList)
    
    return modelResult


def model_search_time(train_data, test_data,DictClass=None,accuracy_criteria=None):
    global modelkey
    
    list1=[ARIMA(train_data, exog=None, order=(1, 0, 0)),
          SARIMAX(train_data,order=(1, 0, 0), seasonal_order=(0, 0, 0, 12)),
          ExponentialSmoothing(train_data,initialization_method='estimated'),
          SimpleExpSmoothing(train_data),
          Holt(train_data)] 
    list2={}
    for i in list1:
        try:
            model = i.fit(disp=0)
        except:
            model = i.fit()
        prediction = model.forecast(len(test_data))
        predictions = pd.Series(prediction, index=test_data.index)
        residuals = test_data - predictions
        mse=np.sqrt(np.mean(residuals**2))
        list2[i.__class__.__name__]=mse
    a = sorted(list2.items(), key=lambda x: x[1])
    selected_model =next(iter(a))[0]
    modelkey={selected_model:0}
    return  modelkey
