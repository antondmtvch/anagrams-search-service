# anagrams-search-service

This is a simple async service for finding anagrams in the redis database.

## What you need

* Redis 2.5.4
* Python 3.7.4

## Usage

### Load words list

```buildoutcfg
curl -X POST http://localhost:8080/load -H 'content-type: application/json' -d '{"words": ["foobar", "aabb", "baba", "boofar", "test"]}'
```

* Result
```buildoutcfg
200: OK
```
### Get anagrams

```buildoutcfg
curl -X GET 'http://localhost:8080/get?word=foobar'
```

* Result
```json
[
    "boofar",
    "foobar"
]
```

```buildoutcfg
curl -X GET 'http://localhost:8080/get?word=qwe'
```

* Result
```json
null
```