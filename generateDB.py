import wikipedia
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
client.drop_database("Wiki-Graph")
db = client["Wiki-Graph"]

main_page = "Computer Science"

links_1nd_degree = wikipedia.WikipediaPage(main_page).links
for link in links_1nd_degree:
    try:
        links_2nd_degree = wikipedia.WikipediaPage(link).links
        link = link.replace(" ", "_")
        for links_2 in links_2nd_degree:
            links_2 = links_2.replace(" ", "_")
            db[link].insert_one({'name':links_2})
        print link + " collect"
    except:
        print "Error in " + link
