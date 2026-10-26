
```markdown
# Serverless URL Shortener

A simple, fast URL shortener deployed on Azure Functions, featuring automated CI/CD deployment via GitHub Actions.

## 🚀 Features
- **Shorten URLs:** Generate a secure, random 6-character code for any valid HTTPS URL.
- **Instant Redirects:** Use the short code to get an HTTP 302 redirect to the original destination.
- **Serverless Architecture:** Built on the Azure Functions Python v2 programming model for automatic scaling.
- **Fast Data Access:** Uses Azure Table Storage for quick, NoSQL lookups.
- **CI/CD Pipeline:** Automatically builds and deploys to Azure whenever changes are pushed to the `main` branch.

## 🛠️ Tech Stack
- **Compute:** Azure Functions (Python 3.13)
- **Database:** Azure Table Storage (`azure-data-tables`)
- **Dependency Management:** `uv`
- **Deployment:** GitHub Actions & Azure Oryx (Remote Build)

## 🔌 API Endpoints

### 1. Create a Short URL
**`POST /api/shorten`**

**Request Body:**
```json
{
  "url": "https://www.python.org/doc/"
}
```

**Response:**
```json
{
  "short_url": "https://<your-app-name>.azurewebsites.net/api/aB3xK9",
  "code": "aB3xK9"
}
```

### 2. Redirect to Original URL
**`GET /api/{code}`**

Returns an HTTP `302 Found` with a `Location` header pointing to the original long URL.

## 💻 Running Locally

### Prerequisites
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- [uv](https://github.com/astral-sh/uv) for Python dependency management
- An Azure Storage Account

### Setup
1. Clone the repository and navigate into the directory:
   ```bash
   git clone <your-repo-url>
   cd url-shortener
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Create a `local.settings.json` file in the root directory (this file is gitignored for security):
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "UseDevelopmentStorage=true",
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net"
     }
   }
   ```
   *(Replace the `STORAGE_CONNECTION_STRING` with your actual Azure Storage connection string).*

4. Start the local development server:
   ```bash
   func start
   ```

5. Test the endpoint locally:
   ```bash
   curl -X POST http://localhost:7071/api/shorten \
     -H "Content-Type: application/json" \
     -d '{"url":"https://www.python.org/doc/"}'
   ```

## ⚙️ Deployment
This project uses GitHub Actions for automated deployment. Any push to the `main` branch triggers a remote build on Azure (using `requirements.txt` to install dependencies) and deploys the updated function app. 

*(Note: To update dependencies for deployment, run `uv export --format requirements.txt --no-dev --no-hashes --output-file requirements.txt` before pushing.)*
```
