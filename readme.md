# DNS Updater

This project automates the updating of DNS records for your domain using Cloudflare or Vercel's API. It runs a Python script periodically to check and update your DNS record with your current public IP address.

## Prerequisites

- Docker installed on your system

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd dns-updater
   ```

2. **Set up your environment:**

   - Create a `.env` file based on `.env.example` and fill in your Vercel API token (`VERCEL_TOKEN`), domain (`DOMAIN`), record name (`RECORD_NAME`), team id (`TEAM_ID`).

3. **Build the Docker image:**

   ```bash
   docker build -t dns-updater .
   ```

4. **Run the Docker container:**

   ```bash
   docker run -d --restart unless-stopped --env-file .env dns-updater
   ```

5. **Verify operation:**

   Check the logs to ensure the script is running and updating DNS records as expected:

   ```bash
   docker logs <container-id>
   ```

## Configuration

- **Environment Variables:**
  - `VERCEL_TOKEN`: Your Vercel API token for authentication.
  - `DOMAIN`: Your domain name (e.g., `kendre.me`).
  - `RECORD_NAME`: The subdomain whose DNS record you want to update.
  - `TEAM_ID`: The id of the team in which the domain resides

## Troubleshooting

- Ensure your `.env` file is correctly configured with valid credentials.
- Check Vercel's API rate limits if you encounter issues with frequent updates.

## Contributing

Feel free to contribute by submitting issues or pull requests.