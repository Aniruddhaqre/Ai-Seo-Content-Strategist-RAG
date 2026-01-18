from query import query_ayurveda_db

result = query_ayurveda_db("Acne prone" , n_results=20)

print(result)


import json

# Assuming result is a list or dictionary
with open("triphala_results.txt", "w", encoding="utf-8") as f:
    # Use indent=4 to make the text file human-readable
    f.write(json.dumps(result, indent=4))

print("Results successfully saved to triphala_results.txt")