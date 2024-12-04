"""
Create and Register a SCITT Signed Statement
TODO:
1. Set Environment Variables for DataTrails Access. 
    See  https://docs.datatrails.ai/developers/developer-patterns/getting-access-tokens-using-app-registrations/

    export DATATRAILS_CLIENT_ID=<your-id>
    export DATATRAILS_CLIENT_SECRET=<your-secret>
2. Set Environment Variables for DigiCert Software Trust Manager 
    export DIGICERT_CLIENT_ID=<your-id>
    export DIGICERT_CLIENT_SECRET=<your-secret>
3. Set Unique Parameters for your submission
4. Execute this script, or paste the code into your python execution environment
   python create-register-signed-statement.py
"""

# Imports vvv
from datatrails_scitt_samples import (
    create_hashed_signed_statement,
    create_hashed_statement,
    register_signed_statement,
)

from digicert import (
    digicert_stm,
)

# Set Unique Parameters vvv
subject = "testsubject"
statement = {"author": "fred", "title": "my biography", "reviews": "mixed"}
content_type = "application/json"
payload_hash_alg = "SHA-256"
kid = b"testkey"

# Set an optional location for where the statement may be stored
payload_location = f"https://storage.example/{subject}"

# Provide optional Key/Value pairs for indexing
# uses: https://github.com/SteveLasker/cose-meta-map
meta_map_dict = {"key1": "value1", "key2": "42"}

# Generate an Unsigned SCITT Statement vvv
statement = create_hashed_statement(
    content_type=content_type,
    payload=statement,
    payload_hash_alg=payload_hash_alg,
    subject=subject,
    meta_map=meta_map_dict,
    payload_location=payload_location,
)

# Sign with DigiCert Software Trust Manager
signed_statement = digicert_scitt_sign(
    kid = kid,
    statement = statement,
)

# Register on DataTrails
transparent_statement = register_signed_statement(
    signed_statement = signed_statement,
)

if transparent-statement is None:
    raise ResponseContentError("Registration Failed")

"""
Register a SCITT Signed Statement ^^^
"""
