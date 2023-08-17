import requests
import pandas as pd
import geopandas as gpd

# Kakao REST API key
API_KEY = "57bb1cdf403802631778c8835c733a89"

# Convert address to coordinates
def convert_address_to_coordinates(address):
    api_url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}

    params = {"query": address}
    
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()

        if "documents" in result and len(result["documents"]) > 0:
            coordinates = result["documents"][0]["y"], result["documents"][0]["x"]
            return coordinates
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Add coordinates to dataframe
def add_coordinates_to_dataframe(df, address_column):
    latitudes = []
    longitudes = []

    for address in df[address_column]:
        coordinates = convert_address_to_coordinates(address)
        if coordinates:
            latitudes.append(coordinates[0])
            longitudes.append(coordinates[1])
        else:
            latitudes.append(None)
            longitudes.append(None)

    df["decimalLatitude"] = latitudes
    df["decimalLongitude"] = longitudes

# Convert CSV to GeoPackage
def csv_to_gpkg(input_csv, output_gpkg):
    df = pd.read_csv(input_csv)
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.decimalLongitude, df.decimalLatitude),
        crs="EPSG:4326",
    )
    gdf.to_file(output_gpkg, driver="GPKG")
    print("Data conversion and storage completed:", output_gpkg)
