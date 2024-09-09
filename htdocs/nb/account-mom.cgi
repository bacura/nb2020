#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser account mother 0.1.1 (2024/05/10)


#==============================================================================
#STATIC
#==============================================================================
#script = File.basename( $0, '.cgi' )
@debug = false

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'title'	=> "娘アカウントエディタ",\
		'pass'	=> "パス",\
		'mail'	=> "メール",\
		'alias'	=> "二つ名",\
		'id'	=> "ID",\
		'language'	=> "言語",\
		'save'	=> "保存",\
		'update'	=> "更新",\
		'user'	=> "ユーザー",\
		'last'	=> "最終ログイン日",\
		'reg_date'	=> "登録日",\
		'edit'	=> "編集",\
		'new_reg'	=> "新規登録",\
		'delete'	=> "削除",\
		'err_mes1'	=> "入力されたIDは英数字とハイフン、アンダーバー以外の文字が使用されています。別のIDを入力して登録してください。",\
		'err_mes2'	=> "入力されたIDは制限の30文字を越えています。別のIDを入力して登録してください。",\
		'err_mes3'	=> "入力されたIDはすでに使用されています。別のIDを入力して登録してください。",\
		'reload'	=> "※更新の反映にはリロードが必要です。",\
		'pencil'	=> "<img src='bootstrap-dist/icons/pencil.svg' style='height:3em; width:3em;'>",\
		'trash'		=> "<img src='bootstrap-dist/icons/trash.svg' style='height:1.5em; width:1.2em;'>",\
		'camera'	=> "<img src='bootstrap-dist/icons/camera.svg' style='height:1.2em; width:1.2em;'>"
	}

	return l[language]
end

def new_account( db, user )
	db.query( "INSERT INTO #{$MYSQL_TB_USER} SET pass='#{user.pass}', mail='#{user.mail}', aliasu='#{user.aliasu}', status='6', language='#{user.language}', user='#{user.name}', mom='#{user.mom}', switch='1', reg_date='#{user.reg_date}';", true )

	# Inserting standard palettes
	0.upto( 3 ) do |c|
    	db.query( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{user.name}', name='#{@palette_default_name[c]}', palette='#{@palette_default[c]}';", true )
	end

	# Inserting new history
	db.query( "INSERT INTO #{$MYSQL_TB_HIS} SET user='#{user.name}', his='';", true )

	# Inserting new SUM
	db.query( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{user.name}', sum='';", true )

	# Inserting new meal
	db.query( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{user.name}', meal='';", true )

	# Inserting new config
	db.query( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{user.name}', icache=1;", true )

end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
db = Db.new( user, @debug, false )

#### Guild member check
if user.status < 5 || user.status == 6 || user.status == 7
	puts "Guild member shun error."
	exit
end


#### Getting POST
command = @cgi['command']
uid_d = @cgi['uid_d']
pass_d = @cgi['pass_d']
mail_d = @cgi['mail_d']
aliasu_d = @cgi['aliasu_d']
language_d = @cgi['language_d']
switch_d = @cgi['switch_d'].to_i
if @debug
	puts "command:#{command}<br>\n"
	puts "uid_d:#{uid_d}<br>\n"
	puts "pass_d:#{pass_d}<br>\n"
	puts "mail_d:#{mail_d}<br>\n"
	puts "aliasu_d:#{aliasu_d}<br>\n"
	puts "language_d:#{language_d}<br>\n"
	puts "<hr>\n"
end


if command == 'update'
	db.query( "UPDATE #{$MYSQL_TB_USER} SET pass='#{pass_d}', mail='#{mail_d}', aliasu='#{aliasu_d}', language='#{language_d}' WHERE user='#{uid_d}';", true )

elsif command == 'switch'
	db.query( "UPDATE #{$MYSQL_TB_USER} SET switch='#{switch_d}' WHERE user='#{uid_d}';", true )

elsif command == 'save'
	message = ''
	# Checking improper characters
	if /[^0-9a-zA-Z\-\_]/ =~ uid_d
    	message = "<p class='msg_small_red'>#{l['err_msg1']}</p>"

	# Checking character limit
	elsif uid_d.size > 30
		message = "<p class='msg_small_red'>#{l['err_msg2']}</p>"

	# OK
	else
		# Checking same ID
		r = db.query( "SELECT user FROM #{$MYSQL_TB_USER} WHERE user='#{uid_d}';", false )
		message = "<p class='msg_small_red'>#{l['err_msg3']}</p>" if r.first
	end

	if message == ''
		new_user = User.new( @cgi )
		new_user.name = uid_d
		new_user.pass = pass_d
		new_user.mail = mail_d
		new_user.aliasu = aliasu_d
		new_user.language = language_d
		new_user.mom = user.name
		new_user.reg_date = @datetime

		new_account( db, new_user )

	else
		puts message
	end
end


if command == 'delete'
	db.query( "UPDATE #{$MYSQL_TB_USER} SET status='0' WHERE user='#{uid_d}' AND mom='#{user.name}';", true )
	uid_d = ''
end


account_html = ''
case command
when 'new', 'edit'
	if command == 'edit'
		r = db.query( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{uid_d}';", false )
		if r.first
			pass_d = r.first['pass']
			mail_d = r.first['mail']
			aliasu_d = r.first['aliasu']
			language_d = r.first['language']
		end
	end

	account_html << "<hr>"

	if command == 'new'
		account_html << "<div class='row'>"
		account_html << "<div class='col-4'>#{l['id']}</div>"
		account_html << "<div class='col-8'><input type='text' class='form-control login_input' id='uid_d' value='' required></div>"
		account_html << "</div>"
	end

	account_html << "<div class='row'>"
	account_html << "<div class='col-4'>#{l['pass']}</div>"
	account_html << "<div class='col-8'><input type='text' class='form-control login_input' id='pass_d' value='#{pass_d}' required></div>"
	account_html << "</div>"
	account_html << "<div class='row'>"
	account_html << "<div class='col-4'>#{l['mail']}</div>"
	account_html << "<div class='col-8'><input type='text' class='form-control login_input' id='mail_d' value='#{mail_d}'></div>"
	account_html << "</div>"
	account_html << "<div class='row'>"
	account_html << "<div class='col-4'>#{l['alias']}</div>"
	account_html << "<div class='col-8'><input type='text' class='form-control login_input' id='aliasu_d' value='#{aliasu_d}'></div>"
	account_html << "</div>"
	account_html << "<div class='row'>"
	account_html << "<div class='col-4'>#{l['language']}</div>"
	account_html << "<div class='col-4'>"
	account_html << "<select class='form-select' id='language_d'>"
	account_html << "<option value='jp' SELECTED>jp</option>"
	account_html << "</select>"
	account_html << "</div>"
	account_html << "</div><br>"
	account_html << "<div class='row'>"

	if command == 'new'
		account_html << "<div class='col-5' align='center'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"saveAccountM()\">#{l['save']}</button></div>"
	else
		account_html << "<div class='col-5' align='center'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"updateAccountM( '#{uid_d}' )\">#{l['update']}</button></div>"
	end
	account_html << "</div>"
else
	account_html << "<div class='row'>"
	account_html << "<table class='table table-sm table-striped'>"
	account_html << "<thead><tr>"
	account_html << "<th>#{l['user']}</th>"
	account_html << "<th>#{l['pass']}</th>"
	account_html << "<th>#{l['mail']}</th>"
	account_html << "<th>#{l['alias']}</th>"
	account_html << "<th>#{l['last']}</th>"
	account_html << "<th>#{l['login_date']}</th>"
	account_html << "<th>#{l['reg_date']}</th>"
	account_html << "<th>#{l['language']}</th>"
	account_html << "<th></th>"
	account_html << "<th></th>"
	account_html << "<tr></thead>"


	r = db.query( "SELECT * FROM #{$MYSQL_TB_USER} WHERE status='6' AND mom='#{user.name}';", false )
	r.each do |e|
		account_html << "<tr>"
		account_html << "<td><div class='custom-control custom-switch'><input type='checkbox' class='custom-control-input' id='sw_#{e['user']}' onchange=\"switchAccountM( 'sw_#{e['user']}', '#{e['user']}' )\" #{$CHECK[e['switch']]}><label class='custom-control-label' for='sw_#{e['user']}'></label></div></td>"
		account_html << "<td>#{e['user']}</td>"
		account_html << "<td>#{e['pass']}</td>"
		account_html << "<td>#{e['mail']}</td>"
		account_html << "<td>#{e['aliasu']}</td>"
		account_html << "<td>#{e['login_date']}</td>"
		account_html << "<td>#{e['reg_date']}</td>"
		account_html << "<td>#{e['language']}</td>"
		account_html << "<td><button type='button' class='btn btn-success btn-sm nav_button' onclick='editAccountM( \"#{e['user']}\" )'>#{l['edit']}</button></td>"
		account_html << "<td>&nbsp;<input type='checkbox' id='delete_checkM'>&nbsp;<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick='deleteAccountM( \"#{e['user']}\" )'>#{l['delete']}</button></td>"
		account_html << "</tr>"
	end
	account_html << "</table>"
end


button_new_reg = ''
button_new_reg = "<button type='button' class='btn btn-success btn-sm nav_button' onclick='newAccountM()'>#{l['new_reg']}</button>" if command != 'edit'


html = <<-"HTML"
<div class='container'>
	<div class='row'>
		<div class='col-10'>
			<div class='col'><h5>#{l['title']}: #{uid_d}</h5></div>
		</div>
		<div class='col-2'>
			#{button_new_reg}
		</div>
	<div>
	#{account_html}
	#{l['reload']}
</div>
HTML

puts html
