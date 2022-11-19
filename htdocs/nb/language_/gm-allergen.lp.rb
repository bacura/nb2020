# Language pack for GM allergen editor 0.00b (2022/11/19)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'allergen' 	=> "アレルゲン登録",\
		'fn' 		=> "食品番号",\
		'name' 		=> "食品名",\
		'obligate'	=> "義務",\
		'recommend'	=> "推奨",\
		'others'	=> "ユーザー<br>登録数",\
		'check'		=> "○",\
		'trash' 	=> "<img src='bootstrap-dist/icons/trash.svg' style='height:1.2em; width:1.2em;'>",\
		'regist'	=> "登　録"
	}

	return l[language]
end
