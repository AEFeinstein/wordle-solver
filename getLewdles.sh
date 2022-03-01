#!/bin/bash

curl 'https://bwnew2n3u5cina42gveozinmkq.appsync-api.us-west-1.amazonaws.com/graphql' \
  -H 'authority: bwnew2n3u5cina42gveozinmkq.appsync-api.us-west-1.amazonaws.com' \
  -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"' \
  -H 'dnt: 1' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36' \
  -H 'content-type: application/json; charset=UTF-8' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'x-amz-user-agent: aws-amplify/4.3.12 js' \
  -H 'x-api-key: da2-awhynspbnzg3dcnxuis5vqyu4e' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'origin: https://www.lewdlegame.com' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.lewdlegame.com/' \
  -H 'accept-language: en-US,en;q=0.9' \
  --data-raw '{"query":"query ListDicts($filter: ModelDictsFilterInput, $limit: Int, $nextToken: String) {\n  listDicts(filter: $filter, limit: $limit, nextToken: $nextToken) {\n    items {\n      id\n      Lewdles\n      LewdWords\n      createdAt\n      updatedAt\n    }\n    nextToken\n    startedAt\n  }\n}\n","variables":{}}' \
  --compressed

