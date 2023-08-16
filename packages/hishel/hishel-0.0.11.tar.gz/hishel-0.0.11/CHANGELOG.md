# Changelog

## 0.0.11 (8/15/2023) 

- Add support for request `cache-control` directives. (#42)
- Drop httpcore dependencie. (#40)
- Support HTTP methods only if they are defined as cacheable. (#37)

## 0.0.10 (8/7/2023) 

- Add Response metadata. (#33)
- Add API Reference documentation. (#30)
- Use stale responses only if the client is disconnected. (#28)

## 0.0.9 (8/1/2023) 

- Expose Controller API. (#23)

## 0.0.8 (7/31/2023)

- Skip redis tests if the server was not found. (#16)
- Decrease sleep time for the storage ttl tests. (#18)
- Fail coverage under 100. (#19)

## 0.0.7 (7/30/2023)

- Add support for `Heuristic Freshness`. (#11)
- Change `Controller.cache_heuristically` to `Controller.allow_heuristics`. (#12)
- Handle import errors. (#13)

## 0.0.6 (7/29/2023)

- Fix `Vary` header validation. (#8)
- Dump original requests with the responses. (#7) 

## 0.0.5 (7/29/2023)

- Fix httpx response streaming.

## 0.0.4 (7/29/2023)

- Change `YamlSerializer` name to `YAMLSerializer`.

## 0.0.3 (7/28/2023)

- Add `from_cache` response extension.
- Add `typing_extensions` into the requirements.

## 0.0.2 (7/25/2023)

- Add [redis](https://redis.io/) support.
- Make backends thread and task safe.
- Add black as a new linter.
- Add an expire time for cached responses.
