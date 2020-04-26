# Movies DB

This script automatically updates the database if needed every time it runs, and allows you to perform certain actions
Describe TODO: --add, --highscores --compare_by

# Requirements

* python 3.7+
* installed packages from Pipfile
* **ENVIRONMENTAL VARIABLE OMDB_API_KEY** -> for demonstration purposes you can use mine: 

One time add on linux OS: `export OMDB_API_KEY="305043ae"`

# Features

* **SORTING** - sort data by given column(any column) in descdening orderd:

Example command: `python main.py --sort_by year`

Example output:

| Title | Year |
| --- | --- |
| Joker | 2019 |
| Parasite | 2019 |
| Green Book | 2018 |
| Coco | 2017 |
| Shazam | 2017 |


* **FILTERING** - filter data from a particular column with certain value. Available filters:

| Command | Description |
| --- | --- |
| `--filter_by cast [Actor]` | Filtering movies which cast contains a certain actor, i.e. `--filter_by cast "John Travolta"`  |
| `--filter_by director [Director]` | Filtering movies by certain director, i.e. `--filter_by director "Roman Polanski"` |
| `filter_by --language [Language]` | Filter movies in a certain language, i.e. `--filter_by language English` |
| `filter_by --box_office [operator] [amount]` | Filter movies by box_office earnings, i.e. `--filter_by box_office gte 100000000`, gte - greater than, equals; gt - greater than; e - equals; lte - less than, equals; lt - less than |
| `filter_by --awards oscars_nominated` | Filter movies which were nominated for Oscar, but didn't win |
| `filter_by --awards awards_won_precentage [operator] [amount]` | Filter movies with certain awards won percentage, i.e. `--filter_by awards awards_won_percentage 80` |


Example command: `python main.py --filter_by awards awards_won_percentage lte 20`

Example output:

| Title | Awards |
| --- | --- |
| The Prestige | Nominated for 2 Oscars. Another 6 wins & 38 nominations. |
| Batman Begins | Nominated for 1 Oscar. Another 14 wins & 72 nominations. |
| Shutter Island | 11 wins & 65 nominations. |

