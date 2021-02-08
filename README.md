
# database-and-plotter
A database that uses a book’s title, chapter count, and word count per chapter. This information is stored in a SQL database as well as a tuple. The database and tuple are passed to a plotter program which displays a multi bar graph with the chapter numbers on the x-axis and the word count per chapter as the y-axis. 

Demonstrates usage of SQL, matplotlib and seaborn plotting 

Database Input: Book title, Book chapter count, Book page count per chapter 

Database Output: tuple containing Book titles, chapter counts, page counts per chapter, SQLAlchemy Database 

Plotter Input: tuple containing Book titles, chapter counts, page counts per chapter, SQLAlchemy Database 

Plotter Output: Plot comparing chapter number to word count for each Title
