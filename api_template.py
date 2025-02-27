from sentinelhub import SHConfig

config = SHConfig()

config.instance_id = "Aengus_Dzud_2025"  # Replace with your actual instance ID
config.sh_client_id = "e8b53aa1-3e64-45f5-ba56-fcf9562f3acc"  # Replace with your actual client ID
config.sh_client_secret = "CGqBWL3rvVLrpyd6KbaIXd6LJh96zb0B"  # Replace with your actual client secret

if not config.sh_client_id or not config.sh_client_secret:
    raise ValueError("Please provide Sentinel Hub client credentials!")

