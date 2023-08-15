from dotenv import load_dotenv
load_dotenv()

from novexity import search

# Call the search function
formatted_json_string, returned_gateway = search(
    "USA Minecraft")

# Print the formatted JSON string
print(formatted_json_string)

# Save the results to search.json
with open("results1.json", "w", encoding="utf-8") as file:
    file.write(formatted_json_string)

# Shut down the gateways
returned_gateway.shutdown()
