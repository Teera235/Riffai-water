"""
Major rivers data for Thailand
"""

MAJOR_RIVERS = {
    "mekong": {
        "name": "แม่น้ำโขง",
        "name_en": "Mekong River",
        "length_km": 4350,
        "basin_id": "mekong_north",
        "coordinates": [
            [20.5, 100.1],
            [20.3, 100.2],
            [20.0, 100.4],
            [19.8, 100.5],
            [19.5, 100.6],
            [19.2, 100.7],
            [18.9, 100.8],
            [18.5, 100.9],
            [18.0, 101.0],
            [17.5, 101.2],
            [17.0, 101.5],
            [16.5, 102.0],
            [16.0, 102.5],
            [15.5, 103.0],
        ],
        "tributaries": ["แม่น้ำกก", "แม่น้ำอิง", "แม่น้ำฝาง"],
    },
    "chao_phraya": {
        "name": "แม่น้ำเจ้าพระยา",
        "name_en": "Chao Phraya River",
        "length_km": 372,
        "basin_id": "central",
        "coordinates": [
            [15.7, 100.1],
            [15.5, 100.2],
            [15.2, 100.3],
            [15.0, 100.3],
            [14.8, 100.3],
            [14.5, 100.4],
            [14.2, 100.4],
            [14.0, 100.5],
            [13.8, 100.5],
            [13.7, 100.5],
            [13.5, 100.5],
        ],
        "tributaries": ["แม่น้ำปิง", "แม่น้ำวัง", "แม่น้ำยม", "แม่น้ำน่าน"],
    },
    "chi": {
        "name": "แม่น้ำชี",
        "name_en": "Chi River",
        "length_km": 765,
        "basin_id": "eastern_coast",
        "coordinates": [
            [16.5, 101.5],
            [16.3, 101.7],
            [16.0, 102.0],
            [15.8, 102.3],
            [15.5, 102.5],
            [15.3, 102.8],
            [15.0, 103.0],
            [14.8, 103.3],
            [14.5, 103.5],
        ],
        "tributaries": ["แม่น้ำมูล"],
    },
    "mun": {
        "name": "แม่น้ำมูล",
        "name_en": "Mun River",
        "length_km": 673,
        "basin_id": "eastern_coast",
        "coordinates": [
            [15.5, 101.5],
            [15.3, 101.8],
            [15.0, 102.0],
            [14.8, 102.3],
            [14.5, 102.5],
            [14.3, 102.8],
            [14.0, 103.0],
            [13.8, 103.3],
            [13.5, 103.5],
        ],
        "tributaries": [],
    },
    "bang_pakong": {
        "name": "แม่น้ำบางปะกง",
        "name_en": "Bang Pakong River",
        "length_km": 230,
        "basin_id": "eastern_coast",
        "coordinates": [
            [14.5, 101.0],
            [14.3, 101.1],
            [14.0, 101.2],
            [13.8, 101.3],
            [13.5, 101.4],
            [13.3, 101.5],
        ],
        "tributaries": ["แม่น้ำนครนายก"],
    },
    "tapi": {
        "name": "แม่น้ำตาปี",
        "name_en": "Tapi River",
        "length_km": 230,
        "basin_id": "southern_east",
        "coordinates": [
            [9.5, 99.0],
            [9.3, 99.2],
            [9.0, 99.3],
            [8.8, 99.4],
            [8.5, 99.5],
        ],
        "tributaries": [],
    },
    "pattani": {
        "name": "แม่น้ำปัตตานี",
        "name_en": "Pattani River",
        "length_km": 214,
        "basin_id": "southern_east",
        "coordinates": [
            [7.0, 101.0],
            [6.8, 101.1],
            [6.5, 101.2],
            [6.3, 101.3],
            [6.0, 101.4],
        ],
        "tributaries": [],
    },
}

def get_rivers_geojson():
    """Convert rivers data to GeoJSON format"""
    features = []
    
    for river_id, river in MAJOR_RIVERS.items():
        feature = {
            "type": "Feature",
            "properties": {
                "id": river_id,
                "name": river["name"],
                "name_en": river["name_en"],
                "length_km": river["length_km"],
                "basin_id": river["basin_id"],
                "tributaries": river["tributaries"],
                "type": "river",
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [[lon, lat] for lat, lon in river["coordinates"]],
            },
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features,
    }
