import openeo

# Connect to openEO backend
connection = openeo.connect("https://openeo.cloud")
connection.authenticate_oidc()  # Authenticate if required

# List available collections in the connected backend
collections = connection.list_collections()

print(connection.describe_account())