# bot-or-not

Basic bot identification based on instinctive arbitrary rules.
Results in lots of false positives as of now.

The aim in this project is to fetch the details about the followers of Indian Politicians, and then try to estimate
the number of followers which may be fake. A lot of parameters can be taken into consideration like,
* Number of followers of the follower
* Number of tweets of the follower
* Number of accounts followed by the follower
* Whether uses the default profile picture

Example : We can classify the follower as a fake follower if he follows three accounts, has 0 tweets, is
followed by 3 other twiiter handles, and uses the default profile picture.
Once, the details of a few politicians are collected, an attempt can be made to calculate the overlap among
different leaders of the same political party (Narendra Modi and Amit Shah), different leaders of different
party (Narendra Modi and Shashi Tharoor), and the leader and the handle of their party (Narendra Modi and
BJP).

- [x] get followers
- [x] compare followers
- [ ] optimize bot identification to reduce false positives
- [ ] sentiment analysis can be done on the activity (linking tweets, content of tweets) of users which
are common to two political parties, to determine if they are using the platform to polarize the opinion of
others on the platform.
- [ ] Deal with the small API rate limit for personal use (60 requests per hour, 5000 follower ids per request).