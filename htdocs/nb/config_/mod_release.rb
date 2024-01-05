# Nutorition browser 2020 Config module for release 0.02b (23/07/14)
#encoding: utf-8

#mod debug
@debug = false

def config_module( cgi, db )
	module_js()
	l = module_lp( db.user.language )

	step = cgi['step']
	password = cgi['password']
	puts "#{step}<br>" if @debug
	puts "#{password}<br>" if @debug

	html =''

	if step ==  ''
		puts 'form step<br>' if @debug
		html = <<-"HTML"
      	<div class="container">
      		<div class='row'>
	    		#{l['msg']}<br>
			</div><br>
      		<div class='row'>
				<div class='col-4'><input type="password" id="password" class="form-control form-control-sm login_input" placeholder="#{l['password']}" required></div>
				<div class='col-4'><button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="release_cfg()">#{l['release']}</button></div>
			</div>
		</div>
HTML
	else
		if user.status != 3 || user.status != 9
			puts 'release step general<br>' if @debug
			html = <<-"HTML"
      		<div class="container">
      			<div class='row'>
	    			#{l['thanks']}
				</div>
			</div>
HTML

			# Updating user table
			db.query( "UPDATE #{$MYSQL_TB_USER} SET status='0' WHERE user='#{db.user.name}' AND cookie='#{db.user.uid}';", true )

			# Deleting indivisual data
			db.query( "DELETE FROM #{$MYSQL_TB_HIS} WHERE user='#{db.user.name}';", true )
			db.query( "DELETE FROM #{$MYSQL_TB_SUM} WHERE user='#{db.user.name}';", true )
			db.query( "DELETE FROM #{$MYSQL_TB_CFG} WHERE user='#{db.user.name}';", true )
			db.query( "DELETE FROM #{$MYSQL_TB_MEAL} WHERE user='#{db.user.name}';", true )
			db.query( "DELETE FROM #{$MYSQL_TB_PRICEM} WHERE user='#{db.user.name}';", true )
			db.query( "DELETE FROM #{$MYSQL_TB_PALETTE} WHERE user='#{db.user.name}';", true )
		else
			puts 'release step ROM<br>' if @debug
			html = <<-"HTML"
      		<div class="container">
      			<div class='row'>
	    			#{l['nguser']}
				</div>
			</div>
HTML
		end
	end

	return html

end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

var release_cfg = function(){
	const password = document.getElementById( "password" ).value;

	$.post( "config.cgi", { mod:'release', step:'release', password:password }, function( data ){
		$( "#L1" ).html( data );

		flashBW();
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

	l['jp'] = {
		'mod_name' => "登録解除",\
		'msg' => "ユーザー登録を解除する場合は、パスワードを入力し登録解除ボタンを押してください。",\
		'password' => "パスワード",\
		'release' => "登録解除",\
		'thanks' => "ユーザー登録を解除しました。ご利用ありがとうございました。",\
		'nguser' => "特殊アカウントは登録解除できません。"
	}

	return l[language]
end

