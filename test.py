'''
#This keeps track of the names dicts you have created, and then gives them to you at the end. 
def make_dict(list_of_names):
    results = []
    for names in list_of_names:
        names = {
            "name": names,
            "homework" : [],
            "quizzes" : [],
            "tests" : []
        }
        results.append(names)
    return results

list_of_names = ["lloyd", 'alice', 'tyler']

my_dicts = make_dict(list_of_names)

##
def make_dict(lst):
    for name in lst:
        d = {k: [] for k in ('homework', 'quizzes', 'tests')}
        d['name'] = name
        yield d

list_of_names = ['lloyd', 'alice', 'tyler']

my_dicts = list(make_dict(list_of_names))

'''
