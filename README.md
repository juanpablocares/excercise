# excercise

=========================================================
========================Execution========================
=========================================================
To execute the algorithm it has to execute the next line

"make run $(sigma_value)"

$(sigma_value) = minimal support level

=========================================================
=====================Output Format=======================
=========================================================
I followed the given output format
<item set size (N)>, <co-occurrence frequency>, <item 1 id >, <item 2 id>, …. <item N id>
The name of the output is the same as the input file but using an extension ".out"

Additionaly I added an output file of my execution using the given example.
It can be run using this line
"make run test"
And the result can be found on the file "retail_25k.out"

=========================================================
=========================Tests===========================
=========================================================
I added some smaller data set to do my first approaches:
- min.dat
- retail.dat
This version as well include the given data set:
- retail_25k.dat

=========================================================
==================Summary Algorithm======================
=========================================================
The flow of the algorithm follow the next steps

 read data transforming each transaction into a list of sets
 combinations_counter = {}
 iterate the first to the last transaction
   combinations_transaction = {}
   iterate from the previous transaction + 1 to the last one
    find the intersection between both transactions
    if len(intersection) >= 3
      generate all combinations of the intersection
      if some combination is not already added into combinations_transaction
        add into combinations_transaction
    append combinations_transaction into combinations_counter
 create file using combinations_counter

=========================================================
================Combination Algorithm====================
=========================================================
I have two versions to get all the combinations of a given intersetion
The first one use itertools.combinations and the second one is mine version.
To activate one or the other you can see more detail in supermarket.py file
in line 73.
By default it is activated "itertools.combinations" my version takes more time
for that reason I prefered this way

=========================================================
========================Statement========================
=========================================================

Supermarket Optimization
 
You’ve been hired as a market consultant to try and help a local supermarket come up with better placement of items based on buyer’s preferences, and towards that goal you’d like to identify certain association rules based on existing records of buyer’s transactions.
 
You are given as input:
•   A transaction database - a file consisting of a single row per transaction, with individual product's SKUs given as space–separated integers. A single transaction consisting of products with SKUs 1001, 1002 and 1003 would have a line that looks like: ‘1001 1002 1003' 
•   A minimal ’support level’ parameter, sigma – a positive integer 
Implement, in Python or Java, an efficient algorithm for generating all frequent item sets of size 3 or more: groups of 3 or more items that appear together in the transactions log at least as often as the support level parameter value. For example, given a value of sigma = 2, all sets of 3 items that appear 2 or more times together in the transaction log should be returned.
 
The results should be returned as a file with the following format:
 
<item set size (N)>, <co-occurrence frequency>, <item 1 id >, <item 2 id>, …. <item N id>
