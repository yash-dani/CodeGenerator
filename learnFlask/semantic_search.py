import requests, json

class Search():
    def __init__(self):
        self.code = []
    
    # Used for debugging purposes
    def print_entries(self):
        for i in range(0, 5):
            print(f"************* Entry {i} *********************")
            for j in range(0, len(self.code[i])):
                print(self.code[i][j])

    def get_language_codes(self, language):
        if language == 'python':
            return 19
        elif language == 'cpp':
            return 16
        elif language == 'go':
            return 55
        elif language == 'java':
            return 23
        elif language == 'swift':
            return 137
        elif language == 'javascript':
            return 22
        elif language == 'html':
            return 3
        elif language == 'c':
            return 28
    
    def rank(self, queries, original_query):
        for i in range(0, 5):
            self.code.append([])

            code_string = ""
            actual_code = queries['results'][i]['lines']
            for key, value in actual_code.items():
                code_string += value
            self.code[i].append(code_string)

        client_query = original_query.split()

        for code_lines in self.code:
            for search_word in client_query:
                code_lines.append(code_lines[0].count(search_word))

            code_lines.append(code_lines[0].count(" "))

        self.score() # Goes through the code lines and score them 
        best_code = self.get_best_code()
        
        return best_code
    
    def score(self):
        score = 0
        all_scores = []
        for i in self.code:
            for j in range(1, len(i) - 1):
                score += i[j] # Adding to score for number of occurences of the search word in the returned query
            score -= 0.5 * i[len(i) - 1] # Subtracting number of spaces from the score

            # Appending score and resetting to 0
            i.append(score)
            all_scores.append(score)
            score = 0
        
        # Normalizing scores
        max_score = max(all_scores)
        min_score = min(all_scores)

        for query in self.code:
            query[len(query) - 1] = (query[len(query) -1] - min_score)/(max_score - min_score)
    
    def get_best_code(self):
        max = -1
        best_code = ""

        for query in self.code:
            if max < query[len(query) - 1]:
                best_code = query[0]
        
        return best_code


    def search(self, language, search_query):
        language_code = self.get_language_codes(language)
        url = f"https://searchcode.com/api/codesearch_I/?q={search_query}&p=1&per_page=5&lan={language_code}"
        headers = {'Accept': 'application/json'}
        result = requests.get(url, headers = headers).json()
        
        top_result = self.rank(result, search_query)

        return top_result # Returns code of first search result