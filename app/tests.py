import requests
import pandas as pd
import io
import gzip

def test_create_file():
    url = "http://localhost:8000/file"
    data = {
        "name": ["John", "Jane", "Bob"],
        "age": [30, 25, 40],
        "salary": [50000, 60000, 70000]
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/gzip'
    assert response.headers['Content-Disposition'] == 'attachment; filename="file.csv.gz"'
    content = gzip.decompress(response.content).decode('utf-8')
    df = pd.read_csv(io.StringIO(content))
    assert set(df.columns) == set(["name", "age", "salary"])
    assert df.shape == (3, 3)
