# Language pack for GM allergen editor 0.00b (2022/11/19)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'search' 	=> "レシピ検索",\
		'fract' 	=> "端数",\
		'round'		=> "四捨五入",\
		'ceil' 		=> "切り上げ",\
		'floor'		=> "切り捨て",\
		'weight' 	=> "重量",\
		'fn' 		=> "食品番号",\
		'name' 		=> "食品名",\
		'change'	=> "<img src='bootstrap-dist/icons/hammer.svg' style='height:1.2em; width:1.2em;'>",\
		'cboard' 	=> "<img src='bootstrap-dist/icons/card-text.svg' style='height:1.2em; width:1.2em;'>",\
		'calendar'	=> "<img src='bootstrap-dist/icons/calendar-plus.svg' style='height:1.2em; width:1.2em;'>",\
		'unit' 		=> "単",\
		'color' 	=> "色",\
		'shun' 		=> "旬",\
		'dic' 		=> "辞",\
		'allergen' 	=> "ア",\
		'plus' 		=> "<img src='bootstrap-dist/icons/plus-square-fill.svg' style='height:2em; width:2em;'>",\
		'signpost'	=> "<img src='bootstrap-dist/icons/signpost.svg' style='height:2em; width:2em;'>"
	}

	return l[language]
end
