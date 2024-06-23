from flask import Flask, render_template
import folium
from data import buildings

app = Flask(__name__)

@app.route('/')
def index():
    # 지도 중심의 위도와 경도를 설정합니다.
    latitude = 37.53530388483148
    longitude = 126.64689286992314

    # 지도를 생성합니다. 줌 컨트롤을 비활성화하고, 최대 줌 레벨과 최소 줌 레벨을 설정합니다.
    mymap = folium.Map(location=[latitude, longitude], zoom_start=17, max_zoom=18, min_zoom=15, zoom_control=True)

    # 구글 맵 타일을 추가합니다.
    tile_layer = folium.TileLayer(
        tiles='https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Maps',
        overlay=True,
        control=False,
        subdomains=['mt0', 'mt1', 'mt2', 'mt3']
    )
    tile_layer.add_to(mymap)

    # 위치별로 정보를 통합합니다.
    combined_buildings = {}
    for building in buildings:
        loc = tuple(building["location"])
        if loc not in combined_buildings:
            combined_buildings[loc] = []
        combined_buildings[loc].append(building)

    # 통합된 정보로 마커를 추가합니다.
    for loc, buildings_at_loc in combined_buildings.items():
        popup_texts = [f"{b['name']}<br>남자 화장실 비밀번호: {b['male_password']}<br>여자 화장실 비밀번호: {b['female_password']}" for b in buildings_at_loc]
        popup_text = "<br><br>".join(popup_texts)
        folium.Marker(
            location=list(loc),
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(mymap)

    # 지도를 HTML 문자열로 저장합니다.
    map_html = mymap._repr_html_()

    title = '당신에게도 언젠가 그 날은 찾아온다.'
    subtitle = '청라 화장실 비번 리스트'

    return render_template('index.html', title=title, subtitle=subtitle, buildings=buildings, map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
