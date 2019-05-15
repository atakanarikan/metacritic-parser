### How to run the app:
* `docker build . -t <your_tag_name>`
* `docker run -p <port>:<port> <your_tag_name>`  # can specify docker flags (`-d` etc)

    Visit `http://localhost:<port>/games`  # port is the one specified when running the container
    
### How to run the tests:
* `docker build . -f DockerfileTesting -t <your_test_tag_name>`
* `docker run <your_test_tag_name>`
 
