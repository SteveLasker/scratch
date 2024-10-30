# SCITT Amend & Append Demo Script

## Minimal Asset Schema to Host the Event Centric Pending Update

  | DataTrails Attribute | Value           |
  | -                    | -               |
  | behaviours           | RecordEvidence  |
  | subject              | "$VCON_ID"      |
  | arc_display_type     | "vCon"          |
  | arc_display_name     | "vCon:$VCON_ID" |
  | public               | false           |

## Event Schema & SCITT Mapping

  | DataTrails Attribute | SCITT Header | SCITT Label      | Value           |
  | -                    | -            | -                | -               |
  | vcon_uuid            | protected    | subject          | <vcon_uuid>     |
  | arc_blob_hash_value  | protected    | payload          | <vcon-hash>     |
  | payload_location     | protected    | payload_location | <conserver_url> |
  | arc_blob_hash_alg    | protected    | payload_hash_alg | SHA-256         |
  | document_created     | protected    | meta-map.created | v.created_at    |
  | document_version     | protected    | meta-map.updated | v.updated_at    |
  | public               | n/a          | n/a              | False           |
  | arc_display_name     | n/a          | n/a              | "vCon:<vcon_uuid>" |
  | arc_display_type     | n/a          | n/a              | Update          |
  | -                    | -            | -                | -               |

1. Get a Fake vCon from the vCon Samples GitHub Repo

    ```bash
    # Fake vCon
    VCON_LOCATION="https://raw.githubusercontent.com/vcon-dev/fake-vcons/main/original_brisbane_vcons/fd5e12f5-ab6d-42d4-883e-140b01d7b15b.vcon.json"

    # Download the fake vCon
    curl -o /tmp/vcon1.json $VCON_LOCATION
    cat /tmp/vcon1.json | jq

    # Save vCon parameters for indexing within DataTrails
    VCON_ID=$(jq -r .uuid /tmp/vcon1.json)
    VCON_HASH=$(sha256sum "/tmp/vcon1.json" | cut -d ' ' -f 1)
    PAYLOAD_LOCATION=$VCON_LOCATION
    VCON_CREATED=$(jq -r .created_at /tmp/vcon1.json)
    VCON_UPDATED=$(jq -r .updated_at /tmp/vcon1.json)
    ```


1. Generate the minimal Asset content

    ```bash
    cat > /tmp/asset.json <<EOF
    {
      "behaviours": ["RecordEvidence"],
      "attributes": {
        "subject": "$VCON_ID"
        "arc_display_type": "vCon",
        "arc_display_name": "vCon:$VCON_ID",
      },
      "public": false
    }
    EOF
    ```

1. Post the Asset

    ```bash
    curl -X POST \
        -H "@$HOME/.datatrails/bearer-token.txt" \
        -H "Content-type: application/json" \
        -d "@/tmp/asset.json" \
        -o "/tmp/asset-created.json" \
        https://app.datatrails.ai/archivist/v2/assets
    ```

1. Get the Asset_ID

    ```bash
    ASSET_ID=$(jq .identity /tmp/asset-created.json)
    ```

1. Fetch the Asset

    ```bash
    curl -X GET \
        -H "@$HOME/.datatrails/bearer-token.txt" \
        https://app.datatrails.ai/archivist/v2/$ASSET_ID | jq
    ```

1. Create the vCon Event Content

    ```bash
    cat > /tmp/event.json <<EOF
    {
      "operation": "Record",
      "behaviour": "RecordEvidence",
      "event_attributes": {
        "arc_display_type":"vCon",
        "vcon_uuid":"$VCON_ID",
        "arc_blob_hash_value":"$VCON_HASH",
        "payload_location":"$PAYLOAD_LOCATION",
        "arc_blob_hash_alg":"SHA-256",
        "document_created":"$VCON_CREATED",
        "document_version":"$VCON_CREATED",
        "arc_display_name":"vCon:$VCON_ID"
      }
    }
    EOF
    ```

1. Create a DataTrails vCon Event

    ```bash
    curl -v -X POST \
        -H "@$HOME/.datatrails/bearer-token.txt" \
        -H "Content-type: application/json" \
        -d "@/tmp/event.json" \
        -o /tmp/event-created.json \
        https://app.datatrails.ai/archivist/v2/$ASSET_ID/events
    ```

1. View the created Event

    ```bash
    cat /tmp/event-created.json | jq
    ```

1. Create a Transcription Event
1. Create a Consent Event
1. Create a Transcription Update Event

    _**Note**_: the consent was for the original transcription.
    Does the user know there was a transcription error? 

1. Create a Revocation Event

    A revocation is scoped to the vCon, not a specific transcription.


   - `meta-map`
     - `"consent-type":"grant"`
     - `"consent-scope":"<vCon_ID>"`
     - `"consent-issuer":"steve.lasker@datatrails.ai"`
     - `"":""`
