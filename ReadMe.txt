Author: Sydney Yeargers

Where to find answers:
	a) See DataFrame 'movie_matrix' (code for solution on lines 18-19).
	b) See DataFrame 'corr_matrix' (code for solution on line 21).
	c) See dictionary 'N' (code for solution on lines 31-38).
	d) See DataFrame 'estimates_matrix' (code for solution on line 51-59).
	e) See file 'output.txt' (code for solution on lines 63-81).

Libraries used: 
	• Pandas
	• Time

Estimations for (d) were calculated by multiplying the rating of the most similar movie by the correlation between the most similar movie and the movie who's rating is being estimated. 
	For example, estimate user1's rating for movie M:
	M = movie without rating by user1 (to be estimated); 
	SM = movie with the highest correlation to M that is also rated by user1;
	SM.r = rating user1 gave SM;
	corr(M, SM) = correlation between M and SM;
		user1_rating = (SM.r)*(corr(M, SM))


Friendly reminder, the professor said the following regarding runtime: "The grade penalty for having a slow program is not high unless your program is terribly slow (several hours to finish) due to improper program implementation. Any runtime within a few minutes to an hour should be fine." (I got marked down for a 7 second runtime on PA1, and I want to make sure that doesn't happen again. This program takes a while to run, but that is only because I am implementing the program for all 671 users, as opposed to one at a time like a recommendation algorithm typically does. I included the runtimes for the calculations of each individual user's estimated ratings and recommended movies as a benchmark for this program's runtime in a realistic setting.)

