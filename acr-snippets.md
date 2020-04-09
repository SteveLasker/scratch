# ACR Snippets

A collection of snippets I find useful.

## ACR Update via REST

```bash
az configure --defaults acr=demo42
export RESOURCE_ID=$(az acr show --query id -o tsv)
az rest --method patch --uri "$RESOURCE_ID?api-version=2019-12-01-preview" --body "{ \"properties\":{\"dataEndpointEnabled\":true}}" -o json
```

Look for:

```bash
"dataEndpointEnabled": true,
    "dataEndpointHostNames": [
      "demo42.eastus.data.azurecr.io"
```

## Validating Data Endpoints

```bash
curl https://demo42.azurecr.io/v2/hello-world/blobs/sha256:cffb9574bda6e04e10c7262083ce27b96e756fb4affdedfc1f66e5aabdf89426
```
