# Language pack for login 0.02b (2022/11/07)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'message' 	=> "IDとパスワードを入力してログインしてください。",\
		'password' 	=> "パスワード",\
		'login' 	=> "ログイン",\
		'error'		=> "IDとパスワードが一致しませんでした。<br>パスワードを忘れた方は再登録してください。",\
		'help'	=> "<img src='bootstrap-dist/icons/question-circle-gray.svg' style='height:3em; width:2em;'>",\
		'nb'		=> "栄養ブラウザ",\
		'regist'	=> "登録",\
		'empty'		=> "[空き地]"
	}

	return l[language]
end
