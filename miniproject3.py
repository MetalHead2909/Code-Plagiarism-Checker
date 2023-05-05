import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
import os
import pyparsing 
import re
import warnings
warnings.filterwarnings("ignore")

#sample_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
#documents = [open(File).read() for File in sample_files]
def codingplagiarismcheck():
    sample_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
    documents = [open(File).read() for File in sample_files]
    for i in range(len(documents)):
        print(f"Document {i+1} : {sample_files[i]}")

    def preprocessing(prog):
        flag1 = 0  # set it to 1 when we encounter comment start
        flag2 = 0  # for variables 

        data_types = ['int', 'long', 'double',
                    'boolean', 'char', 'string', 'void', 'float']     # to store the data types which will help checking for integers and functions

        special_names = []   # to store variable, function and class names
        
        prog = prog.lower()

        comment = pyparsing.nestedExpr("/*","*/").suppress() # using a parser to remove multi-line comments quickly
        prog = comment.transformString(prog)

        prog = prog.strip()     # remove trailing and leading white spaces

        lst_string = [prog][0].split('\n')       # breaking the prog into list of individual lines
        normalised_code = []        # will eventually store the final normalised code
        no_comments_code = []

        no_comments_string = ""                 # to remove comments
        for line in lst_string:
            line = line.split()
            for i in line:
                if i == '//':
                    flag1 = 1
                if flag1 == 0:
                    no_comments_string += i + ' '
            if no_comments_string != '':
                no_comments_code.append(no_comments_string)
            no_comments_string = ""
            flag1 = 0

        for i in range(0, len(no_comments_code)):        
            line = [word for word in re.split("\W+",no_comments_code[i])]
            no_comments_code[i] = ' '.join(line)

        temp_string = ""                 # parsing the string to detect function and variable names
        for line in no_comments_code:
            line = line.split()
            for i in line:

                if flag2 == 1:      # this if statement handles variable detection
                    special_names.append(i)
                    flag2 = 0
                
                if i in data_types or i == "class":
                    flag2 = 1      

                temp_string += i + ' '

            flag2 = 0
            normalised_code.append(temp_string)
            temp_string = ""


        for i in range(0, len(normalised_code)):        
            line = [word for word in re.split("\W+",normalised_code[i]) if word.lower() not in special_names]
            normalised_code[i] = ' '.join(line)
                    
        str1 = ''            
        for i in normalised_code:
            if i != '':
                str1 = str1 + i + '\n'

        str1 = str1[:-1]
        return str1
        
    for i in range(len(documents)):
        documents[i] = preprocessing(documents[i])

    print(documents)

    # List of documents
    # documents = [
    #     "This is document 1.",
    #     "Thisdocument2.",
    #     "3.",
    #     "This is document4.",
    #     "5.",
    #     # Add more documents here
    # ]

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    #print(similarity_matrix)
    #print(similarity_matrix.shape)

    # Checking for plagiarism
    plagiarism_threshold = 0.8
    plagiarism_indices = np.where(similarity_matrix > plagiarism_threshold) #threshold to cut the kmeans cluster
    #print(plagiarism_indices)
    plagiarism_indices = [(i, j) for i, j in zip(plagiarism_indices[0], plagiarism_indices[1])]

    #print(plagiarism_indices)

    # K-means clustering with silhouette score for determining number of clusters
    max_clusters = len(documents)
    best_silhouette_score = -1
    best_num_clusters = len(documents) #change made
    for num_clusters in range(2, max_clusters):
        kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(similarity_matrix)
        cluster_labels = kmeans.labels_
        silhouette_avg = silhouette_score(similarity_matrix, cluster_labels)
        if silhouette_avg > best_silhouette_score:
            best_silhouette_score = silhouette_avg
            best_num_clusters = num_clusters

    # Apply K-means clustering with the determined number of clusters
    kmeans = KMeans(n_clusters=best_num_clusters, random_state=0).fit(similarity_matrix)
    cluster_labels = kmeans.labels_

    # Agglomerative Hierarchical Clustering
    # clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.3)
    # clustering.fit(similarity_matrix)
    #linkage_matrix = dendrogram(clustering, no_plot=True)
    #print([i+1 for i in cluster_labels])

    # Find subgroups
    subgroups = {}
    for idx, label in enumerate(cluster_labels):
        if label not in subgroups:
            subgroups[label] = []
        subgroups[label].append(idx+1)

    # Print subgroups
    #print("Subgroups:")
    #for group, docs in subgroups.items():
    #    print("Group {}: {}".format(group+1, docs))
    #sample_files = ['DividenConquer.txt','BranchnBound2.txt','dijkstra2.txt','DividenConquer2.txt','dijkstra.txt','BranchnBound.txt']
    #results = [ [ 1, 4 ], [ 2, 6 ], [ 3, 5 ] ]
    #results = [ [ 'DividenConquer.txt', 'DividenConquer2.txt' ], [ 'BranchnBound2.txt', 'BranchnBound.txt' ], [ 'dijkstra2.txt', 'dijkstra.txt' ] ]
    result = []
    docresult = []
    for i in subgroups:
       result.append(subgroups[i])
    for i in result:
        tempdocresult = []
        for j in i:
            tempdocresult.append(sample_files[j-1])
        docresult.append(tempdocresult)
    print(result)
    print(sample_files)
    print(docresult)
    return docresult
