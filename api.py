import requests
import urllib
import json
import pandas as pd
from os import path

def get_api(url):
    result = requests.get(url)
    return result.json()

### 課題1：商品名と価格の一覧を取得
def study_1():
    keyword = input("検索したいキーワードを入力してください。：")
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&formatVersion=2&keyword={}&applicationId=1019079537947262807&elements=itemName,itemPrice".format(keyword)
    items_json = get_api(url)
    print("■ 商品一覧")
    for item in items_json["Items"] :
        print("商品名：" + item["itemName"])
        print("価格  ：" + str(item["itemPrice"]) + "\n")
    print('---------------------------------------------------------------------------------------------------------------------------------')

### 課題2：任意の商品の最安値と最高値を取得
def study_2():
    product_dictionary = {}
    keyword = input("価格を取得したい製品に関連するキーワードを入力してください。：")
    # 製品名、購入可能な最安価格、購入可能な最高価格を取得
    url = "https://app.rakuten.co.jp/services/api/Product/Search/20170426?format=json&formatVersion=2&keyword={}&applicationId=1019079537947262807&elements=productName,salesMinPrice,salesMaxPrice".format(keyword)
    products_json = get_api(url)
    # 一覧を表示、辞書に格納
    print("■ 製品名一覧")
    for product in products_json["Products"] :
        print(product["productName"])
        product_dictionary[product["productName"]] = {"minPrice": product["salesMinPrice"], "maxPrice": product["salesMaxPrice"]}
    print('---------------------------------------------------------------------------------------------------------------------------------')
    target = input("対象の製品名を入力してください。：")
    # 指定された商品の最低価格、最高価格を表示
    try :
        print("■ "+ target)
        print("最低価格：" + str(product_dictionary[target]["minPrice"]))
        print("最高価格：" + str(product_dictionary[target]["maxPrice"]))
    except :
        # 存在しない商品の場合エラー出力して処理を終了
        print("ERROR：対象の製品が存在しません")

### 課題3：任意のジャンルのランキングを取得し、CSV出力
def study_3():
    # ジャンルID情報を取得、表示
    url = "https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?formatVersion=2&genreId=0&applicationId=1019079537947262807"
    genre_id_list = get_api(url)
    print("ジャンルID ： ジャンル名")
    for genre_id_info in genre_id_list["children"] :
        print("{0}     ： {1}".format(genre_id_info["genreId"],genre_id_info["genreName"]))
    # 指定したジャンルIDのランキングを取得
    genre_id = input("ジャンルIDを入力してください。：")
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?format=json&formatVersion=2&genreId={}&applicationId=1019079537947262807".format(genre_id)
    ranking_json = get_api(url)

    # データフレーム作成用カラム情報
    column_list = ["順位","キャリア","商品名","キャッチコピー","商品コード","商品価格","商品説明文"
    ,"商品URL","アフィリエイトURL","商品画像有無フラグ","商品画像64x64URL(1)","商品画像64x64URL(2)"
    ,"商品画像64x64URL(3)","商品画像128x128URL(1)","商品画像128x128URL(2)","商品画像128x128URL(3)"
    ,"販売可能フラグ","消費税フラグ","送料フラグ","クレジットカード利用可能フラグ","ショップオブザイヤーフラグ"
    ,"海外配送フラグ","海外配送対象地域","あす楽フラグ","あす楽〆時間","あす楽配送対象地域","アフィリエイト利用利率"
    ,"販売開始時刻","販売終了時刻","レビュー件数","レビュー平均","商品別ポイント倍付け","商品別ポイント倍付け開始日時"
    ,"商品別ポイント倍付け終了日時","店舗名","店舗コード","店舗URL","ジャンル情報"]
    # JSONファイルのキーリスト
    json_key_list = ["rank","carrier","itemName","catchcopy","itemCode","itemPrice","itemCaption"
    ,"itemUrl","affiliateUrl","imageFlag","smallImageUrls","mediumImageUrls","availability","taxFlag"
    ,"postageFlag","creditCardFlag","shopOfTheYearFlag","shipOverseasFlag","shipOverseasArea","asurakuFlag"
    ,"asurakuClosingTime","asurakuArea","affiliateRate","startTime","endTime","reviewCount","reviewAverage"
    ,"pointRate","pointRateStartTime","pointRateEndTime","shopName","shopCode","shopUrl","genreId"]
    # JSONファイルを成形
    ranking_info_list = []
    for info in ranking_json["Items"] :
        ranking_info = []
        for json_key in json_key_list :
            if json_key == "smallImageUrls" or json_key == "mediumImageUrls" :
                count = 0
                while count < 3 :
                    ranking_info.append(info[json_key][0])
                    count += 1
            else :
                ranking_info.append(info[json_key])
        ranking_info_list.append(ranking_info)
    # 取得したデータをデータフレームに格納してCSV出力
    df = pd.DataFrame(ranking_info_list, columns=column_list)
    # CSVファイルを出力
    csv_path = path.dirname(__file__) + "/RANKING_INFO.csv"
    df.to_csv(csv_path, index=False, encoding='utf_8_sig')
    print("CSVファイルを出力しました。({})".format(csv_path))

# 課題1呼び出し
#study_1()
# 課題2呼び出し
#study_2()
# 課題3呼び出し
study_3()