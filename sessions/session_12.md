# Session 12
### [👉 Watch the session recordings]()

### [👉 Slides]()

## Goals 🎯

- [x] Prediction generator service
    - [x] Load latest features from the online feature store
    - [x] Implement .predict() method to generate predictions.
    - [x] Add custom Quix Streams sink to save predictions to Elastic Search
        - [x] Spin up Elastic Search locally with docker compose. 
        - [x] Save predictions from our inference.py to Elastisearch
        - [x] Dockerize both the training and the inference.

- [ ] REST API in Rust
    - [ ] Boilerplate server with actix-web
    - [ ] /predict endpoint that gets predictions from ES and serves them to the client app.
## Questions