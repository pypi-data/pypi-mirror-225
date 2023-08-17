# Latest Indonesia Earthquake
This package will get the latest earthquake from BMKG | Meteorological, Climatological, and Geophysical Agency

## HOW IT WORKS?
This package will scrape from [BMKG](https://bmkg.go.id) to get latest quake happened in Indonesia.

This package using BeautifulSoup4 and Request, for creating output JSON which ready to use in web or mobile applications.

## HOW TO USE?
```
import gempaterkini

if __name__ == '__main__':
    print('Aplikasi utama')
    result = gempaterkini.ekstraksi_data()
    gempaterkini.tampilkan_data(result)
```

# AUTHOR
Mishbahussuduri