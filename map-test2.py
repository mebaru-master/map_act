# モジュールのインポート
import pandas as pd
import urllib
import urllib.error
import urllib.request

# Google API モジュール
#from pygeocoder import Geocoder
import googlemaps

API_KEY = 'AIzaSyAwRK1v-32Vx5I-Du33_BN2a2sSpD4sbbI'
# パラメータの設定
googleapikey = API_KEY
output_path = './output'
#pixel = '640x480'
pixel = '1024x768'
#scale = '18'
scale = '14'



def geocode_address(loc):
    # リストの初期化
    loc_dict = []

    # locationを変数にセット
    rows = loc

    # geocodeにより緯度・経度の情報をループ処理で取得
    for row in rows[0:]:
        print(row)
        print()
        gmaps = googlemaps.Client(key=googleapikey)
        geocode_result = gmaps.geocode(row)

        # loc
        loc = row
        # lat
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        # lng
        lng = geocode_result[0]["geometry"]["location"]["lng"]

        # results
        loc_dict.append({'loc': loc, 'lat': lat, 'lng': lng})

    # リスト型のloc_dictをデータフレームに変換
    df = pd.DataFrame(data=loc_dict)

    # 重複の削除
    df = df.drop_duplicates('loc')

    # データの出力
    df.to_csv(output_path + '\\loc.csv')


# defによる関数オブジェクトの作成
# 画像をダウンロードする
def download_image(loc):

    # データフレームから行列に変換
    lats = loc['lat'].values.tolist()
    lngs = loc['lng'].values.tolist()
    locs = loc['loc'].values.tolist()

    # htmlの設定
    html1 = 'https://maps.googleapis.com/maps/api/staticmap?center='

    # maptypeで取得する地図の種類を設定
    html2 = '&maptype=hybrid'

    # sizeでピクセル数を設定
    html3 = '&size='

    # sensorはGPSの情報を使用する場合にtrueとするので今回はfalseで設定
    html4 = '&sensor=false'

    # zoomで地図の縮尺を設定
    html5 = '&zoom='

    # マーカーの位置の設定（マーカーを表示させてくなければ無でも大丈夫）
    html6 = '&markers='

    # key="googleから取得したキーコード"となるように設定
    html7 = '&key='

    # 緯度経度の情報に該当する航空写真をループ処理で取得
    for lat, lng, loc in zip(lats, lngs, locs):

        # 緯度経度の情報をセット
        axis = str(lat) + "," + str(lng)

        # url
        url = html1 + axis + html2 + html3 + pixel + html4 + html5 + scale + html6 + axis + html7 + googleapikey

        # pngファイルのパスを作成
        dst_path = output_path + '\\' + str(loc) + ".png"

        # 画像を取得しローカルに書き込み
        try:
            data = urllib.request.urlopen(url).read()
            with open(dst_path, mode="wb") as f:
                f.write(data)

        except urllib.error.URLError as e:
            print(e)



# リストの初期化
location = []

# リストに場所や地名を追加する
#location = ["国会議事堂", "วัดพระแก้ว", "New York City", "Государственный Эрмитаж", "مكة المكرمة"]
location = ["富山駅","関西国際空港","Ninoy Aquino International airport terminal 2","Ninoy Aquino International airport terminal 4","Caticlan airport","Caticlan Jetty port","Boracay Jetty port","Boracay Nation"]
#location = ["富山駅","KIX"]

# リストの表示
print(location)
print()


# geocodeで取得できる情報の一覧の例（国会議事堂の場合）
gmaps = googlemaps.Client(key=googleapikey)
address = u'国会議事堂'
#address = u'富山駅'
#address = u'関西国際空港'
#address = 'Ninoy Aquino International airport'
#address = 'Caticlan airport'
#address = 'Caticlan Jetty port'
#address = 'Boracay Jetty port'
#address = 'Boracay Nation'
result = gmaps.geocode(address)
print(result)
print()


# 上記の取得情報一覧より緯度・経度の情報のみを抽出
lat = result[0]["geometry"]["location"]["lat"]
lon = result[0]["geometry"]["location"]["lng"]
print (lat,lon)
print()


# locationの緯度と経度の情報を取得する
geocode_address(location)

# 上記で出力したloc.csvをインポート
loc = pd.read_csv(output_path + '\\loc.csv', index_col = 'Unnamed: 0')

# 緯度経度の情報より画像を取得する
download_image(loc)


