import msal

def acquire_obo_token(user_assertion_token: str) -> str:
    # 1. Initialize configuration variables
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"
    authority = "https://microsoftonline.com"

    # The downstream scopes your backend application needs to access
    scopes = ["https://graph.microsoft.com/.default"]

    # 2. Build the Confidential Client Application
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority
    )

    # 3. Look for a valid token in the cache first (Best Practice)
    # The cache key for OBO is uniquely tied to the user assertion
    user_assertion_hash = msal.ConfidentialClientApplication.OBO_USER_ASSERTION_HASH

    # 4. Request the token using the OBO flow
    result = app.acquire_token_on_behalf_of(
        user_assertion=user_assertion_token,
        scopes=scopes
    )

    # 5. Extract and return the new access token
    if "access_token" in result:
        return result["access_token"]
    else:
        error_msg = result.get("error")
        error_desc = result.get("error_description")
        raise Exception(f"OBO Token Exchange Failed: {error_msg} - {error_desc}")

# Example usage:
# Extracted from HTTP Authorization header
# incoming_jwt = "eyJ0eXAiOiJKV1QiLC..." 
# downstream_token = acquire_obo_token(incoming_jwt)