# Analyzing International Tennis Matches

## Team Members
* Tina Truong 
* Pratheek Pala 
* Shakshi Sharma
* Md Waez Sufi Islam 
* Updesh Sachdeva

## Data Set Description
__Source:__ Kaggle - Huge Tennis Database   
__Link:__ https://www.kaggle.com/datasets/guillemservera/tennis/data      
__File format(s):__ .csv       
__Original Compression:__ ZIP archive   
__Stored format:__ Uncompressed CSV files in project directory  

## Data Set Files
1. atp_matches.csv
2. atp_matches_qual_chall.csv
3. atp_players.csv
4. atp_rankings.csv


## Data Set Features
__Row Counts:__ 193337, 216430, 65019, 3235639 respective to data set files 1-4     
__Column Counts:__ 49, 49, 8, 4 respective to data set files 1-4    
__Delimeters:__ Comma (,)   
__Header Presence:__ All 4 files contain headers as their first lines. Comma seperated.     
__Encoding:__ ASCII text    
__File Sizes:__ 34 MB, 39 MB, 2.4 MB, 71 MB respective to data set files 1-4

## Quality Notes:

* Most modern tournaments have all fields filled out. However, detailed match stats like aces (w_ace), double faults (w_df), match minutes, etc have less data because that precise level of tracking did not start until the late 90s. 

* Some winner / loser seeds columns may be blank which is expected as those are reserved for top players. 

* The winner / loser entry columns are mostly blank because the majority of players qualify for tournaments through the standard ranking process. These columns only record special exceptions like Qualifiers (Q) or Wild Cards (WC). Since these cases are less common, empty fields are to be expected.        

## Anamoly ID's 

* Most tournaments have a 3 or 4-digit code (like 2023-540 for Wimbledon). However, Davis Cup, for example, has a different format such as 2023-D015 or M-DC-2023-WG2-PO-EST-JAM-01.

* It is also important to note the different formats for scoring which include 0-6 6-4 6-2 or 6-7(5) 7-6(3) 6-4 or even 5 set games. The number in parentheses is the loser’s tiebreaker score. 


