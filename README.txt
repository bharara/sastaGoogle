README
=================================
= FILES

=== FileAddWriter.py
This file writes the file address, keys (hash value of the address) and category of the files in the file table in the database

=== ForwardIndex.py 
It is the intial code that wrote into the database without sorting.
The crosponding SQL schema had primary key (fileID, wordID)

=== ReverseIndexMain.py
It is the main py file that sort all the dataset based on wordID (reverse Indexing) and then store it into database.

=== Google.sql
It is the database schema. It includes two tables
====== files
Include fileAddress, category and hash value. It is poppulated by FileAddWriter.py
====== wordfile
includes fileID, wordID and score (based on count and importance in text). It is sorted by (wordID, fileID) based on reverse indexing

=====================================
= Dependencies
=== pymysql
=== BeautifulSoup4

=====================================

= Group Members
=== Abdul Hadi
=== Abdullah Saeed
=== M. Hamza Zahid
=== Muhammad Bilal

=====================================

=Others

=== The root folder of dataset storage and database password are hardcoded in each file
=== Dataset can be download in it's entierity @ https://dumps.wikimedia.org/other/static_html_dumps/current/simple/wikipedia-simple-html.tar.7z