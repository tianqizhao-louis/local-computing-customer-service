# Local Computing Customer Service

A simple service for managing customer data with options for local testing and GCP deployment.

---

## 🚀 Deployment Instructions

### 1. Local Testing Setup

Follow these steps to deploy the service locally:

#### Step 1: Create an `.env` File

Create an environment file to store your configuration variables:

```bash
vim .env
```

#### Step 2: Add the Following Content to .env

```bash
DATABASE_URL=<ENV>
JWT_SECRET_KEY=<ENV>
JWT_ALGORITHM=<ENV>
JWT_REFRESH_SECRET=<ENV>
CAT_API_KEY=<ENV>
```

#### Step 3: Activate Docker on Desktop

run the docker container:

```bash
./build.sh
```

The customer service will run on http://localhost:8081/api/v1/customers

### 2. Deploy to GCP

#### Option 1. Deploy through docker container

##### Step 1: Create an `prod.env` File

Create an environment file to store your configuration variables:

```bash
vim prod.env
```

##### Step 2: Add the Following Content to prod.env

```bash
DEP_DATABASE_URI=<ENV>
//Change URL_PREFIX to your corresponding ipv4
URL_PREFIX=<ENV>
DATABASE_URI=<ENV>

DB_USER=<ENV>
DB_PASS=<ENV>
DB_NAME=<ENV>
INSTANCE_UNIX_SOCKET=<ENV>
INSTANCE_CONNECTION_NAME=<ENV>
JWT_SECRET_KEY=<ENV>
JWT_ALGORITHM=<ENV>
JWT_REFRESH_SECRET=<ENV>

```

##### Step 3: Activate Docker on Desktop

run the docker container:

```bash
docker-compose -f docker-compose.prod.yml --env-file prod.env up --build -d
```

The customer service will run on http://external-ipv4:8081/api/v1/customers
