# excercise

##Execution

To execute the algorithm it has to execute the next line

```
make run $(sigma_value)
```

$(sigma_value) = minimal support level


##Output Format

I followed the given output format
```
<item set size (N)>, <co-occurrence frequency>, <item 1 id >, <item 2 id>, …. <item N id>
```
The name of the output is the same as the input file but using an extension ".out"

Additionaly I added an output file of my execution using the given example.
It can be run using this line
```
make run test
```
And the result can be found on the file "retail_25k.out"


##Tests

I added some smaller data set to do my first approaches:
- min.dat
- retail.dat
This version as well include the given data set:
- retail_25k.dat


##Summary Algorithm

The flow of the algorithm follow the next steps
```
 read data transforming each transaction into a list of sets
 iterate trough each sku
   tree_of_combinations = {}
   iterate from each transaction + 1 to the last one
     iterate from before transaction + 1 to the last one
       find the intersection between both transactions
       if len(intersection) >= 3
         remove actual sku from intersection
         generate all combinations of intersections
         add to each combination 'sku'
         add to tree_of_combinations
   create file using tree_of_combinations
```
