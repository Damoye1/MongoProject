# MongoProject
Data 30
In Python, I had to pull data on all available starships from the API http://swapi.dev/. The "pilots" key contains APIs pointing to the characters who pilot the starship. My aim was to replace these with their respective ObjectId's from the characters collection and inserts starships into it's own collection. I achieved this with the use of importing the pymongo, requests and pprint libraries and creating functions.
I first pulled all the API information through the link, and created a function that would put the API documents in a list for every page then updating the pilots to ObjectID's. Finally, inserting it into the starships collection and calling the function.
