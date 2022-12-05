# Language pack for koyomi calc 0.00b (2022/11/27)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'koyomi' 	=> "こよみ栄養計算",\
		'palette'	=> "パレット",\
		'signpost'	=> "<img src='bootstrap-dist/icons/signpost.svg' style='height:2em; width:2em;'>",\
		'fromto'	=> "　～　",\
		'calc'		=> "計　算",\
		'no_day'	=> "該当日がありません",\
		'name'		=> "栄養成分",\
		'unit'		=> "単位",\
		'volume'	=> "合計",\
		'breakfast'	=> "朝食",\
		'lunch'		=> "昼食",\
		'dinner'	=> "夕食",\
		'supply'	=> "捕食・間食",\
		'period'	=> "期間総量（",\
		'days'		=> "日間）",\
		'average'	=> "１日平均"
	}

	return l[language]
end
