#! /usr/bin/env python

# Load the datafile and perform SVD on the data
# output JSON file containing U, S, and V matrices

import numpy, pylab, scipy.cluster

import csv, operator, pprint

infilename = "out_commonwordcounts_table.txt"


def load_table( filename ):
	with open( filename ) as f:
		contents = numpy.array( [ r for r in csv.reader( f, delimiter='\t' ) ] )
	# Now extract row and column headings
	rh = list( contents[1:,0] )
	ch = list( contents[0,1:] )
	return rh, ch, contents[1:,1:].astype( numpy.int32 )


def scat_plot( v1, v2 ):
	pylab.scatter( v1 , v2 , marker = 'o' )
	# Labels added per http://stackoverflow.com/questions/5147112/matplotlib-how-to-put-individual-tags-for-a-scatter-plot	
	for label, x, y in zip( rh, v1 , v2 ):
		pylab.annotate( label, xy=(x,y) , xytext = (-20, 20),
                  textcoords = 'offset points', ha = 'right', va = 'bottom',
                  bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
                  arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))


def top_words( vec , words , numwords ):
	pprint.pprint( sorted(   zip(  words , vec ) , key = operator.itemgetter(1) , reverse=True )[0:numwords] )


if __name__ == "__main__":
	rh, ch, data = load_table( infilename )

	# full matrices= false is the compact SVD transformation, returning a limited number of basis vectors (8, not 438)
	centroids, labels = scipy.cluster.vq.kmeans2( data, 3, iter = 10 )



	# Now we need to turn the SVD results into something physically meaningful
	# The columns of U = weightings of 1 specific component across all samples (observations)
	# And each column of V (aka row of VT) represents the contribution of each word to one specific basis vector


	exit()
	# What are the top 10 words associated with Component 1?
	top_words( v[:,1] , ch , 10 )

	# Let's start with a scatter plot where each datapoint represents one observation, and we plot magnitude of C1 vs C2 for all observations
	# This is a scatterplot of U columns 1 vs 2
	pylab.subplot(	221 )
	scat_plot( u[:,1] , u[:,2] )

	# And again for second subplot
	pylab.subplot( 222 )
	scat_plot( u[:,1] , u[:,3] )
	
	pylab.subplot( 223 )
	scat_plot( u[:,1] , u[:,4] )

	pylab.subplot( 224 )
	pylab.plot( v[:,1] )
	#scat_plot( u[:,2] , u[:,4] )

	pylab.show()
