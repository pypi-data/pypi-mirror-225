# `Google Finance Scraper`

The `Google Finance Scraper` is a simple testing example to understand the basics of developing your first Python package. 

## Deployment

* Socketify
  * Build:
    ```shell
    docker build -f Dockerfile-socketify -t socketify/develop:0.1 .
    ```
  * Temp Run (bash):
    ```shell
    docker run --name socketify-service --rm -it --network host socketify/develop:0.1 bash
    ```
* API Service
  * Build:
    ```shell
    docker build --no-cache -t scraper-service/develop:0.1 . --build-arg GIT_COMMIT=$(git rev-parse HEAD)
    ```
  * Run:
    ```shell
    docker run --name scraper-api-service --rm -it --network host scraper-service/develop:0.1
    ```
