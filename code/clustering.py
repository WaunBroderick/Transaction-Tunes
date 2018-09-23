import pandas as pd 
import numpy as np 
from sklearn.cluster import KMeans 
from sklearn import cross_validation
from sklearn.cross_validation import KFold
from sklearn.cluster import DBSCAN
from pygame import mixer

#company: inputs song database -> songs matched to clusters based on previous clusts that we have -> 
#model 1: map song to predefined clust
#


mixer.init()
mixer.music.load('e:/LOCAL/Betrayer/Metalik Klinik1-Anak Sekolah.mp3')
mixer.music.play()


songs = pd.read_csv("spotify_songclass_data.csv", index_col = 14)
songs = songs.drop(columns=["target", "artist"])

# how many clusters do we want? try 

#categorical columns: mode, artist 
#try dbscan 
#don't really have categorical data (ignore artist names for now)
def dbscan(data):
    db = DBSCAN(eps=0.7).fit(data)
    labels = db.labels_
    print("Labels", len(labels))
    mapping = pd.DataFrame(columns = ["Song Name", "Clust"])
    mapping["Song Name"] = list(data.index)
    mapping["Clust"] = db.labels_
    return(mapping)

def kmeans(data, n_clusts):
    km = KMeans(init='k-means++', n_clusters=n_clusts).fit(data)
    print("test")
    labels = km.labels_
    mapping = pd.DataFrame(columns = ["Song Name", "Clust"])
    mapping["Song Name"] = list(data.index)
    mapping["Clust"] = km.labels_
    return(mapping)


#mapping = kmeans(songs, 8)
#mapping.to_csv("clust_map_km.csv")

#clusts + demographics => predict song types highly correlated to 
#association analysis - which 
#find significant variables 
#