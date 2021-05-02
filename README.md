# UNFINISHED
# Redapi Scraper
An implementation of the reddit api for data collection purposes.
Parses JSON responses to streamlined JSON and CSV formats.
## TODO
- [ ] Integrate Front-end
- [x] Save to CSV Format
- [x] Implement Logging
- [ ] Release as executable
- [ ] Release as library?
- [ ] Implement Parsing of data to .xls or .xlsx format
## Usage
### Setup
After cloning the repository or downloading and extracting the code zip file, run the following command to set up the environment for the scripts while in the extracted folder:
```bash
$ pip install -r requirements.txt
```
This should install the relevant requirements.
To run the script, it requires 2 config files to be created and
### Example python script
```python
from infoget import getComments

def main():
  search_data = {
    "sorting":"top",  # top posts (Currently configured to year)
    "limit": 10,      # limit to 10 posts
    "subreddit":"linux"   # search linux subreddit, could be any subreddit
  }
  result = getComments(search_data)
  if result != 0: # successful execution returns 0
    print("Error: ", result)
  else:
    print("Success")

if __name__ == "__main__":
  main()
```
