# Secure Public API Endpoint

This project provides a secure public API endpoint hosted on a serverless platform, allowing users to interact with the API using various client applications. The API endpoint is designed to meet specific requirements, including authentication, rate limiting, and streaming capabilities.

## Features

- Authentication using bearer tokens in the format "USER{XXX}" where XXX is a 3-digit numeric ID.
- Rate limiting each user ID to 4 requests per minute.
- Support for streaming responses with configurable delay.
- Securely hosted on a serverless platform (Cloudflare Workers, Azure Functions, or Google Cloud Functions) using free tiers.

## Usage

### Public Endpoint URL

The API endpoint is hosted at [INSERT_PUBLIC_ENDPOINT_URL_HERE](#).

### API Documentation

#### Endpoint: `/api`

- **Method**: `GET`
- **Query Parameters**:
  - `stream`: Set to "true" or "false" to enable/disable streaming responses.
- **Headers**:
  - `Authorization`: Bearer token in the format "USER{XXX}".
- **Response**:
  - JSON object with the following properties:
    - `message`: Customized welcome message including user ID and visit number.
    - `group`: Hashed integer between 1-10 derived from the user ID.
    - `rate_limit_left`: Number of requests remaining in the current rate limit window.
    - `stream_seq`: Sequence number that increments on each response when streaming is enabled.

### Example Client Code

#### cURL

```bash
# Request with streaming enabled
curl -X GET "INSERT_PUBLIC_ENDPOINT_URL_HERE/api?stream=true" -H "Authorization: Bearer USER123"

# Request with streaming disabled
curl -X GET "INSERT_PUBLIC_ENDPOINT_URL_HERE/api?stream=false" -H "Authorization: Bearer USER123"
