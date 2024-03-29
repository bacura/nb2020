# Nutorition browser 2020 Config module for acount 0.10b (2022/12/24)
#encoding: utf-8

@debug = false

def config_module( cgi, db )
	module_js()
	l = module_lp( db.user.language )

	step = cgi['step']

	res = db.query( "SELECT pass, mail, aliasu FROM #{$MYSQL_TB_USER} WHERE user='#{db.user.name}' AND cookie='#{db.user.uid}';", false )
	aliasu = res.first['aliasu']
	mail = res.first['mail']
	pass = res.first['pass']
	language = res.first['language']

	if step ==  'change'
		new_mail = cgi['new_mail']
		new_aliasu = cgi['new_aliasu']
		old_password = cgi['old_password']
		new_password1 = cgi['new_password1']
		new_password2 = cgi['new_password2']
		language = cgi['language']

		if pass == old_password || pass == ''
			mail = new_mail if new_mail != '' && new_mail != nil
			aliasu = new_aliasu if new_aliasu != '' && new_aliasu != nil
			if new_password1 == new_password2
				pass = new_password1 if new_password1 != '' && new_password1 != nil
			end

			# Updating acount information
			db.query( "UPDATE #{$MYSQL_TB_USER} SET pass='#{pass}', mail='#{mail}', aliasu='#{aliasu}', language='#{language}' WHERE user='#{db.user.name}' AND cookie='#{db.user.uid}';", true )
		else
			puts "<span class='msg_small_red'>#{l['no_save']}</span><br>"
		end
	end

  	option_language = ''
  	$LP.each do |e| option_language << "<option value='#{e}'>#{e}</option>" end

	html = <<-"HTML"
    <div class="container">
    	<div class='row'>
	    	<div class='col-2'>#{l['aliase']}</div>
			<div class='col-4'><input type="text" maxlength="60" id="new_aliasu" class="form-control login_input" value="#{aliasu}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>#{l['mail']}</div>
			<div class='col-4'><input type="email" maxlength="60" id="new_mail" class="form-control login_input" value="#{mail}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>#{l['new_pw']}</div>
			<div class='col-4'><input type="text" maxlength="30" id="new_password1" class="form-control login_input" placeholder="#{l['char30']}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>#{l['new_pw']}</div>
			<div class='col-4'><input type="text" maxlength="30" id="new_password2" class="form-control login_input" placeholder="#{l['confirm']}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>#{l['language']}</div>
	    	<div class='col-2'>
        		<select id="language" class="form-select">
        		#{option_language}
        		</select>
			</div>
		</div>
		<hr>

    	<div class='row'>
	    	<div class='col-2'>#{l['password']}</div>
			<div class='col-4'><input type="password" id="old_password" class="form-control login_input" required></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'></div>
			<div class='col-4'><button type="button" class="btn btn-warning btn-sm nav_button" onclick="account_cfg( 'change' )">#{l['save']}</button></div>
		</div>
	</div>
HTML

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// Updating account information
var account_cfg = function( step ){
	let new_mail = '';
	let new_aliasu = '';
	let old_password = '';
	let new_password1 = '';
	let new_password2 = '';
	let language = '';

	if( step == 'change' ){
		new_mail = document.getElementById( "new_mail" ).value;
		new_aliasu = document.getElementById( "new_aliasu" ).value;
		old_password = document.getElementById( "old_password" ).value;
		new_password1 = document.getElementById( "new_password1" ).value;
		new_password2 = document.getElementById( "new_password2" ).value;
		language = document.getElementById( "language" ).value;
	}

	$.post( "config.cgi", { mod:'account', step:step, new_mail:new_mail, new_aliasu:new_aliasu, old_password:old_password, new_password1:new_password1, new_password2:new_password2, language:language }, function( data ){
		$( "#L1" ).html( data );
		dl1 = true;
		dline = true;
		displayBW();

	});
};

</script>
JS
	puts js
end


# Language pack
def module_lp( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'mod_name'	=> "アカウント",\
		'aliase'	=> "二つ名",\
		'mail'		=> "メールアドレス",\
		'new_pw'	=> "新しいパスワード",\
		'char30'	=> "30文字まで",\
		'confirm'	=> "(確認)",\
		'language'	=> "言語",\
		'password'	=> "現在のパスワード",\
		'save'		=> "保存",\
		'no_save'	=> "現在のパスワードが違うので、保存されませんでした。"
	}

	return l[language]
end
