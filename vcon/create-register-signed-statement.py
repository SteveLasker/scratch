"""
Create and Register a SCITT Signed Statement
TODO:
1. SET Environment Variables for DataTrails Access. 
    See  https://docs.datatrails.ai/developers/developer-patterns/getting-access-tokens-using-app-registrations/

    export DATATRAILS_CLIENT_ID=<your-id>
    export DATATRAILS_CLIENT_SECRET=<your-secret>
2. Set Unique Parameters for your submission
3. Execute this script, or paste into your python execution environment
   python create-register-signed-statement.py
"""

"""
Imports vvv
"""
import cbor2
import json

import hashlib

from ecdsa import SigningKey
from hashlib import sha256
from pycose import headers
from pycose.messages import Sign1Message
from pycose.keys.curves import P256
from pycose.keys.keyparam import KpKty, EC2KpX, EC2KpY, KpKeyOps, EC2KpCurve
from pycose.keys.keytype import KtyEC2
from pycose.keys.keyops import VerifyOp
from pycose.keys import CoseKey

from datatrails_scitt_samples.cbor_header_labels import (
    HEADER_LABEL_CWT_CNF,
    HEADER_LABEL_CNF_COSE_KEY,
    HEADER_LABEL_PAYLOAD_HASH_ALGORITHM,
    HEADER_LABEL_LOCATION,
)

from datatrails_scitt_samples.cose_sign1message import extract_to_be_signed

from datatrails_scitt_samples.statement_creation import (
    cose_key_ec2_p256,
    create_hashed_signed_statement,
    create_hashed_statement,
)

from datatrails_scitt_samples.scripts.register_signed_statement import (
    main as register_signed_statement,
)
"""
Imports ^^^
"""

"""
Set Unique Parameters vvv
"""
subject = "testsubject"
statement = {"author": "fred", "title": "my biography", "reviews": "mixed"}
payload_preimage_content_type = "application/json"
payload_hash_alg = "SHA-256"

kid = b"testkey"
issuer = "testissuer"
signing_key_file = "/tmp/my-signing-key.pem"
with open(signing_key_file, encoding="UTF-8") as file:
    signing_key = SigningKey.from_pem(file.read(), hashlib.sha256)

# Set an optional location for where the statement may be stored
payload_location = f"https://storage.example/{subject}"

# Provide optional Key/Value pairs for indexing
# uses: https://github.com/SteveLasker/cose-meta-map
meta_map_dict = {"key1": "value1", "key2": "42"}

"""
Set Unique Parameters ^^^
"""

"""
Generate a SCITT Signed Statement vvv
"""

# load the Statement
payload_contents = json.dumps(statement)

# Create a Hash of a statement
# uses: https://cose-wg.github.io/draft-ietf-cose-hash-envelope/draft-ietf-cose-hash-envelope.html

match payload_hash_alg:
    case "SHA-256":
        payload_hash = sha256(payload_contents.encode("utf-8")).digest()
    case _:
        raise ValueError(f"Unsupported Payload Hash Algorithm: {payload_hash_alg}")

verifying_key = signing_key.verifying_key

statement = create_hashed_statement(
    content_type=payload_preimage_content_type,
    issuer=issuer,
    kid=kid,
    subject=subject,
    meta_map=meta_map_dict,
    payload=payload_hash,
    payload_hash_alg=payload_hash_alg,
    payload_location=payload_location,
    verifying_key=verifying_key,
)

# This is compute_signature() from pycose's SignCommon (base of Sign1Message)
# without the key / alg consistency check
to_be_signed = extract_to_be_signed(statement)

# Send bytes to remote
alg = statement.get_attr(headers.Algorithm)
if alg is None:
    raise ValueError("Algorithm not set")
cose_signing_key = CoseKey.from_dict(cose_key_ec2_p256(signing_key))
# Receive signature bytes in response and set them on the statement
signature = alg.sign(key=cose_signing_key, data=to_be_signed)

# Now, locally, complete serialization of the statement with the signature attached

# This would be nice, but pycose doesn't appear to support it
# statement.signature = signature
# signed_statement = statement.encode(sign=False)

# Instead, we'll just encode directly following the implementation of encod
struct = [
    statement.phdr_encoded,
    statement.uhdr_encoded,
    statement.payload,
    signature,
]
signed_statement = cbor2.dumps(
    cbor2.CBORTag(statement.cbor_tag, struct),
    default=statement._custom_cbor_encoder,
)

with open("/tmp/signed-statement.cbor", "wb") as output_file:
    output_file.write(signed_statement)

"""
Generate a SCITT Signed Statement ^^^
"""

"""
Register a SCITT Signed Statement vvv
"""

# register the signed statement
register_signed_statement(
    [
        "--signed-statement-file",
        "/tmp/signed-statement.cbor",
    ]
)

"""
Register a SCITT Signed Statement ^^^
"""
