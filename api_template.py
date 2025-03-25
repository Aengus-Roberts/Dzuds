from sentinelhub import SHConfig

config = SHConfig()

config.sh_client_id = "AAA"  # Replace with your actual client ID
config.sh_client_secret = "AAA"  # Replace with your actual client secret
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
config.sh_base_url = "https://sh.dataspace.copernicus.eu"
config.save("cdse")

if not config.sh_client_id or not config.sh_client_secret:
    raise ValueError("Please provide Sentinel Hub client credentials!")

