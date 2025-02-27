from sentinelhub import SentinelHubRequest, MimeType, bbox_to_dimensions, BBox, CRS
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('Agg')  # Use a non-interactive backend
from copernicus_test import config

# Define bounding box (longitude, latitude) for Bath
bath_bbox = BBox(bbox=[-2.414, 51.366, -2.324, 51.412], crs=CRS.WGS84)

#image resolution (10m per pixel)
resolution = 10
size = bbox_to_dimensions(bath_bbox, resolution=resolution)

#Sentinel-1 SAR evalscript (VV Polarization)
evalscript_sar = """
//VERSION=3
function setup() {
    return {
        input: ["VV"],
        output: { bands: 1 }
    };
}
function evaluatePixel(sample) {
    return [sample.VV];
}
"""


# Make Sentinel-1 API request
request = SentinelHubRequest(
    evalscript=evalscript_sar,
    input_data=[{
        "type": "S1GRD",  # Correct Sentinel-1 dataset type (GRD - Ground Range Detected)
        "dataFilter": {
            "timeRange": {
                "from": "2025-02-07T00:00:00Z",
                "to": "2025-02-12T23:59:59Z"
            },
            "mosaickingOrder": "mostRecent",
            "acquisitionMode": "IW",  # Interferometric Wide Swath (most common)
            "polarization": "DV",  # Dual polarization (VV + VH)
            "orbitDirection": "DESCENDING"  # Use descending orbit data
        },
        "processing": {
            "orthorectify": True,  # Corrects geometric distortions
            "backCoeff": "GAMMA0_TERRAIN"  # Use GAMMA0 backscatter coefficient
        }
    }],
    bbox=bath_bbox,
    size=size,
    config=config,
    responses=[SentinelHubRequest.output_response("default", MimeType.PNG)]
)

# Get image data
image_data = request.get_data()[0]

# Display image
plt.figure(figsize=(10, 10))
plt.imshow(np.clip(image_data / 255, 0, 1))
plt.title("Sentinel-2 True Color Image - Bath, UK")
plt.axis("off")
plt.savefig("sentinel_image.png", dpi=300, bbox_inches='tight')
print("Image saved as 'sentinel_image.png")
