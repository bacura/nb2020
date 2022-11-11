# Language pack for regist 0.06b (2022/11/07)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'nb'		=> "栄養ブラウザ",\
		'login'		=> "ログイン",\
		'help'		=> "<img src='bootstrap-dist/icons/question-circle-gray.svg' style='height:2em; width:2em;'>",\
		'food'		=> "食品",\
		'recipe'	=> "レシピ",\
		'memory'	=> "記憶",\
		'search'	=> "<img src='bootstrap-dist/icons/search-gray.svg' style='height:1.5em; width:1.5em;'>",\
		'message' 	=> "IDとパスワードは必須です。英数字とアンダーバー(_)のみ使用可能です。ご登録前に利用規約を確認しておいてください。",\
		'id_rule' 	=> "ID (4~30文字)",\
		'pass_rule' => "パスワード (30文字まで)",\
		'a_rule' 	=> "二つ名 (60文字まで)",\
		'mail_rule' => "メールアドレス (60文字まで)",\
		'submit' 	=> "送信",\
		'error1' 	=> "入力されたIDは英数字とハイフン、アンダーバー以外の文字が使用されています。別のIDを入力して登録してください。",\
		'error2' 	=> "入力されたIDは制限の30文字を越えています。別のIDを入力して登録してください。",\
		'error3'	=> "IDは4文字以上の長さが必要です。別のIDを入力して登録してください。",\
		'error4'	=> "入力されたIDはすでに使用されています。別のIDを入力して登録してください。",\
		'confirm'	=> "下記の内容でよろしければ登録してください。",\
		'id'		=> "ID",\
		'aliase'	=> "二つ名",\
		'mail'		=> "メールアドレス",\
		'pass'		=> "パスワード",\
		'language'	=> "言語",\
		'regist'	=> "登録する",\
		'back'		=> "変更する",\
		'thanks'	=> "ご登録ありがとうございました。",\
		'thanks2'	=> "して引き続きご利用ください。",
	}

	return l[language]
end
