# Language pack for koyomi 0.13b (2022/12/05)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'koyomi' 	=> "こよみ:食事",\
		'sun' 		=> "日",\
		'mon' 		=> "月",\
		'tue' 		=> "火",\
		'wed' 		=> "水",\
		'thu' 		=> "木",\
		'fri' 		=> "金",\
		'sat' 		=> "土",\
		'year' 		=> "年",\
		'breakfast' => "朝食",\
		'lunch' 	=> "昼食",\
		'dinner' 	=> "夕食",\
		'supply'	=> "間食 / 補食",\
		'memo' 		=> "メモ",\
		'foodrec' 	=> "食事記録",\
		'exrec'		=> "拡張記録",\
		'calc' 		=> "栄養計算",\
		'compo' 	=> "食品構成",\
		'g100' 		=> "100 g相当",\
		'food_n' 	=> "食品名",\
		'food_g'	=> "食品群",\
		'weight'	=> "重量(g)",\
		'palette'	=> "パレット",\
		'snow'		=> "<img src='bootstrap-dist/icons/snow2.svg' style='height:1.2em; width:1.2em;'>",\
		'visionnerz'=> "<img src='bootstrap-dist/icons/graph-up.svg' style='height:2em; width:1.0em;'>",\
		'return'	=> "<img src='bootstrap-dist/icons/geo.svg' style='height:2em; width:2em;'>"
	}

	return l[language]
end
