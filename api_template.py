from sentinelhub import SHConfig

config = SHConfig()

config.instance_id = "AAA"  # Replace with your actual instance ID
config.sh_client_id = "AAA"  # Replace with your actual client ID
config.sh_client_secret = "AAA"  # Replace with your actual client secret

if not config.sh_client_id or not config.sh_client_secret:
    raise ValueError("Please provide Sentinel Hub client credentials!")

