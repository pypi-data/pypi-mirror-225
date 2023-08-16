from main import *

intentfp, thesaurusfp, UIName = "intents.json", "thesaurus.json", "Ultron"

JanexPT = JanexPT(intentfp, thesaurusfp, UIName)

#JanexPT.trainpt()
inputstr = input("You: ")
IC = JanexPT.pattern_compare(inputstr, "Jack")
Response = JanexPT.response_compare(inputstr, IC)
NewResponse = JanexPT.generate_response_with_synonyms(Response, 10)

print(Response)
print(NewResponse)
