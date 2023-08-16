# from pandas.core.strings import str_count
import boto3
import hana_ml
import io
import json
import numpy as np
import pandas as pd
import sys
import time
from fuzzywuzzy import fuzz
from io import BufferedReader, TextIOWrapper
from pytrends.request import TrendReq
from types import SimpleNamespace

limit = np.int64(10**9 * 2.1)
sys.setrecursionlimit(limit)

run_mode = "cloud"
if run_mode == "local":
    path_to_folder = '../'
    sys.path.append(path_to_folder)
    import credentials as cred
else:
    def credf(keys):
        client = boto3.client('secretsmanager', region_name = 'us-west-2')
        if keys == "redshift":
            response = client.get_secret_value(SecretId='ejgallo-prophet-redshift')
            database_secrets = json.loads(response['SecretString'])
            cred = SimpleNamespace(**database_secrets)
        else:
            response = client.get_secret_value(SecretId='ejgallo-prophet-masterkeys')
            database_secrets = json.loads(response['SecretString'])
            cred = SimpleNamespace(**database_secrets)
        return cred
    cred = credf('master')
    credr = credf('redshift')

bucket_name = 'ejgallo-lake-sales-dev'
benchmark_acv_str = 'prophet/Data_Acquisition/source_data/Archive/2021/benchmark/data/acv_curves.csv'
benchmark_geo_str = 'prophet/Data_Acquisition/source_data/Archive/2021/benchmark/data/geo_codes.csv'
brand_standards_str = 'prophet/Deployment/Auxillary_Functions/prime_directive/off_brand_standards_Q2.csv'
upc_tier_str = 'prophet/Data_Acquisition/source_data/Archive/2021/benchmark/data//UPC_Tier_Dict.csv'

########################### Data Extraction ###########################
class data_extraction:
    def __init__(self):
        pass

    def hana_connection(self):
        conn = hana_ml.dataframe.ConnectionContext(
            address= cred.HANA_ADDRESS,
            port=cred.HANA_PORT,
            user=cred.HANA_USER,
            password=cred.HANA_PASSWORD
            )
        return conn

    def s3_connection(self):
        s3c = boto3.client(
            's3', 
            region_name = cred.AWS_REGION_NAME,
            aws_access_key_id = cred.AWS_ACCESS_KEY,
            aws_secret_access_key = cred.AWS_SECRET_KEY
            )
        return s3c

    def sg_upload_to_s3(self, df, bucket_name, file_name, index=False):
        role = get_execution_role()
        sess = sagemaker.Session()
        region = boto3.session.Session().region_name
        sm = boto3.Session().client('sagemaker')
        df.to_csv('{}'.format(file_name), index=index)
        data_location = sess.upload_data(path='data', bucket=bucket_name, key_prefix='data')
        print("Uploading is successful...")

    def sg_reading_in_from_s3(self, bucket_name, file_name,dtypes = None):
        role = get_execution_role()
        data_location = 's3://{}/{}'.format(bucket_name, file_name)
        df = pd.read_csv(data_location, low_memory=False, dtype = dtypes) # , on_bad_lines='skip')
        return df

    def lc_upload_to_s3(self, df, bucket_name, file_name, index=False):
        s3c = self.s3_connection()
        KEY = '{}'.format(file_name)
        df.to_csv('buffer', index=index)
        s3c.upload_file(Bucket = bucket_name, Filename = 'buffer', Key = KEY)
        print("Uploading is successful...")

    def lc_reading_in_from_s3(self, bucket_name, file_name, dtypes = None):
        s3c = self.s3_connection()
        KEY = '{}'.format(file_name)
        obj = s3c.get_object(Bucket=bucket_name, Key = KEY)                         
        df = pd.read_csv(io.BytesIO(obj['Body'].read()) , encoding='utf8', low_memory=False, dtype = dtypes) # , on_bad_lines='skip')
        return df

    # def lc_reading_in_from_s3(self, bucket_name, file_name, dtypes = None):
    #     s3c = self.s3_connection()
    #     KEY = '{}'.format(file_name)
    #     obj = s3c.get_object(Bucket=bucket_name, Key = KEY)
    #     streaming_body = obj['Body']
    #     content_len = obj['ContentLength']
    #     buffered_io = S3StreamingBodyIO(streaming_body._raw_stream, content_len)
    #     df = pd.read_csv(io.BytesIO(buffered_io.read()), encoding='ISO-8859-1', low_memory=False, dtype = dtypes) # on_bad_lines='skip')
    #     return df

    def lcm_upload_to_s3(self, bucket, file_name):
        minio = self.minio_connection()
        print("Saving... data in {} at {}".format(bucket, file_name))
        print()
        try:
            minio.fput_object(bucket, file_name, file_name, content_type="application/csv")
            return True
        except ResponseError as err:
            print(err)
            return False

    def lcm_reading_in_from_s3(self, bucket, file_name):
        minio = self.minio_connection()
        print("Loading... data from {} at {}".format(bucket, file_name))
        print()
        try:
            minio.fget_object(bucket, file_name, file_name)
            return True
        except ResponseError as err:
            print(err)
            return False

    def rs_data_connection(self):
        engine_string = 'redshift+psycopg2://{}:{}@data-lake.cwjgbxpbqebs.us-west-2.redshift.amazonaws.com:5439/prophet'.format(credr.username, credr.password)
        conn = sa.create_engine(engine_string)
        return conn

    def rs_data_extraction_str(self, table_name, schema_name='prophet'):
        metadata = MetaData()
        conn = self.rs_data_connection()
        dt = Table(table_name, metadata, autoload=True, autoload_with=conn, schema=schema_name)
        df_columns = dt.columns.keys()
        return dt, conn, df_columns

    def rs_data_insertion(self, df, table_name, schema_name='prophet'):
        conn = self.rs_data_connection()
        df_length = len(df)
        cindex = 0
        nindex = 100
        while cindex < df_length:
            if cindex < df_length:
                if nindex >= df_length:
                    nindex = df_length
                df_portion = df[cindex:nindex]
                print("Inserting {}-{}th data rows...".format(cindex, nindex))
                df_portion.to_sql(table_name, conn, index=False, if_exists='append', schema=schema_name) ##### change to append
                cindex += 100
                nindex += 100   
        print("Data successfully inserted...")

    def rs_data_deletion(self, table_name, schema_name='prophet'):
        metadata = MetaData()
        conn = self.rs_data_connection()
        dt = Table(table_name, metadata, autoload=True, autoload_with=conn, schema=schema_name)
        delete_stmt = dt.delete()
        results = conn.execute(delete_stmt)
        print("The number of rows deleted are {}...".format(results.rowcount))    


    # PYTRENDS FUNCTION THAT GETS TRENDING CITIES BASED ON KEYWORD(BRAND)
    def get_google_city(self, keyword):
        """generates the google trends piece from a keyword that is entered(benchmark)
        Args:
            keyword (str): planning brand that is entered in order to generate city list
        Returns:
            df: cities that are trending for the keyword
        """
        print('gathering google trends data')
        pytrends = TrendReq(hl='en-US')
        # Building our payload for the trends query
        cat = '71'
        geo = 'US'
        gprop = ''
        keywords = [keyword]
        timeframe = 'today 3-m'
        # Pytrends function to get google data
        pytrends.build_payload(keywords, cat,
                           timeframe,
                           geo,
                           gprop)
        try:
            output= pytrends.interest_by_region(resolution='DMA', inc_low_vol=True, inc_geo_code=True)
            city_queries = output[output[keywords[0]] > 30]
            city_queries['Google'] = 'Y'
            city_queries = city_queries[['geoCode','Google']]
        except:
            city_queries = pd.DataFrame([], columns=['geoCode','Google'])
        time.sleep(1)
        return city_queries

    # READING IN ACV DATA
    def read_acv(self):
        s3c = self.s3_connection()
        """gets our acv curves from s3 in order to run the distributor path option for upcs
        Returns:
             df: acv_df is the accounts with the respective net list running percent for each category and tier 
        """ 
        bucket=bucket_name
        key = benchmark_acv_str
        obj = s3c.get_object(Bucket= bucket , Key = key)
        acv_df = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8',low_memory = False)
        columns = ['9L VOLUME','PHYS VOLUME','NET LIST DOLLARS']
        for column in columns:
            acv_df[column] = round(acv_df[column],2)
        columns = ['nl_percent','nl_running_percent']
        for column in columns:
            acv_df[column] = round(acv_df[column],4)
        acv_df['Rtl_Acct_ID'] = acv_df['Rtl_Acct_ID'].astype(int)
        acv_df['geoCode'] = acv_df['geoCode'].astype(str)
        acv_df['concat'] = acv_df['Mkt_Grp_State'] + ' ' + acv_df['Acct_City']
        acv_df['concat'] = acv_df['concat'].astype(str)
        unique_citystates = acv_df[['Mkt_Grp_State','Acct_City','concat']].drop_duplicates()
        # Read in geocodes and fuzzy match them--> need to do ts cause some cities have different spellings from the hana side
        key = benchmark_geo_str
        obj = s3c.get_object(Bucket= bucket , Key = key)
        geo_codes = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8',low_memory = False)
        geo_codes['concat'] =geo_codes['Mkt_Grp_State'] + ' ' + geo_codes['City']
        matchers = {}
        for j in unique_citystates['concat']:
            for i in geo_codes['concat']:
                if (j[:2] == i[:2]):
                    if fuzz.ratio(i,j) > 90:
                        matchers[j] = i
        acv_df['new_concat'] = acv_df['concat'].map(matchers)
        acv_df_new = acv_df.merge(geo_codes[['geoCode','concat']],left_on = 'new_concat',right_on = 'concat',how='left')
        acv_df_new['new_concat'] = acv_df_new['new_concat'].astype(str)
        acv_df_new = acv_df_new.drop(['geoCode_x','concat_x','concat_y','new_concat','geoCode_x'],axis = 1)
        acv_df_new = acv_df_new.rename(columns = {'geoCode_y':'geoCode'})
        acv_df_new['geoCode'] =acv_df_new['geoCode'].astype(str)
        acv_df_new['State'] = np.where(acv_df_new['State'] == 'New Mexico','New_Mexico',acv_df_new['State'])
        acv_df_new['State'] = np.where(acv_df_new['State'] == 'DC','District of Columbia',acv_df_new['State'])
        return acv_df_new

    # GETTING OUR UPCS DF WCH CONTAINS CATEGORY AND PRICE TIER FOR INDIVIDUAL ITEMS
    def read_upc_df(self):
        s3c = self.s3_connection()
        """gets our upc df: a dataframe with all upcs and thier corresponding price tier and category
        Returns:
            [df]: [upc_df is all upcs and their corresponding price tier and category: to be merged onto acv df]
        """
        bucket=bucket_name
        key = upc_tier_str
        obj = s3c.get_object(Bucket= bucket , Key = key)
        upc_df = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8',low_memory = False)
        # Add leading zeros to UPC to match Gallo data
        upc_df['UPC'] = upc_df['UPC'].astype(int)
        upc_df['UPC'] = upc_df['UPC'].astype(str).str.rjust(12, "0")
        return upc_df


########################### Buffer Streaming Processing ###########################

class S3StreamingBodyIO(BufferedReader):
    def __init__(self, buffer, content_len):
        self.buffer = buffer
        self.content_len = content_len
    def read(self, *args):
        MAX_SSL_CONTENT_LENGTH = limit
        size = self.content_len
        if size > MAX_SSL_CONTENT_LENGTH:
            data_out = bytearray()
            remaining_size = size
            i = 1
            while remaining_size > 0:
                print("iteration {} and remaining size {}...".format(str(i), remaining_size))
                chunk_size = min(remaining_size, MAX_SSL_CONTENT_LENGTH)
                data_out += self.buffer.read(chunk_size)
                remaining_size = remaining_size - chunk_size
                i += 1
            return data_out
        else:
            return self.buffer.read(size)


########################### Prime Directive Processing ###########################

class prime_directive:
    def __init__(self, change_names = {'FINE_WINE':'Fine_Wine_Acct_Flag', 'INFLUENCER':'Fine_Wine_Inflncr_Acct_Flag','ICON':'Fine_Wine_Icon_Acct_Flag'}):
        self.change_names = change_names

    def search_func(self, upc_value, bucket_name, file_name, platform='cloud'):
        de = data_extraction()
        if platform == "sagemaker":
            brand_standards = de.sg_reading_in_from_s3(bucket_name, file_name,dtypes = {'UPC':str})
        elif platform == "local":
            brand_standards = pd.read_csv("../data/off_brand_standards.csv", low_memory=False, dtypes = {'UPC':str})
        else:
            brand_standards = de.lc_reading_in_from_s3(bucket_name, file_name, dtypes = {'UPC':str})
        brand_standards['UPC'] = brand_standards['UPC'].astype(str).str.zfill(12)
        upc_search = brand_standards[brand_standards['UPC'] == upc_value].drop_duplicates()
        try:
            upc_search = upc_search.rename(columns = self.change_names)
            upc_search.columns = map(str.lower, upc_search.columns)
        except:
            print("No such columns exist...")
            print()
        search_dict = upc_search.to_dict('records')[0]
        return search_dict

    def standards_check(self, dictionary, zone, channel, icon, influencer, finewine, gsp):
        #zone checker
        check_value = 0
        if dictionary['segmentation'] == 'BROAD':
            return 'Y'
        else:
            check_value += int(dictionary[zone.lower()])
            #channel of dist checker
            check_value += int(dictionary[channel.lower()])
            #icon checker
            #influencer checker
            if dictionary['fine_wine_acct_flag'] == 1:
                check_value += finewine
            elif dictionary['fine_wine_inflncr_acct_flag'] == 1:
                check_value += influencer
            #fine wine checker
            elif dictionary['fine_wine_icon_acct_flag'] == 1:
                check_value += icon
            #we're going to vet liquor items
            if (dictionary['gsp'] == 1) and (dictionary['not_gsp'] == 1) :
                check_value += 1
            elif dictionary['gsp'] == 1:
                check_value += gsp
            elif dictionary['not_gsp'] == 1:
                check_value -= gsp
            if (dictionary['segmentation'] == 'GSP') and (check_value == 3) and (gsp == 1):
                return 'Y'
            else:
                if check_value == 4:
                    return 'Y'
                else:
                    return 'N'

    def create_score(self, check_value):
        if check_value == 'Y':
            return 1
        elif check_value == 'N':
            return 0
        elif  check_value in ['Gold','Silver']:
            return 1
        else:
            return 0

    def brand_standard_process(self, df):
        if len(df) != 0:
            #what Patrick is changing
#             df.columns = df.columns.str.lower()
            df['UPC'] = df['UPC'].astype(str).str.zfill(12)
            try:
                upc_list = list(set(df['UPC']))
            except:
                upc_list = list(set(df['UPC']))
            brand_standard_list = []
            standard_change = ['Fine_Wine_Acct_Flag','Fine_Wine_Inflncr_Acct_Flag', 'Fine_Wine_Icon_Acct_Flag',
                   'Prem_Spirit_Acct_Flag', 'Whiskey_Segment']
            standard_change = [element.lower() for element in standard_change]
            store_list = ['GROCERY','LIQUOR','CONVENIENCE','DRUG','MASS MERCHANDISER','ALL OTHER-OFF SALE','DOLLAR','CLUB']
            for upc in upc_list:
                try:
                    search_dict = self.search_func(upc, bucket_name, brand_standards_str)
                    upc_df = df[df['UPC']==upc]
                    upc_df = upc_df.rename(columns = self.change_names)
                    upc_df.columns = map(str.lower, upc_df.columns)
                    for i in standard_change:
                        upc_df[i] = upc_df[i].apply(lambda x: self.create_score(x))
                    upc_df['gsp'] = np.where((upc_df['prem_spirit_acct_flag'] ==1) | (upc_df['whiskey_segment'] == 1),1,0)
                    upc_df['zone_check'] = np.where(upc_df['key_acct_zone'].str.contains('1|2|3'),'zone1_3','zone4_5')
                    upc_df = upc_df[upc_df['channel_of_distribution'].isin(store_list)]
                    upc_df['standards_check'] = upc_df.apply(lambda x: self.standards_check(search_dict,x['zone_check'],x['channel_of_distribution'],
                                                                   x['fine_wine_icon_acct_flag'],x['fine_wine_inflncr_acct_flag'],
                                                                  x['fine_wine_acct_flag'],x['gsp']), axis = 1)
                    upc_df = upc_df[upc_df['standards_check'] == 'Y']
                except Exception as err:
                    print('passing this upc {}... {}...'.format(upc, err))
                    continue
                brand_standard_list.append(upc_df)
            try:
                brand_standard_df = pd.concat(brand_standard_list)
            except:
                print("Concat failed...")
                brand_standard_df = pd.DataFrame([], columns=df.columns)
        else:
            print("Data Empty...")
            brand_standard_df = df.copy()
        return brand_standard_df

########################### Data Cleaning ###########################
class data_cleaning:
    def __init__(self):
        pass
    def dec_to_perc(self, num):
        perc = str(round(num * 100, 2)) + "%"
        return perc
    def remove_decimal(self, word):
        new_word =  re.sub('(\.0+)','',word)
        return new_word
    def oned_cross_merging(self, df1, df2):
        df1['key'] = 1
        df2['key'] = 1
        df = pd.merge(df1, df2, on ='key').drop("key", 1)
        return df
    def clean_upc(self, upc):
        """need to clean some upcs in order to account for zfill and other objects 
        Args:
            upc ([str]): [unique identifier of item]
        Returns:
            [str]: [refurbished upc item]
        """
        if upc[0] != '0':
            upc = '0' + upc[:-1]
            return upc
        else:
            return upc

