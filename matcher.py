# Matcher
#   Program to match surevy takers by similar answers

# Import Libraries
import csv, sys

# Responses
#   This is a class representes all of the responses
#
#   Attributes
#       answers: CSV List                   - list of the person's responses
#       id: str                             - id to represent the person (such as name)
#       ignore_indexes: [int]               - indexes to ignore when comparing responses (name, email, etc.)
#       matches_detailed: [(str, double)]   - (name, score) ranked in order of prefence 
#       matches: [str]                      - Names of people in order of preference
#
#   * matches and matches_detailed are empty lists until `compute_scores` is called
class Responses:
        
    def __init__(self, answers: [], id_index: int, ignore_indexes: [int]):
        self.answers = answers
        self.id = answers[id_index]
        self.ignore_indexes = ignore_indexes
        self.matches_detailed = []
        self.matches = []

    # Compute Scores
    #   Given a list of other Responses, calculate the scores with each response.
    #   The scores are then reordered from highest score to lowest score.
    #
    #   Params
    #       others: [Response]
    #
    #   Returns
    #       Void, but matches and matches_detailed will be updated
    def compute_scores(self, others: []):
        for other in others:
            if not other == self:
                self.matches_detailed.append((other.id, self.compare(other)))
        self.matches_detailed = sorted(self.matches_detailed, key=lambda r: r[1], reverse=True)
        self.matches = [m[0] for m in self.matches_detailed]

    # Compare
    #   Compute the score between this and the other
    #   Score is number of same answers divided by the number of total answers
    #
    #   Params
    #       other: Response
    #
    #   Returns
    #       Double  - the score of the pair
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


# Make Matches
#   This is the algorithm that matches each person in the list to their highest available preference
#
#   Params
#       prefs: {str: [str]}  
#           - Preference of people to be matched
#           - Each key in the dict is a person to be matched.
#           - Each value in the dict is an ordered list of people, ranked from first to last preference
#
#   Returns
#       List of 2-tuples 
def make_matches(prefs: {str: [str]}):
    # Empty list to hold matches
    matches = []
    
    # Get all of the people in the dict
    people = list(prefs.keys())

    # Index in the list
    i=0

    # As long as there is more than one person in the list,
    # continue running the algorithm
    while len(people) > 1:
        p = people[i]                               # Pull a person from the list at the current index
        top_pick = prefs[p][0]                      # Get that person's top prefenced
        top_pick_of_top_pick = prefs[top_pick][0]   # Get the top pick of the top pick

        # If the top pick also wants the person, match them
        if p == top_pick_of_top_pick:
            # Add the match to matches
            matches.append((p, top_pick)) 
            
            # Remove both from the pool of people 
            people.remove(p)        # Remove p from the list
            people.remove(top_pick) # Remove top pick from the list
            del prefs[p]            # Delete p from the dict
            del prefs[top_pick]     # Delete top pick from the dict
            
            # Remove both from ever other person's preference list
            for key in prefs:
                prefs[key].remove(p)
                prefs[key].remove(top_pick)
        else:
            # If the top pick doesn't have the person as first choice,
            # Do nothing and move onto the next person
            i += 1
    
        # If the end of the list is reached, 
        # loop back around to the beginning
        if i == len(people):
            i = 0

    # Return all of the matches
    return matches 


# Match Email
#   This function was to output the matches in a format that could be emailed out to the people
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
    # Get CSV file name
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        file_name = input("Input csv file name: ")

    # Read CSV     
    csv_responses = csv.reader(open("../responses2.csv"))

    # Create a list of people
    people = []
    for csv_response in csv_responses:
        response = Responses(csv_response, 1, [0, 1, 2, 3, 7, 19])
        people.append(response)
    
    # Pull the questions out of the responses and delete them
    questions = people[0].answers
    del people[0]

    # Calculate Matches
    for person in people:
        person.compute_scores(people)    
    
    # Generate pref dict
    # {response.id : response.matches}
    pref_dict = {}
    for person in people:
        pref_dict[person.id] = person.matches
    
    # Pair the people based off their prefences
    matches = make_matches(pref_dict)
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
   
