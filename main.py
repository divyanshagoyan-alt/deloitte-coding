import json, unittest, datetime
import pandas as pd
with open("data-1.json","r",  encoding="utf8") as f:
     jsonData1 = json.load(f)
jsonData1
with open("./data-2.json","r",encoding="utf8") as f:
    jsonData2 = json.load(f)
jsonData2
with open("./data-result.json","r",encoding="utf8") as f:
    jsonExpectedResult = json.load(f)
jsonExpectedResult
def convertFromFormat1 (jsonObject):
    # Split location into country, city, area, factory, section
    loc = jsonObject['location'].split('/')
    
    # Convert timestamp from milliseconds to ISO format with Z
    ts_ms = jsonObject['timestamp']
    dt = datetime.datetime.fromtimestamp(ts_ms / 1000.0, tz=datetime.timezone.utc)
    ts_iso = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    return {
        "device": {
            "id": jsonObject['deviceID'],
            "type": jsonObject['deviceType']
        },
        "timestamp": ts_iso,
        "country": loc[0],
        "city": loc[1],
        "area": loc[2],
        "factory": loc[3],
        "section": loc[4],
        "data": {
            "status": jsonObject['operationStatus'],
            "temperature": jsonObject['temp']
        }
    }

def convertFromFormat2 (jsonObject):
    # Format 2 is already in the unified format based on data-result.json
    return jsonObject
def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result
class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()