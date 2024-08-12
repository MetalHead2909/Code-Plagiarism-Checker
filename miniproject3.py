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
import io
import tokenize
warnings.filterwarnings("ignore")
import time

#sample_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
#documents = [open(File).read() for File in sample_files]
def codingplagiarismcheck(check):
    path = os.getcwd()
    sample_files = [doc for doc in os.listdir(path+"/uploads") if doc.endswith('.java') or doc.endswith('.txt') or doc.endswith('.c') or doc.endswith('.py')]
    documents = [open(path+"/uploads/"+File).read() for File in sample_files]
    for i in range(len(documents)):
        print(f"Document {i+1} : {sample_files[i]}")
    #Java Preprocessing
    def preprocessing_java(prog):
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
    #Python Preprocessing
    def preprocessing_python(source):
        """
        Returns 'source' minus comments and docstrings.
        """
        io_obj = io.StringIO(source)
        out = ""
        prev_toktype = tokenize.INDENT
        last_lineno = -1
        last_col = 0
        for tok in tokenize.generate_tokens(io_obj.readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            ltext = tok[4]
            # The following two conditionals preserve indentation.
            # This is necessary because we're not using tokenize.untokenize()
            # (because it spits out code with copious amounts of oddly-placed
            # whitespace).
            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += (" " * (start_col - last_col))
            # Remove comments:
            if token_type == tokenize.COMMENT:
                pass
            # This series of conditionals removes docstrings:
            elif token_type == tokenize.STRING:
                if prev_toktype != tokenize.INDENT:
            # This is likely a docstring; double-check we're not inside an operator:
                    if prev_toktype != tokenize.NEWLINE:
                        # Note regarding NEWLINE vs NL: The tokenize module
                        # differentiates between newlines that start a new statement
                        # and newlines inside of operators such as parens, brackes,
                        # and curly braces.  Newlines inside of operators are
                        # NEWLINE and newlines that start new code are NL.
                        # Catch whole-module docstrings:
                        if start_col > 0:
                            # Unlabelled indentation means we're inside an operator
                            out += token_string
                        # Note regarding the INDENT token: The tokenize module does
                        # not label indentation inside of an operator (parens,
                        # brackets, and curly braces) as actual indentation.
                        # For example:
                        # def foo():
                        #     "The spaces before this docstring are tokenize.INDENT"
                        #     test = [
                        #         "The spaces before this string do not get a token"
                        #     ]
            else:
                out += token_string
            prev_toktype = token_type
            last_col = end_col
            last_lineno = end_line

        
        return out
    def preprocessing_python2(prog):
        flag1 = 0  # to check if a data type is encountered 
        loc = 0 # to store the index of first occurence of single line comment
        flag2 = 0   # once flag1 = 1, it keeps checking if a variable is encountered

        data_types = ['int', 'long', 'double',
                    'boolean', 'char', 'string', 'void', 'float']     # to store the data types which will help checking for integers and functions

        special_names = []   # to store variable, function and class names
        
        prog = prog.lower()

        comment = pyparsing.nestedExpr("/*","*/").suppress() # using a parser to remove multi-line comments quickly
        prog = comment.transformString(prog)

        prog = preprocessing_python(prog)

        prog = prog.strip()     # remove trailing and leading white spaces

        lst_string = [prog][0].split('\n')       # breaking the prog into list of individual lines
        normalised_code = []        # will eventually store the final normalised code
        no_comments_code = []

        no_comments_string = ""                 # to remove comments
        for line in lst_string:
            line = line.split()
            for i in line:
                loc = i.find('//')
                if loc >= 0:
                    no_comments_string += i[0:loc] + ' '
                    break
                no_comments_string += i + ' '
            if no_comments_string != '':
                no_comments_code.append(no_comments_string)
            no_comments_string = ""

        lst_string = no_comments_code
        no_comments_code = []

        for line in lst_string:
            line = line.split()
            for i in line:
                loc = i.find('#')
                if loc >= 0:
                    no_comments_string += i[0:loc] + ' '
                    break
                no_comments_string += i + ' '
            if no_comments_string != '':
                no_comments_code.append(no_comments_string)
            no_comments_string = ""

        for i in range(0, len(no_comments_code)):        
            line = [word for word in re.split("\W+",no_comments_code[i])]
            no_comments_code[i] = ' '.join(line)


        temp_string = ""                 # parsing the string to detect function and variable names
        for line in no_comments_code:
            line = line.split()
            for i in line:

                if flag1 == 1:
                    if re.search("^[a-zA-Z_$]", i) is not None and i not in data_types:
                        flag2 = 1
                    else:
                        flag2 = 0

                if flag2 == 1:      # this if statement handles variable detection
                    special_names.append(i)
                    #print(i)
                    flag2 = 0
                
                if i in data_types or i == "class":
                    flag1 = 1      

                temp_string += i + ' '

            flag1 = 0
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
    #C Preprocessing

    start_time = time.time()

    def preprocessing_c(prog):
        flag1 = 0  # to check if a data type is encountered 
        loc = 0 # to store the index of first occurence of single line comment
        flag2 = 0   # once flag1 = 1, it keeps checking if a variable is encountered

        data_types = ['int', 'long', 'double',
                    'boolean', 'char', 'string', 'void', 'float']     # to store the data types which will help checking for integers and functions

        special_names = []   # to store variable, function and class names
        
        prog = prog.lower()

        comment = pyparsing.nestedExpr("/*","*/").suppress() # using a parser to remove multi-line comments quickly
        prog = comment.transformString(prog)

        #prog = remove_comments_and_docstrings(prog)

        prog = prog.strip()     # remove trailing and leading white spaces

        lst_string = [prog][0].split('\n')       # breaking the prog into list of individual lines
        normalised_code = []        # will eventually store the final normalised code
        no_comments_code = []

        no_comments_string = ""                 # to remove comments
        for line in lst_string:
            line = line.split()
            for i in line:
                loc = i.find('//')
                if loc >= 0:
                    no_comments_string += i[0:loc] + ' '
                    break
                no_comments_string += i + ' '
            if no_comments_string != '':
                no_comments_code.append(no_comments_string)
            no_comments_string = ""

        lst_string = no_comments_code
        no_comments_code = []

        for line in lst_string:
            line = line.split()
            for i in line:
                loc = i.find('#')
                if loc >= 0:
                    no_comments_string += i[0:loc] + ' '
                    break
                no_comments_string += i + ' '
            if no_comments_string != '':
                no_comments_code.append(no_comments_string)
            no_comments_string = ""

        for i in range(0, len(no_comments_code)):        
            line = [word for word in re.split("\W+",no_comments_code[i])]
            no_comments_code[i] = ' '.join(line)


        temp_string = ""                 # parsing the string to detect function and variable names
        for line in no_comments_code:
            line = line.split()
            for i in line:

                if flag1 == 1:
                    if re.search("^[a-zA-Z_$]", i) is not None and i not in data_types:
                        flag2 = 1
                    else:
                        flag2 = 0

                if flag2 == 1:      # this if statement handles variable detection
                    special_names.append(i)
                    #print(i)
                    flag2 = 0
                
                if i in data_types or i == "class":
                    flag1 = 1      

                temp_string += i + ' '

            flag1 = 0
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
    if check == 1:
        for i in range(len(documents)):
            documents[i] = preprocessing_java(documents[i])
    else:
        if check == 2:
            for i in range(len(documents)):
                documents[i] = preprocessing_python2(documents[i])
        else:
            if check == 3:
                for i in range(len(documents)):
                    documents[i] = preprocessing_c(documents[i])

    #print(documents)

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
    plagiarism_threshold = 0.9
    plagiarism_indices = np.where(similarity_matrix >= plagiarism_threshold) #threshold to cut the kmeans cluster
    #print(plagiarism_indices)
    plagiarism_indices = [(i, j) for i, j in zip(plagiarism_indices[0], plagiarism_indices[1])]
    print('plagiarism_indices')
    #print(plagiarism_indices)

    #using plagiarism threshold
    for i in range(len(documents)):
        for j in range(len(documents)):
            t = (i,j)
            if t not in plagiarism_indices:
                similarity_matrix[i][j] = 0.02
    # print(similarity_matrix)

    # K-means clustering with silhouette score for determining number of clusters
    max_clusters = len(documents)
    best_silhouette_score = -1
    best_num_clusters = len(documents) #change made
    for num_clusters in range(2, max_clusters):#max_clusters added max_clusters+1
        kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(similarity_matrix)
        cluster_labels = kmeans.labels_
        silhouette_avg = silhouette_score(similarity_matrix, cluster_labels)
        # print("=================================================================")
        # print("Cluster Labels: ",cluster_labels,"\tSilhoutte Score: ",silhouette_avg,"\tClusters : ",num_clusters)
        # print("=================================================================")
        if silhouette_avg > best_silhouette_score:
            best_silhouette_score = silhouette_avg
            best_num_clusters = num_clusters
    
    print("\nBest Silhouette Score: ",best_silhouette_score,"\tBest Num Clusters: ",best_num_clusters)

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
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution Time for Finding Code Plagirarim: ",execution_time)
    result = []
    docresult = []
    for i in subgroups:
       result.append(subgroups[i])
    for i in result:
        tempdocresult = []
        for j in i:
            tempdocresult.append(sample_files[j-1])
        docresult.append(tempdocresult)
    #path = os.getcwd() + "/uploads"
    for i in range(len(sample_files)):
        path = os.getcwd() + "/uploads/" + str(sample_files[i])
        if os.path.exists(path):
            os.remove(path)
    #     import os
    # if os.path.exists("demofile.txt"):
    #   os.remove("demofile.txt")
    # else:
    #   print("The file does not exist")
    #print(result)
    #print(sample_files)
    #print(docresult)
    return docresult
