# Language pack for recipe list 0.22b (2022/11/18)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'recipel' 	=> "レシピ帳",\
		'words' 	=> "検索語：",\
		'norecipe' 	=> "検索条件のレシピは見つかりませんでした",\
		'prevp' 	=> "前項",\
		'nextp' 	=> "次項",\
		'range' 	=> "表示範囲",\
		'all' 		=> "全て",\
		'draft' 	=> "下書き",\
		'protect' 	=> "保護",\
		'public' 	=> "公開",\
		'normal' 	=> "無印",\
		'publicou' 	=> "公開(他ユーザー)",\
		'type'	 	=> "料理スタイル",\
		'role' 		=> "献立区分",\
		'tech'	 	=> "調理区分",\
		'chomi'	 	=> "[ 調味％ ]",\
		'time' 		=> "目安時間(分)",\
		'cost'	 	=> "目安費用(円)",\
		'limit' 	=> "絞　り　込　み",\
		'reset' 	=> "条件クリア",\
		'photo' 	=> "写真",\
		'name' 		=> "レシピ名",\
		'status' 	=> "ステータス",\
		'operation' => "操作",\
		'globe' 	=> "<img src='bootstrap-dist/icons/globe.svg' style='height:1.2em; width:1.2em;'>",\
		'lock'		=> "<img src='bootstrap-dist/icons/lock-fill.svg' style='height:1.2em; width:1.2em;'>",\
		'cone' 		=> "<img src='bootstrap-dist/icons/cone-striped.svg' style='height:1.2em; width:1.2em;'>",\
		'table' 	=> "<img src='bootstrap-dist/icons/motherboard.svg' style='height:1.2em; width:1.2em;'>",\
		'calendar' 	=> "<img src='bootstrap-dist/icons/calendar-plus.svg' style='height:1.2em; width:1.2em;'>",\
		'printer' 	=> "<img src='bootstrap-dist/icons/printer.svg' style='height:1.2em; width:1.2em;'>",\
		'diagram' 	=> "<img src='bootstrap-dist/icons/diagram-2.svg' style='height:1.2em; width:1.2em;'>",\
		'dropper'	=> "<img src='bootstrap-dist/icons/eyedropper.svg' style='height:1.2em; width:1.2em;'>",\
		'trash' 	=> "<img src='bootstrap-dist/icons/trash.svg' style='height:1.2em; width:1.2em;'>",\
		'space' 	=> "　"
	}

	return l[language]
end
