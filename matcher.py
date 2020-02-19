# Matcher
#   Program to match surevy takers 
#   by similar answers

# Import Libraries
import csv

class Responses:
        
    def __init__(self, answers: [], id_index: int, ignore_indexes: [int]):
        self.answers = answers
        self.id = answers[id_index]
        self.ignore_indexes = ignore_indexes
        self.matches_detailed = []
        self.matches = []
        self.best_match = None
        self.best_match_score = 0

    def compute_matches(self, others: []):
        for other in others:
            if not other == self:
                self.matches_detailed.append((other.id, self.compare(other)))
        self.matches_detailed = sorted(self.matches_detailed, key=lambda r: r[1], reverse=True)
        self.matches = [m[0] for m in self.matches_detailed]

    def compare(self, other):
        num_ans = len(self.answers)-len(self.ignore_indexes)
        num_same_ans = 0
        
        for i in range(len(self.answers)):
            if i not in self.ignore_indexes:
                if self.answers[i] == other.answers[i]:
                    num_same_ans += 1


        similarity = num_same_ans / num_ans
        return similarity

    def csv(self):
        return self.id + ','+ str(self.matches)[1:-1]

    def __eq__(self, other):
        if other == None:
            return False
        if type(other) == str:
            return self.id == other
        return self.id == other.id
        
    def __repr__(self):
        return self.id + ": " + str(self.answers) + '\nMatches: ' + str(self.matches_detailed)



def make_matches(people: [str], prefs: {str: [str]}):
    matches = []
    i=0

    while len(people) > 1:
        p = people[i]
        top_pick = prefs[p][0]
        top_pick_prefs = prefs[top_pick]

        if p == top_pick_prefs[0]:
            matches.append((p, top_pick))
            
            people.remove(p)
            people.remove(top_pick)
            del prefs[p]
            del prefs[top_pick]
            for key in prefs:
                prefs[key].remove(p)
                prefs[key].remove(top_pick)

        else:
            i += 1
    
        if i == len(people):
            i = 0

    return matches 

def match_email(x, y):
    print("----------------")
    print(x.answers[2])
    print(y.answers[2])
    print()
    print("-------------------------------------------------")
    print("Mesa Match!")
    print(x.id + " and " + y.id)
    print("-------------------------------------------------")
    print()
    print("These were your responses. . .")
    print()
    space = max(len(x.id), len(y.id))
    for i in range(len(x.answers)):
        if i == 3 or i not in x.ignore_indexes:
            if i == 20: continue
            print(questions[i])
            print(f'    {x.id:<{space}} - {x.answers[i]}')
            print(f'    {y.id:<{space}} - {y.answers[i]}')
            print()
    print("----------------")

# Main
if __name__ == '__main__':
    # Read CSV
    csv_responses = csv.reader(open("../responses2.csv"))

    # Create a list of people
    people = []
    for csv_response in csv_responses:
        response = Responses(csv_response, 1, [0, 1, 2, 3, 7, 19])
        people.append(response)
    
    questions = people[0].answers
    del people[0]

    # Calculate Matches
    for person in people:
        person.compute_matches(people)    
    
    # Generate pref dict
    # {response.id : response.matches}
    pref_dict = {}
    for person in people:
        pref_dict[person.id] = person.matches
    
    names = [p.id for p in people]
    matches = make_matches(names, pref_dict)
    for pair in matches:
        print(pair)    
    ''' 
    # Print Emails
    print()
    print("Printing emails. . .")
    print()
    for match in matches:
        match_email(people[people.index(match[0])], people[people.index(match[1])])
        print()
        input("Press enter to continue")
        print()
    '''

    # Print Results
    print()
    while True:
        name = input("Enter a name: ")
        try:
            i = people.index(name)
            print(people[i])
        except:
            print("Error: Person not found")
   
