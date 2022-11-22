# Language pack for cutting board 0.17b (2022/11/11)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'cboard' 	=> "まな板",\
		'dish' 		=> "食数",\
		'fn' 		=> "食品#",\
		'chomi' 	=> "調味％",\
		'guide_g' 	=> "目安g",\
		'guide_e' 	=> "目安E",\
		'guide_s' 	=> "目安塩",\
		'waste' 	=> "残食g",\
		'gram' 		=> "<img src='bootstrap-dist/icons/google.svg' style='height:1.5em; width:1.5em;'>",\
		'reset' 	=> "リセット",\
		'operation' => "操作",\
		'food_name' => "食品名",\
		'memo' 		=> "一言メモ",\
		'simple_g' 	=> "単純g",\
		'sort' 		=> "<img src='bootstrap-dist/icons/sort-down.svg' style='height:1.2em; width:1.2em;'>",\
		'expect_g' 	=> "予想g",\
		'volume' 	=> "量",\
		'unit' 		=> "単位",\
		'rrate' 	=> "摂食率",\
		'up' 		=> "<img src='bootstrap-dist/icons/chevron-up.svg' style='height:1.5em; width:1.5em;'>",\
		'down' 		=> "<img src='bootstrap-dist/icons/chevron-down.svg' style='height:1.5em; width:1.5em;'>",\
		'trash' 	=> "<img src='bootstrap-dist/icons/trash.svg' style='height:1.8em; width:1.8em;'>",\
		'recipe'	=> "レシピ",\
		'calc' 		=> "栄養",\
		'price' 	=> "原価",\
		'lucky' 	=> "Lucky☆",\
		'foodize' 	=> "食品化",\
		'detective' => "名探偵",\
		'save' 		=> "<img src='bootstrap-dist/icons/save.svg' style='height:1.8em; width:1.8em;'>",\
		'printer'	=> "<img src='bootstrap-dist/icons/printer.svg' style='height:1.8em; width:1.8em;'>"
	}

	return l[language]
end
