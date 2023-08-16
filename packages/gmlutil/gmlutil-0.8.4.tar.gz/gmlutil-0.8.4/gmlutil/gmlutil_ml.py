import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
# import umap.umap_ as umap

from geopandas import GeoDataFrame
from geopandas import points_from_xy
from kmodes.kmodes import KModes
from kmodes.kprototypes import KPrototypes
from numpy import mean, std
from scipy.cluster.hierarchy import linkage, dendrogram
from shapely.geometry import mapping, Point, Polygon
from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, StackingClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering, DBSCAN, Birch
from sklearn.manifold import TSNE
from sklearn.mixture import GaussianMixture
from statsmodels.tsa.stattools import adfuller
from xgboost import XGBClassifier

########################### Data Visualization ###########################
class data_visualization:
    def __init__(self):
        pass

#     def plot_confusion(self, model, X, y, class_names, normalized='true'):
#         titles_options = [("Confusion matrix, without normalization", None),
#                           ("Normalized confusion matrix", normalized)]
#         for title, normalize in titles_options:
#             display = plot_confusion_matrix(model, X, y,
#                                          display_labels=class_names,
#                                          cmap=plt.cm.Blues,
#                                          normalize=normalize)
#             display.ax_.set_title(title)
#             print(title)
#             print(display.confusion_matrix)
#         plt.show()

    def data_visualization(self, df, column_list, removal_list, title, x_axis):
        try:
            df = df.drop(removal_list, axis=1)
        except:
            pass
        sqrt_num = int(math.sqrt(len(column_list)))
        if sqrt_num ** 2 < len(column_list):
            plot_size = sqrt_num + 1
        else:
            plot_size = sqrt_num
        fig, axes = plt.subplots(plot_size, plot_size, figsize=(len(column_list)*5, len(column_list)*5))
        fig.suptitle(title)
        i, j = 0, 0
        for column in column_list:
            df[column] = df[column].astype(int)
            df[x_axis] = df[x_axis].astype(int)
            x = x_axis
            axes[i, j].set_title(column)
            sns.lineplot(ax=axes[i, j],data=df,x=x,y=column,lw=1)
    #         sns.lineplot(ax=axes[i, j],data=df,x='Month_Day_Time',y=column,
    #                      hue='City',lw=1)
    #         sns.lineplot(ax=axes[i, j],data=df,x='Month_Day_Time',y=column,
    #                      hue="chain_store",estimator=None)
            i += 1
            if i == plot_size:
                i = 0
                j += 1

    def elbow_graph(self, df, model_name='KMEANS', range_start=2, range_end=11):
        distortions = []
        for i in range(range_start, range_end):
            print("Fitting cluster {}...".format(i))
            if model_name == "KMEANS":
                km = KMeans(n_clusters=i, init='random',n_init=10,max_iter=100,tol=1e-04)
                km.fit(df)
                distortions.append(km.inertia_)
            elif model_name == "KPROTO":
                km = KPrototypes(n_clusters=i, init='Huang',n_init=10,max_iter=100,n_jobs=-1)
                km.fit(df, categorical=list(range(len(categorical_list))))
                distortions.append(km.cost_)
        plt.plot(range(range_start,range_end), distortions, marker='o')
        plt.xlabel('Number of clusters')
        plt.ylabel('Distortion')
        plt.show()

    def pca_graph(self, df, pca_percent=0.99):
        df = df.fillna(0)
        model_pca = PCA(pca_percent)
        pca_transformed = model_pca.fit_transform(df)
        components = model_pca.components_
        colors = ["C" + str(index) for index,_ in enumerate(components[0])]
        print("Explained Variance Ratios for PC1 and PC2: ", model_pca.explained_variance_ratio_)
        print()
        labels = {
            str(i): f"PC {i+1} ({var:.1f}%)"
            for i, var in enumerate(model_pca.explained_variance_ratio_ * 100)
        }
        fig = px.scatter_matrix(
            pca_transformed,
            labels=labels,
            dimensions=components,
            color=colors)
        fig.update_traces(diagonal_visible=False)
        fig.show()

    def tsne_graph(self, df):
        model_tsne = TSNE(learning_rate=100)
        model_name = "TSNE"
        transformed = model_tsne.fit_transform(df)
        x_axis = transformed[:, 0]
        y_axis = transformed[:, 1]
        plt.scatter(x_axis, y_axis)
        print(model_name)
        plt.show()

#     def umap_graph(self, df):
#         numerical_df = df.select_dtypes(exclude='object')
#         for c in numerical_df.columns:
#             pt = PowerTransformer()
#             numerical_df.loc[:, c] = pt.fit_transform(np.array(numerical_df[c]).reshape(-1, 1))
#         categorical_df = df.select_dtypes(include='object')
#         categorical_df = pd.get_dummies(categorical_df)
#         categorical_weight = len(df.select_dtypes(include='object').columns) / len(df.columns)
#         fit1 = umap.UMAP(metric='l2').fit(numerical_df)
#         fit2 = umap.UMAP(metric='dice').fit(categorical_df)
#         intersection = umap.general_simplicial_set_intersection(fit1.graph_, fit2.graph_, weight=categorical_weight)
#         intersection = umap.reset_local_connectivity(intersection)
#         embedding = umap.simplicial_set_embedding(fit1._raw_data, intersection, fit1.n_components, 
#                                                         fit1._initial_alpha, fit1._a, fit1._b, 
#                                                         fit1.repulsion_strength, fit1.negative_sample_rate, 
#                                                         200, 'random', np.random, fit1.metric, 
#                                                         fit1._metric_kwds, False)
#         plt.figure(figsize=(20, 10))
#         plt.scatter(*embedding.T, s=2, cmap='Spectral', alpha=1.0)
#         plt.show()


########################### Model Training ###########################
class model_training:
    def __init__(self):
        pass

    def load_model_trained(self, bucket_name, directory_name, model_name, label_name):
        s3c = boto3.client(
                's3', 
                region_name = cred.AWS_REGION_NAME,
                aws_access_key_id = cred.AWS_ACCESS_KEY,
                aws_secret_access_key = cred.AWS_SECRET_KEY
            )
        KEY = '{}/{}_model_trained_{}.pickle'.format(directory_name, model_name, label_name)
        try:
            obj = s3c.get_object(Bucket=bucket_name, Key = KEY)
            model_trained = pickle.loads(obj['Body'].read())
            return model_trained
        except Exception as err:
            print("Loading failed for {}...".format(str(err)))
            print()
    def save_model_trained(self, model_trained, bucket_name, directory_name, model_name, label_name):
        s3c = boto3.client(
                's3', 
                region_name = cred.AWS_REGION_NAME,
                aws_access_key_id = cred.AWS_ACCESS_KEY,
                aws_secret_access_key = cred.AWS_SECRET_KEY
            )
        KEY = '{}/{}_model_trained_{}.pickle'.format(directory_name, model_name, label_name)
        try:
            serialized_df = pickle.dumps(model_trained)
            s3c.put_object(Bucket=bucket_name, Key=KEY, Body=serialized_df)
            print("Model Successfully Saved...")
            print()
        except Exception as err:
            print("Error while saving a pickle file for {}...".format(str(err)))
            print()

    def ba_model(self, X_train, X_test, y_train, y_test):
        model_trained = BaggingClassifier()
        cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=2)
        n_scores = cross_val_score(model_trained, X_train, y_train, scoring='accuracy', cv=cv, error_score='raise')
        print('> Bagging Accuracy: %.3f (%.3f)' % (mean(n_scores), std(n_scores)))
        print()
        model_trained.fit(X_train, y_train)
        prediction = model_trained.predict(X_test)
        print(classification_report(y_test, prediction))
        return model_trained

    def rf_model(self, X_train, X_test, y_train, y_test):
        model_trained = RandomForestClassifier()
        cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        n_scores = cross_val_score(model_trained, X_train, y_train, scoring='accuracy', cv=cv, error_score='raise')
        print('> Random Forest Accuracy: %.3f (%.3f)' % (mean(n_scores), std(n_scores)))
        print()
        model_trained.fit(X_train, y_train)
        prediction = model_trained.predict(X_test)
        print(classification_report(y_test, prediction))
        return model_trained

    def build_stacking(self):
        level0 = list()
        level0.append(('lr', LogisticRegression()))
        level0.append(('knn', KNeighborsClassifier()))
        level0.append(('cart', DecisionTreeClassifier()))
        level0.append(('svm', SVC()))
        level0.append(('bayes', GaussianNB()))
        level1 = LogisticRegression()
        model = StackingClassifier(estimators=level0, final_estimator=level1, cv=5)
        return model

    def model_stacking(self):
        models = dict()
        models['lr'] = LogisticRegression(max_iter=1000)
        models['knn'] = KNeighborsClassifier()
        models['cart'] = DecisionTreeClassifier()
        models['svm'] = SVC()
        models['bayes'] = GaussianNB()
        models['stacking'] = self.build_stacking()
        return models

    def evaluate_stacking(self, model, X, y):
        cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        scores = cross_val_score(model, X, y, scoring='accuracy', cv=cv, error_score='raise')
        return scores

    def st_model(self, X_train, X_test, y_train, y_test):
        models = self.model_stacking()
        model_name = "Stacking"
        results, names = list(), list()
        for name, model in models.items():
            scores = self.evaluate_stacking(model, X_train, y_train)
            results.append(scores)
            names.append(name)
            print('> %s %.3f (%.3f)' % (name, mean(scores), std(scores)))
        print()
        plt.boxplot(results, labels=names, showmeans=True)
        plt.show()
        model_trained = models['stacking']
        model_trained.fit(X_train, y_train)
        print()
        prediction = model_trained.predict(X_test)
        print(classification_report(y_test, prediction))
        return model_trained

    def xgb_model(self, X_train, X_test, y_train, y_test):
        model_trained = XGBClassifier()
        model_name = "XGB"
        cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        n_scores = cross_val_score(model_trained, X_train, y_train, scoring='accuracy', cv=cv)
        print('> XGB Accuracy: %.3f (%.3f)' % (mean(n_scores), std(n_scores)))
        print()
        model_trained.fit(X_train, y_train)
        print()
        prediction = model_trained.predict(X_test)
        print(classification_report(y_test, prediction))
        return model_trained

    def xgb_feature(self, model, column_names):
        column_names = list(column_names)
        importance = model.feature_importances_
        print()
        max_importance_index = {}
        for i,v in enumerate(importance):
            print('Feature: {}, Score: {}'.format(column_names[int(i)],round(v,5)))
            max_importance_index[i] = v
        max_importance_index = dict(sorted(max_importance_index.items(), key=lambda item: item[1], reverse=True))
        plt.bar([x for x in range(len(importance))], importance)
        plt.show()
        return max_importance_index

    def kmeans_model(self, df, n_clusters=4, algorithm='elkan'):
        model_trained = KMeans(algorithm=algorithm, n_clusters=n_clusters)
        model_trained.fit(df)
        return model_trained

    def birch_model(self, df, threshold=0.01, n_clusters=4):
        model_trained = Birch(threshold=threshold, n_clusters=n_clusters)
        model_trained.fit(df)
        return model_trained

    def db_model(self, df):
        model_trained = DBSCAN()
        model_trained.fit(df)
        for i in range(0, df.shape[0]):
            if model_trained.labels_[i] == 0:
                c1 = plt.scatter(df[i, 0], df[i, 1], c='r', marker='+')
            elif model_trained.labels_[i] == 1:
                c2 = plt.scatter(df[i, 0], df[i, 1], c='g', marker='o')
            elif model_trained.labels_[i] == -1:
                c3 = plt.scatter(df[i, 0], df[i, 1], c='b', marker='*')
        plt.legend([c1, c2, c3], ['Cluster 1', 'Cluster 2', 'Noise'])
        plt.title('DBSCAN finds 2 clusters and Noise')
        plt.show()
        return model_trained

    def kp_model(self, df, n_clusters=4, init='Cao'):
        categorical_columns = df.select_dtypes(include='object').columns
        categorical_list = []
        for col_name in categorical_list:    
            index_no = df.columns.get_loc(col_name)
            categorical_list.append(index_no)
        model_trained = KPrototypes(n_clusters=n_clusters, init=init)
        model_trained.fit(df, categorical=categorical_list)
        return model_trained

########################### Polygon Map ###########################
class polygon_map:
    def __init__(self):
        pass
    def Left_index(self, points):
        minn = 0
        for i in range(1,len(points)):
            if points[i].x < points[minn].x:
                minn = i
            elif points[i].x == points[minn].x:
                if points[i].y > points[minn].y:
                    minn = i
        return minn

    def orientation(self, p, q, r):
        val = (q.y - p.y) * (r.x - q.x) - \
            (q.x - p.x) * (r.y - q.y)
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def convexHull(self, points, n):
        if n < 3:
            return
        l = self.Left_index(points)
        hull = []
        p = l
        q = 0
        while(True):
            hull.append(p)
            q = (p + 1) % n
            for i in range(n):
                if(self.orientation(points[p],
                            points[i], points[q]) == 2):
                    q = i
            p = q
            if(p == l):
                break
        lon = []
        lat = []
        for each in hull:
            lon.append(points[each].x)
            lat.append(points[each].y)
        return lon, lat

    def cluster_creator(self, df, index_list, eps, min_samples, metric, metric_params, algorithm, leaf_size, p, n_jobs):
        model = DBSCAN(eps=eps, min_samples=min_samples, metric=metric, metric_params=metric_params, algorithm=algorithm, leaf_size=leaf_size, p=p, n_jobs=n_jobs)
        prediction = model.fit_predict(df[index_list])
        pred = pd.DataFrame(prediction, columns=['cluster_group'])
        df = df.join(pred)
        return df

    def polygon_creator(self, df, longitude, latitude):
        lon = df[longitude]
        lat = df[latitude]
        df = GeoDataFrame(df, geometry=points_from_xy(lon, lat))
        df.rename(columns={"geometry": "points"}, inplace=True)
        points = [Point(x,y) for x,y in zip(lon, lat)]
        new_lon, new_lat = self.convexHull(points, len(points))
        polygon_geom = [Polygon(zip(new_lon, new_lat))]*len(df)
        crs = 'epsg:4326'
        df = GeoDataFrame(df, crs=crs, geometry=polygon_geom)  
        return df
        
    def map_creator(self, df, index_list, eps=0.5, min_samples=5, metric='euclidean', metric_params=None, algorithm='auto', leaf_size=30, p=None, n_jobs=None):
        df = self.cluster_creator(df, index_list, eps=eps, min_samples=min_samples, metric=metric, metric_params=metric_params, algorithm=algorithm, leaf_size=leaf_size, p=p, n_jobs=n_jobs)
        n_clusters = len(set(df['cluster_group']))
        df_list = []
        for cluster in range(n_clusters):
            part_df = df[df['cluster_group']==cluster]
            part_df = self.polygon_creator(part_df, 'Long', 'Lat')
            df_list.append(part_df)
        total_df = pd.concat(df_list, ignore_index=False)
        return total_df

    def boundary_test(self, acct_name, polygon, points):
        if polygon.contains(points):
            print("{} is in the polygon...".format(acct_name))
        elif polygon.touches(points):
            print("{} is in the polygon...".format(acct_name))
        else:
            print("Not in the polygon...")


########################### Time Series Models ###########################
class time_series_models:
    def __init__(self):
        pass

    def arima_stationarity_test(self, df,column):
        pre_result = adfuller(df[column].dropna())
        k = pre_result[2]
        if pre_result[1] >= 0.05:
            significant_list = {}
            for i in range(1,k): 
                df['Seasonal First Difference'] = df[column] - df[column].shift(i)
                result=adfuller(df['Seasonal First Difference'].dropna())        
                if result[1] < 0.05:
                    significant_list[i] = result[1]
            if significant_list != {}:
                best_key = min(significant_list, key=significant_list.get)
                print(significant_list)
                df['Seasonal First Difference'] = df[column] - df[column].shift(best_key)
                results=adfuller(df['Seasonal First Difference'].dropna()) 
                labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations']
                for value,label in zip(results,labels):
                    print(label+' : '+str(value))
                print("Best shift happened at : {}".format(best_key))
                print()
                df['Seasonal First Difference'].plot(x=df['Month_x'], y=df[column])
                print()
            else:
                print()
                print("Seasonality couldn't be removed with the given parameters...")
                print()
        else:
            print("There is no trend or seasonality found in this dataset...")
            print()
