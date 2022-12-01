# Language pack for magic calc 0.06b (2020/12/01)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'calc' 		=> "食品成分計算表",\
		'palette'	=> "パレット",\
		'precision'	=> "精密合計",\
		'ew'		=> "予想g",\
		'fract'		=> "端数",\
		'round'		=> "四捨五入",\
		'ceil'		=> "切り上げ",\
		'floor'		=> "切り捨て",\
		'recalc'	=> "<img src='bootstrap-dist/icons/calculator.svg' style='height:2em; width:2em;'>",\
		'raw'		=> "Raw<img src='bootstrap-dist/icons/download.svg' style='height:1.5em; width:1.5em;'>",\
		'food_no'	=> "食品番号",\
		'food_name'	=> "食品名",\
		'total'		=> "合計",\
		'weight'	=> "重量"
	}

	return l[language]
end
