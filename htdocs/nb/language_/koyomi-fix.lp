# Language pack for koyomi-fix

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'save' 		=> "保存",\
		'g100' 		=> "100 g相当",\
		'food_n' 	=> "食品名",\
		'food_g'	=> "食品群",\
		'weight'	=> "重量(g)",\
		'palette'	=> "パレット",\
		'signpost'	=> "<img src='bootstrap-dist/icons/signpost.svg' style='height:2em; width:2em;'>",\
		'clock'		=> "<img src='bootstrap-dist/icons/clock.svg' style='height:1.5em; width:1.5em;'>",\
		'min'		=> "分間",\
		'week'		=> "-- １週間以内 --",\
		'month'		=> "-- １ヶ月以内 --",\
		'volume'	=> "個数",\
		'history'	=> "履歴"
	}

	return l[language]
end
