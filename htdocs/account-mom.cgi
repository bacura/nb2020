#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser account mother 0.01b


#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'account-mom'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================
def new_account( user, lp )
	mdb( "INSERT #{$MYSQL_TB_USER} SET pass='#{user.pass}', mail='#{user.mail}', aliasu='#{user.aliasu}', status='6', language='#{user.language}', user='#{user.name}', mom='#{user.mom}', switch='1', reg_date='#{user.reg_date}';", false, @debug )

	# Inserting standard palettes
	0.upto( 3 ) do |c|
    	mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{user.name}', name='#{@palette_default_name[c]}', palette='#{@palette_default[c]}';", false, @debug )
	end

	# Inserting new history
	mdb( "INSERT INTO #{$MYSQL_TB_HIS} SET user='#{user.name}', his='';", false, @debug )

	# Inserting new SUM
	mdb( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{user.name}', sum='';", false, @debug )

	# Inserting new meal
	mdb( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{user.name}', meal='';", false, @debug )

	# Inserting new config
	mdb( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{user.name}', his_max=200, recipel='1:0:99:99:99:99:99', koyomiex='0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t';", false, @debug )
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


#### Guild member check
if user.status < 5 && user.status != 6
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
	mdb( "UPDATE #{$MYSQL_TB_USER} SET pass='#{pass_d}', mail='#{mail_d}', aliasu='#{aliasu_d}', language='#{language_d}' WHERE user='#{uid_d}';", false, @debug )
elsif command == 'switch'
	mdb( "UPDATE #{$MYSQL_TB_USER} SET switch='#{switch_d}' WHERE user='#{uid_d}';", false, @debug )
elsif command == 'save'
	message = ''
	# Checking improper characters
	if /[^0-9a-zA-Z\-\_]/ =~ uid_d
    	message = "<p class='msg_small_red'>#{lp[14]}</p>"

	# Checking character limit
	elsif uid_d.size > 30
		message = "<p class='msg_small_red'>#{lp[15]}</p>"

	# OK
	else
		# Checking same ID
		r = mdb( "SELECT user FROM #{$MYSQL_TB_USER} WHERE user='#{uid_d}';", false, @debug )
		message = "<p class='msg_small_red'>#{lp[16]}</p>" if r.first
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

		new_account( new_user, lp )
	else
		puts message
	end
end


if command == 'delete'
	mdb( "UPDATE #{$MYSQL_TB_USER} SET status='0' WHERE user='#{uid_d}' AND mom='#{user.name}';", false, @debug )
	uid_d = ''
end


account_html = ''
case command
when 'new', 'edit'
	if command == 'edit'
		r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{uid_d}';", false, @debug )
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
		account_html << "<div class='col-4'>#{lp[4]}</div>"
		account_html << "<div class='col-8'><input type='text' class='form-control login_input' id='uid_d' value='' required></div>"
		account_html << "</div>"
	end

	account_html << "<div class='row'>"
	account_html << "<div class='col-4'>#{lp[1]}</div>"
	account_html << "<div class='col-8'><input type='text' class='form-control login_input' id='pass_d' value='#{pass_d}' required></div>"
	account_html << "</div>"
	account_html << "<div class='row'>"
	account_html << "<div class='col-4'>#{lp[2]}</div>"
	account_html << "<div class='col-8'><input type='text' class='form-control login_input' id='mail_d' value='#{mail_d}'></div>"
	account_html << "</div>"
	account_html << "<div class='row'>"
	account_html << "<div class='col-4'>#{lp[3]}</div>"
	account_html << "<div class='col-8'><input type='text' class='form-control login_input' id='aliasu_d' value='#{aliasu_d}'></div>"
	account_html << "</div>"
	account_html << "<div class='row'>"
	account_html << "<div class='col-4'>#{lp[5]}</div>"
	account_html << "<div class='col-4'>"
	account_html << "<select class='form-select' id='language_d'>"
	account_html << "<option value='jp' SELECTED>jp</option>"
	account_html << "</select>"
	account_html << "</div>"
	account_html << "</div><br>"
	account_html << "<div class='row'>"

	if command == 'new'
		account_html << "<div class='col-5' align='center'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"saveAccountM()\">#{lp[6]}</button></div>"
	else
		account_html << "<div class='col-5' align='center'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"updateAccountM( '#{uid_d}' )\">#{lp[6]}</button></div>"
	end
	account_html << "</div>"
else
	account_html << "<div class='row'>"
	account_html << "<table class='table table-sm table-striped'>"
	account_html << "<thead><tr>"
	account_html << "<th>#{lp[22]}</th>"
	account_html << "<th>#{lp[7]}</th>"
	account_html << "<th>#{lp[1]}</th>"
	account_html << "<th>#{lp[2]}</th>"
	account_html << "<th>#{lp[3]}</th>"
	account_html << "<th>#{lp[8]}</th>"
	account_html << "<th>#{lp[9]}</th>"
	account_html << "<th>#{lp[5]}</th>"
	account_html << "<th></th>"
	account_html << "<th></th>"
	account_html << "<tr></thead>"


	r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE status='6' AND mom='#{user.name}';", false, @debug )
	r.each do |e|
		account_html << "<tr>"
		account_html << "<td><div class='custom-control custom-switch'><input type='checkbox' class='custom-control-input' id='sw_#{e['user']}' onchange=\"switchAccountM( 'sw_#{e['user']}', '#{e['user']}' )\" #{checked( e['switch'].to_i )}><label class='custom-control-label' for='sw_#{e['user']}'></label></div></td>"
		account_html << "<td>#{e['user']}</td>"
		account_html << "<td>#{e['pass']}</td>"
		account_html << "<td>#{e['mail']}</td>"
		account_html << "<td>#{e['aliasu']}</td>"
		account_html << "<td>#{e['login_date']}</td>"
		account_html << "<td>#{e['reg_date']}</td>"
		account_html << "<td>#{e['language']}</td>"
		account_html << "<td><button type='button' class='btn btn-success btn-sm nav_button' onclick='editAccountM( \"#{e['user']}\" )'>#{lp[11]}</button></td>"
		account_html << "<td>&nbsp;<input type='checkbox' id='delete_checkM'>&nbsp;<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick='deleteAccountM( \"#{e['user']}\" )'>#{lp[17]}</button></td>"
		account_html << "</tr>"
	end
	account_html << "</table>"
end

html = <<-"HTML"
<div class='container'>
	<div class='row'>
		<div class='col-10'>
			<div class='col'><h5>#{lp[12]}: #{uid_d}</h5></div>
		</div>
		<div class='col-2'>
			<button type='button' class='btn btn-success btn-sm nav_button' onclick='newAccountM()'>#{lp[13]}</button>
		</div>
	<div>
	#{account_html}
	#{lp[23]}
</div>
HTML

puts html
