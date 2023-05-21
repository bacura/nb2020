# Nutorition browser 2020 Config module for acount 0.02b (2022/12/24)
#encoding: utf-8

def config_module( cgi, user, lp )
	module_js()
	l = language_pack( user.language )

	step = cgi['step']

	res = mdb( "SELECT pass, mail, aliasu FROM #{$MYSQL_TB_USER} WHERE user='#{user.name}' AND cookie='#{user.uid}';", false, false )
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
			mdb( "UPDATE #{$MYSQL_TB_USER} SET pass='#{pass}', mail='#{mail}', aliasu='#{aliasu}', language='#{language}' WHERE user='#{user.name}' AND cookie='#{user.uid}';", false, false )
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
	var new_mail = '';
	var new_aliasu = '';
	var old_password = '';
	var new_password1 = '';
	var new_password2 = '';
	var language = '';

	if( step == 'change' ){
		var new_mail = document.getElementById( "new_mail" ).value;
		var new_aliasu = document.getElementById( "new_aliasu" ).value;
		var old_password = document.getElementById( "old_password" ).value;
		var new_password1 = document.getElementById( "new_password1" ).value;
		var new_password2 = document.getElementById( "new_password2" ).value;
		var language = document.getElementById( "language" ).value;
	}

	$.post( "config.cgi", { mod:'account', step:step, new_mail:new_mail, new_aliasu:new_aliasu, old_password:old_password, new_password1:new_password1, new_password2:new_password2, language:language }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
	displayLINE( 'on' );
};

</script>
JS
	puts js
end


# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
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
