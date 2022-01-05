#! /usr/bin/ruby
#nb2020-clean.rb for modified20211228

#Bacura KYOTO Lab
#Saga Ukyo-ku Kyoto, JAPAN
#https://bacura.jp
#yossy@bacura.jp


#==============================================================================
# MAIN
#==============================================================================

source_file = '20201225-mxt_kagsei-mext_01110_012-m20211228.txt'
out_file = '20201225-mxt_kagsei-mext_01110_012-m20211228_clean.txt'

data_solid = []

# 食品成分表データの読み込みと加工
f = open( source_file, 'r' )
f.each_line do |e|
	items = e.force_encoding( 'UTF-8' ).split( "\t" )

	#### 共通
	t = e.force_encoding( 'UTF-8' )

	#### 穀類
	if items[0] == '01'
		t.sub!( 'こむぎ', '＜こむぎ＞' )
		t.sub!( 'こめ', '＜こめ＞' )
		t.sub!( '［水稲穀粒］', '［水稲穀粒+］' )
		t.sub!( '［水稲めし］', '［水稲めし+］' )
		t.sub!( '［水稲全かゆ］', '［水稲全かゆ+］' )
		t.sub!( '［水稲五分かゆ］', '［水稲五分かゆ+］' )
		t.sub!( '［水稲おもゆ］', '［水稲おもゆ+］' )
		t.sub!( '［陸稲穀粒］', '［陸稲穀粒+］' )
		t.sub!( '［陸稲めし］', '［陸稲めし+］' )
		t.sub!( '［水稲穀粒］', '［水稲穀粒+］' )
		t.sub!( '［その他］　', '')

		t.sub!( '［玄穀］　国産　普通', '小麦玄穀　国産　普通') if items[1] == '01012'
		t.sub!( '［玄穀］　輸入　軟質', '小麦玄穀　輸入　軟質') if items[1] == '01013'
		t.sub!( '［玄穀］　輸入　硬質', '小麦玄穀　輸入　硬質') if items[1] == '01014'

		01057
	end

	#### いも・でん粉類
	if items[0] == '02'
		t.sub!( '＜でん粉・でん粉製品＞　', '' )
	end

	#### 砂糖・甘味類
	if items[0] == '03'
		t.sub!( '（砂糖類）', '［砂糖類］' )
		t.sub!( '車糖', '（車糖）' )
		t.sub!( 'ざらめ糖', '（ざらめ糖）' )
		t.sub!( '加工糖', '（加工糖）' )
	end

	#### 豆類
	if items[0] == '04'
		t.sub!( 'だいず', '＜だいず＞' )
		t.sub!( '全粒　', '' ) if /全粒・全粒製品/ =~ e
		t.sub!( '水煮缶詰', '大豆の水煮　缶詰' )
		t.sub!( '（揚げ豆）', '　揚げ豆') if items[1] == '04014'

	end

	#### 野菜類
	if items[0] == '06'
		t.sub!( '加工品　', '' ) if /トマト/ =~ e
		t.sub!( 'ホール', 'ホールトマトの缶詰' ) if /トマト/ =~ e
	end

	#### 果実類
	if items[0] == '06'
		t.sub!( '（ネクター）', 'ネクター')
	end

	#### 魚介類
	if items[0] == '10'
		t.sub!( '＜えび・かに類＞　', '' )
		t.sub!( '（えび類）', '＜えび類＞' )
		t.sub!( '（かに類）　', '＜かに類＞' )
		t.sub!( '＜いか・たこ類＞　', '')
		t.sub!( '（いか類）', '＜いか類＞' )
		t.sub!( '（たこ類）　', '＜たこ類＞' )
		t.sub!( '（あじ類）', '［あじ類］' )
		t.sub!( '（いわし類）', '［いわし類］' )
		t.sub!( '（かじき類）', '［かじき類］' )
		t.sub!( '（かつお類）', '［かつお類］' )
		t.sub!( '（かれい類）', '［かれい類］' )
		t.sub!( '（こち類）', '［こち類］' )
		t.sub!( '（さけ・ます類）', '［さけ・ます類］' )
		t.sub!( '（さば類）', '［さば類］' )
		t.sub!( '（さめ類）', '［さめ類］' )
		t.sub!( '（ししゃも類）', '［ししゃも類］' )
		t.sub!( '（たい類）', '［たい類］' )
		t.sub!( '（たら類）', '［たら類］' )
		t.sub!( '（ふぐ類）', '［ふぐ類］' )
		t.sub!( '（まぐろ類）', '［まぐろ類］' )
		t.sub!( '缶詰', 'いわしの缶詰' ) if /いわし/ =~ e
		t.sub!( '缶詰', 'かつおの缶詰' ) if /かつお/ =~ e
		t.sub!( '加工品', '（加工品）' ) if /かつお/ =~ e
		t.sub!( '缶詰', 'さばの缶詰' ) if /さば/ =~ e
		t.sub!( '加工品　', '' ) if /さば/ =~ e
		t.sub!( '缶詰', 'たらの缶詰' ) if /たら/ =~ e
		t.sub!( '加工品　', '' ) if /たら/ =~ e
		t.sub!( '缶詰', 'まぐろの缶詰' ) if /まぐろ/ =~ e
		t.sub!( '加工品　', '' ) if /えび/ =~ e
		t.sub!( '加工品', '') if /かに/ =~ e
		t.sub!( '加工品', '［加工品］' ) if /いか/ =~ e
		t.sub!( 'つくだ煮', 'えびのつくだ煮' ) if items[1] == '10331'
		t.sub!( 'くん製', 'いかのくん製' ) if items[1] == '10355'
		t.sub!( '塩辛', 'いかの塩辛' ) if items[1] == '10358'
		t.sub!( '味付け缶詰', 'イカの味付け缶詰' ) if items[1] == '10359'
	end

	#### 肉類
	if items[0] == '11'
		t.sub!( '［ハム類〕', '［ハム類］' )
		t.sub!( '［ソーセージ類〕', '［ソーセージ類］' )

		t.sub!( '［', '*')
		t.sub!( '］', '@')
		t.sub!( '（', '［')
		t.sub!( '）', '］')
		t.sub!( '*', '（')
		t.sub!( '@', '）')

		t.sub!( '　うし　', '　［うし］　' )
		t.sub!( '（和牛肉）', '（和牛肉+）')
		t.sub!( '（乳用肥育牛肉）', '（乳用肥育牛肉+）' )
		t.sub!( '（交雑牛肉）', '（交雑牛肉+）' )
		t.sub!( '（輸入牛肉）', '（輸入牛肉+）' )
		t.sub!( '（子牛肉）', '（子牛肉+）' )
		t.sub!( '（ひき肉）　生', '牛ひき肉　生' ) if /うし/ =~ e
		t.sub!( '（ひき肉）　焼き', '牛ひき肉　焼き' ) if /うし/ =~ e
		t.sub!( '（副生物）　', '牛ホルモン　' ) if /うし/ =~ e
		t.sub!( '（加工品）　', '') if /うし/ =~ e
		t.sub!( '味付け缶詰', '牛味付け缶詰' ) if items[1] == '11106'
		t.sub!( 'スモークタン', '牛スモークタン' ) if items[1] == '11108'

		t.sub!( '　ぶた　', '　［ぶた］　' )
		t.sub!( '（大型種肉）', '（豚大型種肉+）')
		t.sub!( '（中型種肉）', '（豚中型種肉+）')
		t.sub!( '（ひき肉）　生', '豚ひき肉　生' ) if /ぶた/ =~ e
		t.sub!( '（ひき肉）　焼き', '豚ひき肉　焼き' ) if /ぶた/ =~ e
		t.sub!( '（副生物）　', '豚ホルモン　' ) if /ぶた/ =~ e
		t.sub!( '（その他）　', '' ) if /ぶた/ =~ e
		t.sub!( 'スモークレバー', '豚スモークレバー' ) if items[1] == '11197'

		t.sub!( '（マトン）', '（マトン+）')
		t.sub!( '（ラム）', '（ラム+）')
		t.sub!( '　めんよう　', '　［めんよう］　' )
		t.sub!( '混合プレスハム', '羊混合プレスハム') if items[1] == '11179'

		t.sub!( '鶏卵', '［鶏卵+］' )
		t.sub!( '　にわとり　', '　［にわとり］　' )
		t.sub!( '（親・主品目）', '（成鶏+）' )
		t.sub!( '（親・副品目）', '（成鶏+）' )
		t.sub!( '（若どり・主品目）', '（若鶏+）' )
		t.sub!( '（若どり・副品目）', '（若鶏+）' )
		t.sub!( '（二次品目）　ひき肉　生', '鶏ひき肉　生' ) if /にわとり/ =~ e
		t.sub!( '（二次品目）　ひき肉　焼き', '鶏ひき肉　焼き' ) if /にわとり/ =~ e
		t.sub!( '（その他）　', '' ) if /にわとり/ =~ e
		t.sub!( '皮', 'にわとりの皮' ) if /にわとり/ =~ e
		t.sub!( '心臓', 'にわとりの心臓') if items[1] == '11231'
		t.sub!( '肝臓', 'にわとりの肝臓') if items[1] == '11232'
		t.sub!( 'なんこつ［胸肉］', 'にわとりのなんこつ 胸肉') if items[1] == '11236'
	end

	#### 乳類
	if items[0] == '13'
		t.sub!( '＜牛乳及び乳製品＞　', '' )
		t.sub!( '＜その他＞　', '' )
		t.sub!( '（その他）　', '' )
	end

	#### 油脂類
	if items[0] == '14'
		t.sub!( '（その他）　', '' )
	end

	#### 菓子類
	if items[0] == '15'
		t.sub!( '＜牛乳及び乳製品＞　', '' )
		t.sub!( '＜その他＞　', '' )
	end

	#### 嗜好飲料類
	if items[0] == '16'
		t.sub!( '＜その他＞　（炭酸飲料類）', '＜炭酸飲料類＞' )
		t.sub!( '＜その他＞　', '' )
	end

	#### 調味料・香辛料類
	if items[0] == '17'
		t.sub!( '＜その他＞　', '' )
		t.sub!( '＜調味料類＞　（その他）　', '＜調味料類＞　' )
		t.sub!( '（ウスターソース類）', '［ウスターソース類］' )
		t.sub!( '（辛味調味料類）', '［辛味調味料類］' )
		t.sub!( '（しょうゆ類）', '［しょうゆ類］' )
		t.sub!( '（食塩類）', '［食塩類］' )
		t.sub!( '（食酢類）', '［食酢類］' )
		t.sub!( '（だし類）', '［だし類］' )
		t.sub!( '（調味ソース類）', '［調味ソース類］' )
		t.sub!( '（トマト加工品類）', '［トマト加工品類］' )
		t.sub!( '（ドレッシング類）', '［ドレッシング類］' )
		t.sub!( '（みそ類）', '［みそ類］' )
		t.sub!( '（ルウ類）', '［ルウ類］' )
		t.sub!( '半固形状ドレッシング', '（半固形状ドレッシング）' )
		t.sub!( '分離液状ドレッシング', '（分離液状ドレッシング）' )
		t.sub!( '乳化液状ドレッシング', '（乳化液状ドレッシング）' )
		t.sub!( 'すし酢', '（酢）　すし酢' ) if /すし酢/ =~ e
		t.sub!( '甘酢', '（酢）　甘酢' ) if items[1] == '17094'
		t.sub!( '黄身酢', '（酢）　黄身酢' ) if items[1] == '17096'
		t.sub!( 'ごま酢', '（酢）　ごま酢' ) if items[1] == '17097'
		t.sub!( '三杯酢', '（酢）　三杯酢' ) if items[1] == '17099'
		t.sub!( '二杯酢', '（酢）　二杯酢' ) if items[1] == '17100'
		t.sub!( '中華風合わせ酢', '（酢）　中華風合わせ酢' ) if items[1] == '17104'
		t.sub!( 'オイスターソース', '（ソース）　オイスターソース' ) if items[1] == '17031'
		t.sub!( 'デミグラスソース', '（ソース）　デミグラスソース' ) if items[1] == '17005'
		t.sub!( 'ホワイトソース', '（ソース）　ホワイトソース' ) if items[1] == '17109'
		t.sub!( 'ミートソース', '（ソース）　ミートソース' ) if items[1] == '17033'
		t.sub!( '焼きそば粉末ソース', '（ソース）　焼きそば粉末ソース' ) if items[1] == '17144'
		t.sub!( 'ごまだれ', '（たれ）　ごまだれ' ) if items[1] == '17098'
		t.sub!( '冷やし中華のたれ', '（たれ）　冷やし中華のたれ' ) if items[1] == '17108'
		t.sub!( '焼き鳥のたれ', '（たれ）　焼き鳥のたれ' ) if items[1] == '17112'
		t.sub!( '焼き肉のたれ', '（たれ）　焼き肉のたれ' ) if items[1] == '17113'
		t.sub!( 'みたらしのたれ', '（たれ）　みたらしのたれ' ) if items[1] == '17114'
	end

	#### 調理加工食品類
	if items[0] == '18'
		t.sub!( '和風料理', '＜和風料理＞' )
		t.sub!( '和え物類', '［和え物類］' )
		t.sub!( '汁物類', '［汁物類］' )
		t.sub!( '酢の物類', '［酢の物類］' )
		t.sub!( '煮物類', '［煮物類］' )
		t.sub!( 'その他', '［その他］' )

		t.sub!( '洋風料理', '＜洋風料理＞' )
		t.sub!( 'カレー類', '［カレー類］' )
		t.sub!( 'コロッケ類', '［コロッケ類］' )
		t.sub!( 'シチュー類', '［シチュー類］' )
		t.sub!( '素揚げ類', '［素揚げ類］' )
		t.sub!( 'スープ類', '［スープ類］' )
		t.sub!( 'フライ用冷凍食品', 'フライ類' )
		t.sub!( 'ハンバーグステーキ類', '［ハンバーグ類］' )
		t.sub!( 'フライ類', '［フライ類］' )

		t.sub!( '中国料理', '＜中国料理＞' )
		t.sub!( '点心類', '［点心類］' )
		t.sub!( '菜類', '［菜類］' )

		t.sub!( '韓国料理', '＜韓国料理＞' )
	end

	data_solid << t
end
f.close


####
header = data_solid.shift
data_solid_ = []
c = 0
data_solid.each do |e|
	t = e.sub( /\t+\n/, "\n" )
	t.gsub!( '"', '' )
	a = t.split( "\t" )
	if /^\d\d/ =~ e && a.size >= 10
		data_solid_[c] = t
	else
		c -= 1
		data_solid_[c].chomp!
		data_solid_[c] << "<br>#{t}"
	end
	c += 1
end
data_solid_.unshift( header )

# 成分表データの書き込み
f = open( out_file, 'w' )
data_solid_.each do |e| f.puts e end
f.close
