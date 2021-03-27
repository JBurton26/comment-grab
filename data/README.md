# Data Folder
This folder is ignored by git,
Processed JSON files are in the format:
```
# NOTE: DOES NOT REPRESENT ACTUAL POST #
{
  "created": "2021-01-23 12:34:56",
  "images": "",
  "name": "t3_iytrfh",
  "permalink": "www.reddit.com/r/example/comments/iytrfh/my_post/",
  "score": 1234,
  "title": "My Post",
  "upvote_ratio": 0.99,
  "user": "redd1tor_",
  "xcomments":[
    {
        "body": "example comment!",
        "created": "2021-01-24 10:56:40",
        "id": "t1_gybb5kl",
        "parentComment": "t3_iytrfh",
        "score": 23,
        "user": "reddi_two"
    },
    {
        "body": "wow good point",
        "created": "2021-01-24 11:22:34",
        "id": "t1_gybb8jn",
        "parentComment": "t1_gybb5kl",
        "score": 11,
        "user": "r3dd"
    }
  ]
}
```
