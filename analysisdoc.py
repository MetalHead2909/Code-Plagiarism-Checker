import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def analysis(file1,file2):

    def read_file(file_path):
        with open(file_path, 'r') as file:
            return file.readlines()

    def create_windows(lines, window_size):
        windows = []
        for i in range(len(lines) - window_size + 1):
            window = ' '.join(lines[i:i + window_size])
            windows.append((i, window))
        return windows

    def find_similar_windows(file1_windows, file2_windows, threshold):
        similar_windows = []
        vectorizer = TfidfVectorizer().fit_transform([window for _, window in file1_windows + file2_windows])
        vectors = vectorizer.toarray()
        
        for i, (_, window1) in enumerate(file1_windows):
            for j, (_, window2) in enumerate(file2_windows):
                vec1 = vectors[i]
                vec2 = vectors[len(file1_windows) + j]
                similarity = cosine_similarity([vec1], [vec2])[0][0]
                if similarity >= threshold:
                    similar_windows.append((file1_windows[i][0], file2_windows[j][0], similarity))
        
        return similar_windows
    
    def generate_html(file1_lines, file2_lines, similar_windows, window_size):
        file1_html = []
        file2_html = []
        
        file1_set = set()
        file2_set = set()

        file_similarities = list()
        for win in similar_windows:
            for i in range(win[0], win[0] + window_size):
                file1_set.add(i)
            for j in range(win[1], win[1] + window_size):
                file2_set.add(j)
            file_similarities.append(round(float(win[2])*100,2))
        
        for i, line in enumerate(file1_lines):
            if i in file1_set:
                file1_html.append(f'<span style="background-color: red;display: inline-block;width: 100%;">{line}</span>')
            else:
                file1_html.append(line)
        
        for i, line in enumerate(file2_lines):
            if i in file2_set:
                file2_html.append(f'<span style="background-color: red;display: inline-block;width: 100%;">{line}</span>')
            else:
                file2_html.append(line)
        
        return ''.join(file1_html), ''.join(file2_html), file_similarities

    def main(file1_path, file2_path, window_size=5, threshold=0.56):
        file1_lines = read_file(file1_path)
        file2_lines = read_file(file2_path)
        
        file1_windows = create_windows(file1_lines, window_size)
        file2_windows = create_windows(file2_lines, window_size)
        
        similar_windows = find_similar_windows(file1_windows, file2_windows, threshold)

        file1_html, file2_html,file_similarities = generate_html(file1_lines, file2_lines, similar_windows, window_size)
        
        #print("Similar Windows:")
        #for win in similar_windows:
            #print(f"File1 Lines {win[0]}-{win[0]+window_size-1} and File2 Lines {win[1]}-{win[1]+window_size-1} with similarity {win[2]*100:.2f}%")
            #print("File1 Window:")
            #print(''.join(file1_lines[win[0]:win[0] + window_size]))
            #print("File2 Window:")
            #print(''.join(file2_lines[win[1]:win[1] + window_size]))
            #print()
        
        # print("FILE 1")
        # print(file1_html)
        # print("================================")
        # print("FILE 2")
        # print(file2_html)
        # print("================================")
        # print(file_similarities)
        return [file1_html,file2_html,file_similarities]

    file1_path = './testuploads/'+file1
    file2_path = './testuploads/'+file2
    return main(file1_path, file2_path)
