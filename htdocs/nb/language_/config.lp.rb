# Language pack for config 0.23b (2022/11/20)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'account' 	=> "アカウント情報",\
		'display' 	=> "表示",\
		'palette'	=> "成分パレット",\
		'history'	=> "履歴",\
		'rsum'		=> "まな板",\
		'convert'	=> "各種変換",\
		'bio'		=> "生体情報",\
		'allergen'	=> "アレルゲン",\
		'koyomi'	=> "こよみ",\
		'school'	=> "お教室",\
		'release' 	=> "登録解除"
	}

	return l[language]
end
