import pandas as pd
import pickle
import gmlutil as mlu
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, PowerTransformer, StandardScaler

cred = credf('master')

########################### Data Conversion to Numerical Data ###########################
class data_conversion:
    def __init__(self, categorical_list, numerical_list):
        self.categorical_list = categorical_list
        self.numerical_list = numerical_list

    def s3_connection(self):
        s3c = boto3.client(
            's3', 
            region_name = cred.AWS_REGION_NAME,
            aws_access_key_id = cred.AWS_ACCESS_KEY,
            aws_secret_access_key = cred.AWS_SECRET_KEY
            )
        return s3c

    def load_labels(self, bucket_name, directory_name, label_name):
        s3c = self.s3_connection()
        KEY = '{}/labels_{}.pickle'.format(directory_name, label_name)
        try:
            obj = s3c.get_object(Bucket=bucket_name, Key = KEY)
            label_dict = pickle.loads(obj['Body'].read())
        except Exception as err:
            print("Label does not exist for {}...".format(label_name))
            print()
            label_dict = {}
        return label_dict

    def save_labels(self, label_dict, bucket_name, directory_name, label_name):
        s3c = self.s3_connection()
        KEY = '{}/labels_{}.pickle'.format(directory_name, label_name)
        try:
            serialized_df = pickle.dumps(label_dict)
            s3c.put_object(Bucket=bucket_name, Key=KEY, Body=serialized_df)
            print("Label successfully saved for {}...".format(label_name))
            print()
        except Exception as err:
            print("Error while saving a label file for {}...".format(str(err)))
            print()         

    def data_conversion_cat_onehot(self, df):
        df_num = df[self.numerical_list]
        if self.categorical_list != []:
            df_cat = df[self.categorical_list]
            df_cat = pd.get_dummies(df_cat)
            df = pd.concat([df_cat, df_num], axis=1)
        else:
            df = df_num
        return df

    def data_conversion_cat(self, df, bucket_name, directory_name, label_name):
        df_num = df[self.numerical_list]
        label_dict = self.load_labels(bucket_name, directory_name, label_name)
        if self.categorical_list != []:
            print("Detected categorical list for sustainable growth...")
            df_cat = df[self.categorical_list]
            if label_dict == {}:
                for category in self.categorical_list:
                    label_encoder = LabelEncoder()
                    df_cat.loc[:,category] = label_encoder.fit_transform(df_cat.loc[:,category]) # use label_encoder.inverse_transform(data) to go back to original labels
                    label_dict[category] = label_encoder
                self.save_labels(label_dict,  bucket_name, directory_name, label_name)
            else:
                for category in self.categorical_list:
                    label_encoder = label_dict[category]
                    df_cat.loc[:,category] = label_encoder.transform(df_cat.loc[:,category])
            df = pd.concat([df_cat, df_num], axis=1)
        else:
            print("There is no categorical list for the data...")
            df = df_num
        return df, label_dict

    def data_conversion_num(self, df, bucket_name, directory_name, label_name, scaler_type = "minmax"):
        categorical_list = list(df.columns)
        categorical_list = [category for category in categorical_list if category not in self.numerical_list]
        df_cat = df[categorical_list]
        df_num = df[self.numerical_list]
        label_dict = self.load_labels(bucket_name, directory_name, label_name)
        if self.numerical_list != []:
            print("Detected numerical list for the data...")
            if label_dict == {}:
                if scaler_type == "minmax":
                    scaler = MinMaxScaler()
                elif scaler_type == "power":
                    scaler = PowerTransformer()
                else:
                    scaler = StandardScaler()               
                scaler.fit_transform(df_num)
                self.save_labels(scaler,  bucket_name, directory_name, label_name)
            else:
                scaler = label_dict
                scaler.transform(df_num)
        else:
            print("There is no numerical list for sustainable growth...")
            df = df_cat
        df = pd.concat([df_cat, df_num], axis=1)
        return df

########################### Data Preparation ###########################
class data_preparation:
    def __init__(self):
        pass

    def train_testsets(self, df, target_label, test_size=0.3, oversampling="no", oversampling_strategy="minority", undersampling="no", undersampling_strategy="majority"):
        y = df[target_label]
        X = df.drop(columns=[target_label])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        if oversampling.lower() == "yes":
            if oversampling_strategy == "minority":
                over = SMOTE(sampling_strategy='minority')
            else:
                over = SMOTE(sampling_strategy='auto')
        if undersampling.lower() == "yes":
            if undersampling_strategy == "majority":
                under = RandomUnderSampler(sampling_strategy = 'majority')
            else:
                under = RandomUnderSampler(sampling_strategy = 'auto')
        if oversampling.lower() == "yes" and undersampling.lower() == "yes":
            steps = [('o', over), ('u', under)]
            pipeline = Pipeline(steps=steps)
            X_train, y_train = pipeline.fit_resample(X_train, y_train)
        elif oversampling.lower() == "yes" and undersampling.lower() != "yes":
            steps = [('o', over)]
            pipeline = Pipeline(steps=steps)
            X_train, y_train = pipeline.fit_resample(X_train, y_train)
        elif oversampling.lower() != "yes" and undersampling.lower() == "yes":
            steps = [('u', under)]
            pipeline = Pipeline(steps=steps)
            X_train, y_train = pipeline.fit_resample(X_train, y_train)
        return X_train, X_test, y_train, y_test
