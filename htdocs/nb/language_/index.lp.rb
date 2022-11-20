# Language pack for index page 0.23b (2022/11/07)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'nb'		=> "栄養ブラウザ",\
		'login'		=> "ログイン",\
		'logout'	=> "ログアウト",\
		'regist'	=> "登録",\
		'san'		=> "さん",\
		'help' 		=> "<img src='bootstrap-dist/icons/question-circle-gray.svg' style='height:3em; width:2em;'>",\
		'search' 	=> "<img src='bootstrap-dist/icons/search-gray.svg' style='height:1.5em; width:2em;'>",\
		'food'		=> "食品",\
		'recipe'	=> "レシピ",\
		'memory'	=> "記憶",\
		'login_' 	=> "ログインが必要",\
		'gmen' 		=> "ギルドメンバー専用",\
		'cboard' 	=> "<img src='bootstrap-dist/icons/card-text.svg' style='height:1.2em; width:1.2em;'>&nbsp;まな板",\
		'table' 	=> "<img src='bootstrap-dist/icons/motherboard.svg' style='height:1.2em; width:1.2em;'>&nbsp;お膳",\
		'history'	=> "<img src='bootstrap-dist/icons/inbox-fill.svg' style='height:1.2em; width:1.2em;'>&nbsp;履　歴",\
		'recipel' 	=> "<img src='bootstrap-dist/icons/journal-text.svg' style='height:1.2em; width:1.2em;'>&nbsp;レシピ帳",\
		'menul' 	=> "<img src='bootstrap-dist/icons/journals.svg' style='height:1.2em; width:1.2em;'>&nbsp;献立帳",\
		'book' 		=> "<img src='bootstrap-dist/icons/book.svg' style='height:1.2em; width:1.2em;'>",\
		'gear' 		=> "<img src='bootstrap-dist/icons/gear-fill.svg' style='height:1.2em; width:1.2em;'>",\
		'koyomi' 	=> "こよみ",\
		'ginmi' 	=> "アセスメント",\
		'pysique' 	=> "体格管理",\
		'momchai' 	=> "母子管理",\
		'note' 		=> "管理ノート",\
		'foodrank' 	=> "食品栄養ランク",\
		'fczl' 		=> "FCZエディタ",\
		'accountm' 	=> "娘アカウント管理",\
		'visionnerz'=> "VISIONNERZ",\
		'recipe3d' 	=> "3Dレシピ検索",\
		'school' 	=> "お料理教室",\
		'toker'		=> "統計(R)",\
		'unit' 		=> "単位登録",\
		'color' 	=> "色登録",\
		'allergen' 	=> "アレルゲン登録",\
		'dic' 		=> "辞書登録",\
		'slog' 		=> "別リク",\
		'user' 		=> "ユーザー管理",\
		'gycv' 		=> "緑黄色野菜登録",\
		'shun' 		=> "旬登録",\
		'memorya' 	=> "記憶管理",\
		'senior' 	=> "終焉管理",\
		'condition' => "状態管理",\
	}

	return l[language]
end











