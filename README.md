## boot.dev

boot.dev is an internet learning platform for backend developers. It provides courses on Python, DSA, JavaScript, HTTP, Golang, Servers, SQL, Docker, etc. Throughout the course the students are supposed to complete 3 personal projects.

## boot analyzer

This small CLI tool uses boot.dev api to get information about some of the users of boot.dev that are present in the leaderboard. It provides a quick overview of how many people have completed the personal projects and if they have a public github account.

I hope this tool will be useful to anyone who want to have a look at the projects made by the users of boot.dev

### running the script

The boot analyzer sends up to 34 GET requests to the boot.dev api. There is a 2 second timeout between the requests, so running the program takes around a minute of your time. The script prints intermediate results as soon as the api responses arrive.

