
# coding: utf-8

# In[84]:


'''
1. The total number of votes cast
2. A complete list of candidates who received votes
3. The percentage of votes each candidate won
4. The total number of votes each candidate won
5. The winner of the election based on popular vote.

As an example, your analysis should look similar to the one below:
Election Results
-------------------------
Total Votes: 620100
-------------------------
Rogers: 36.0% (223236)
Gomez: 54.0% (334854)
Brentwood: 4.0% (24804)
Higgins: 6.0% (37206)
-------------------------
Winner: Gomez
-------------------------
Your final script must be able to handle any such similarly-structured dataset in the future 
(i.e you have zero intentions of living in this hillbilly town -- so your script needs to work without massive re-writes). 
In addition, your final script should both print the analysis to the terminal and export a text file with the results.
'''

import pandas as pd
import os
import csv


# In[85]:


os.chdir("/Users/rorr/PythonStuff/")
csvpath = os.path.join("Resources", "election_data_2.csv")

election = pd.read_csv(csvpath, encoding="utf-8")

# In[86]:

print("---------------------------------")
print("Election Results")
vote_count = len(election["Voter ID"])
print("---------------------------------")
print("Total Votes:" + str(vote_count))

# In[87]:
unique_candidates = election["Candidate"].unique()

# In[111]:

print("---------------------------------")
unique_candidates = election["Candidate"].unique()
Candidate_votes = election["Candidate"].value_counts()
Outcome = (Candidate_votes / vote_count) * 100 
Outcome = pd.DataFrame(Outcome)
Outcome.index.name = "Name"

# In[117]:
results = Outcome['Candidate'].astype(str) + '%   ' + "(" + (Candidate_votes).astype(str) + ")"
print(results.to_string(header=None))
print("---------------------------------")

# In[130]:

winner = (Candidate_votes).idxmax()
print("Winner: " + str(winner))

text = open("election_results.txt", "w")
text.write("-------------------------")
text.write('\n')
text.write("Election Results")
text.write('\n')
text.write("-------------------------")
text.write('\n')
text.write("Total Votes:" + str(vote_count))
text.write('\n')
text.write("-------------------------")
text.write('\n')
text.write(results.to_string(header=None))
text.write('\n')
text.write("-------------------------")
text.write('\n')
text.write("Winner: " + str(winner))
text.write('\n')
text.write("-------------------------")
text.close()

