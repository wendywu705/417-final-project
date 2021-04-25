To generate test files run the following code:

A= number of tests ie. 100  
B= number of moves backwards from goal state ie. 50    
C= filename ie. 15pz_1.txt

run in command line: `generate8_tests.py $A $B $C`  
for example: `generate8_tests.py 100 50 8pz_1.txt`
  
Or if generating 15puzzle test files... same format.  
ie. `generate15_tests.py 100 50 15pz_1.txt`  

Generated test files will be stored in the same directory.  
