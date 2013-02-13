#! /usr/bin/env python

# Perform dimensionality reduction and write a file containing features (columns) and observations (rows) for common
#     words that appear across file dataset.
# Takes the previously generated JSON file of raw wordcounts for all files as input.


import json, collections, csv
from nltk.corpus import stopwords

infilename = "out_json_wordcounts.txt"
outfilename = "out_commonwordcounts_table_fraclength.txt"

# Provide an option to write out the count as fraction of total document, rather than raw number of counts. Possibly useful for resumes of very different length
fraction_counts = True


with open( infilename ) as f:
	data = json.loads( f.read() )

# Clear out all the words that appear in only 1 file, or that appear in all (limited predictive power?). Then, dither further based on nltk/stopwords corpus.

# Remove all words that appear in only one file. In amogh's dataset, this cuts the wordlist from 1877-> 471 
# Then also apply filter: strip out stopwords, which cuts the dataset from 471 --> 438
data["words"] = { k: data["words"][k] for k in data["words"] if data["words"][k] > 1 and k not in stopwords.words('english') }


# Now that we have a list of all words of interest across all files (minus the words that only appear once or twice ever)...
# We will want to write out a CSV file containing features (columns) and observations (rows).

with open( outfilename , "w" ) as f:
	csvwriter = csv.writer( f, delimiter = '\t' )

	csvwriter.writerow( [ "File name" ] + data["words"].keys() )
	
	for filename in data["files"]:	
		if not fraction_counts:
			csvwriter.writerow(
		  	   [filename] + [ data["files"][filename]["wordcounts"].get(w,0)  for w in data["words"] ]  )
		else:
			csvwriter.writerow(
			   [filename] + [ data["files"][filename]["wordcounts"].get(w,0) / float( data["files"][filename]["numwords"] )
			    for w in data["words"] ]  )

