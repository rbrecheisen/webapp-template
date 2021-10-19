# webapp-template
Template project using NGINX, Django, Bootstrap and Docker

## server

## server_v2

- write failing test. question is what is this test supposed to test? think in terms of acceptance testing. we have a REST app but also want to have an HTML front-end. so consider we have a single view that responds to both JSON and HTML requests. you can start with the index() view. can i write a test that checks the response type depending on a query parameter format=json or format=html?
- [done] get skeleton app (HTML only) up-and-running