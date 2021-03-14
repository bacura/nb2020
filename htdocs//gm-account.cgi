#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 GM account editor 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-account'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


#### GM check
if user.status < 9
	puts "GM error."
	exit
end


#### Getting POST data
command = @cgi['command']
target_uid = @cgi['target_uid']
target_pass = @cgi['target_pass']
target_mail = @cgi['target_mail']
target_aliasu = @cgi['target_aliasu']
target_status = @cgi['target_status']
target_language = @cgi['target_language']
if @debug
	puts "command:#{command}<br>\n"
	puts "target_uid:#{target_uid}<br>\n"
	puts "target_pass:#{target_pass}<br>\n"
	puts "target_mail:#{target_mail}<br>\n"
	puts "target_aliasu:#{target_aliasu}<br>\n"
	puts "target_status:#{target_status}<br>\n"
	puts "target_language:#{target_language}<br>\n"
	puts "<hr>\n"
end


account_html = ''
if command == 'edit'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{target_uid}';", false, @debug )
	if r.first
		account_html << "<div class='row'>"
		account_html << "	<div class='col-1'>#{lp[1]}</div><div class='col-4'><input type='text' class='form-control' id='target_pass' value='#{r.first['pass']}'></div>"
		account_html << "</div><br>"
		account_html << "<div class='row'>"
		account_html << "	<div class='col-1'>#{lp[2]}</div><div class='col-4'><input type='text' class='form-control' id='target_mail' value='#{r.first['mail']}'></div>"
		account_html << "</div><br>"
		account_html << "<div class='row'>"
		account_html << "	<div class='col-1'>#{lp[3]}</div><div class='col-4'><input type='text' class='form-control' id='target_aliasu' value='#{r.first['aliasu']}'></div>"
		account_html << "</div><br>"
		account_html << "<div class='row'>"
		account_html << "	<div class='col-1'>#{lp[4]}</div>"
		account_html << "	<div class='col-4'>"
		account_html << "<select class='form-select' id='target_status'>"
		10.times do |c|
			if r.first['status'].to_i == c
				account_html << "<option value='#{c}' SELECTED>#{@account[c]}</option>"
			else
				account_html << "<option value='#{c}'>#{@account[c]}</option>"
			end
		end
		account_html << "</select>"
		account_html << "</div>"
		account_html << "</div><br>"
		account_html << "<div class='row'>"
		account_html << "	<div class='col-1'>#{lp[5]}</div>"
		account_html << "	<div class='col-4'>"
		account_html << "		<select class='form-select' id='target_language'>"
		$LP.size.times do |c|
			if r.first['lp'].to_i == c
				account_html << "<option value='#{c}' SELECTED>#{$LP[c]}</option>"
			else
				account_html << "<option value='#{c}'>#{$LP[c]}</option>"
			end
		end
		account_html << "		</select>"
		account_html << "	</div>"
		account_html << "</div><br>"
		account_html << "<div class='row'>"
		account_html << "	<div class='col-5' align='center'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"saveAccount( '#{target_uid}' )\">#{lp[6]}</button></div>"
		account_html << "</div>"
	end
else
	if command == 'save'
		mdb( "UPDATE #{$MYSQL_TB_USER} SET pass='#{target_pass}', mail='#{target_mail}', aliasu='#{target_aliasu}', status='#{target_status}', language='#{target_language}' WHERE user='#{target_uid}';", false, @debug )
	end

	account_html << "<div class='row'>"
	r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE status!='9' AND user!='';", false, @debug )
	if r.first
		account_html << "<table class='table table-striped table-bordered'>"
		account_html << "<thead>"
		account_html << "<th>#{lp[7]}</th>"
		account_html << "<th>#{lp[1]}</th>"
		account_html << "<th>#{lp[2]}</th>"
		account_html << "<th>#{lp[3]}</th>"
		account_html << "<th>#{lp[4]}</th>"
		account_html << "<th>#{lp[8]}</th>"
		account_html << "<th>#{lp[9]}</th>"
		account_html << "<th>#{lp[10]}</th>"
		account_html << "<th>#{lp[5]}</th>"
		account_html << "</thead>"

		r.each do |e|
			account_html << "<tr>"
			account_html << "<td>#{e['user']}</td>"
			account_html << "<td>#{e['pass']}</td>"
			account_html << "<td>#{e['mail']}</td>"
			account_html << "<td>#{e['aliasu']}</td>"
			account_html << "<td>#{@account[e['status'].to_i]}</td>"
			account_html << "<td>#{e['login_date']}</td>"
			account_html << "<td>#{e['reg_date']}</td>"
			account_html << "<td>#{e['count']}</td>"
			account_html << "<td>#{e['language']}</td>"
			account_html << "<td><button type='button' class='btn btn-success btn-sm nav_button' onclick='editAccount( \"#{e['user']}\" )'>#{lp[11]}</button></td>"
			account_html << "</tr>"
		end
		account_html << "</table>"
	else
		account_html << 'no account.'
	end
end

html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[12]}: #{target_uid}</h5></div>
	</div>
	#{account_html}
</div>
HTML

puts html
