#! /usr/bin/ruby
#encoding: utf-8
#Nutritoin browser note 0.0b


#==============================================================================
# LIBRARY
#==============================================================================
require './probe'


#==============================================================================
# STATIC
#==============================================================================
@debug = true
script = 'note'


#==============================================================================
# DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


#### Getting POST
command = @cgi['command']
if @debug
	puts "command: #{command}<br>"
	puts "<hr>"
end


case command
when 'write'
	note = @cgi['note']
	note_code = generate_code( user.name, 'n' )
	aliasm = ''
	if user.name != user.mom and user.mom != ''
		r = mdb( "SELECT aliasu from #{$MYSQL_TB_USER} WHERE user='#{user.mom}';", false, @debug )
		if r.first
			aliasm = r.first['aliasu']
			aliasm = user.mom if aliasm == '' || aliasm == nil
		end
	end
	p @datetime, note_code, aliasm,note if @debug
	mdb( "INSERT INTO #{$MYSQL_TB_NOTE} SET code='#{note_code}', user='#{user.name}', aliasm='#{aliasm}', note='#{note}', datetime='#{@datetime}';", false, @debug )
when 'photo'
	aliasm = ''
	if user.name != user.mom and user.mom != ''
		r = mdb( "SELECT aliasu from #{$MYSQL_TB_USER} WHERE user='#{user.mom}';", false, @debug )
		if r.first
			aliasm = r.first['aliasu']
			aliasm = user.mom if aliasm == '' || aliasm == nil
		end
	end
	note_code = generate_code( user.name, 'n' )
	mdb( "INSERT INTO #{$MYSQL_TB_NOTE} SET code='#{note_code}', mcode='note_tmp_new', user='#{user.name}', aliasm='#{aliasm}', note='', datetime='#{@datetime}';", false, @debug )
	exit()

when 'mcode_update'
	r = mdb( "SELECT code FROM #{$MYSQL_TB_NOTE} WHERE user='#{user.name}' AND mcode='note_tmp_new';", false, @debug )
	if r.first
		rr = mdb( "SELECT mcode FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' AND code='#{r.first['code']}';", false, @debug )
		if rr.first
			mdb( "UPDATE #{$MYSQL_TB_NOTE} SET mcode='#{rr.first['mcode']}' WHERE mcode='note_tmp_new' AND 'user='#{user.name}';", false, @debug )
		else
			mdb( "DELETE FROM #{$MYSQL_TB_NOTE} WHERE mcode='note_tmp_new' AND user='#{user.name}';", false, @debug )
		end
	end
	exit()
when 'delete'
	note_code = @cgi['code']
	p note_code if @debug
	mdb( "DELETE FROM #{$MYSQL_TB_NOTE} WHERE code='#{note_code}';", false, @debug )
else

end


daughter_delete = true

####
puts 'Extract note<br>' if @debug
note_html = ''
r = mdb( "SELECT * FROM #{$MYSQL_TB_NOTE} WHERE user='#{user.name}' ORDER BY datetime DESC;", false, @debug )
r.each do |e|
	note_date =  "#{e['datetime'].year}-#{e['datetime'].month}-#{e['datetime'].day} #{e['datetime'].hour}:#{e['datetime'].min}"

	note = e['note'].gsub( "\n", '<br>' )

	note_html << '<div class="row">'
p e['mcode']
	if e['mcode'] == nil
		if e['aliasm'] == ''
			note_html << '<div class="col-2"></div>'
			note_html << "<div class='col-9' >"
			note_html << "	<div class='alert alert-light'>#{note}<br><br>"
			note_html << "		<div align='right'>#{note_date}&nbsp;&nbsp;&nbsp;&nbsp;"
			if daughter_delete
				note_html << "			<input type='checkbox' id='#{e['code']}'>&nbsp;"
				note_html << "			<span onclick=\"deleteNote( '#{e['code']}' )\">#{lp[2]}</span>"
			end
			note_html << '</div></div></div>'
			note_html << "<div class='col-1'>#{user.aliasu}</div>"
		else
			note_html << "<div class='col-1'>#{e['aliasm']}</div>"
			note_html << "<div class='col-9' >"
			note_html << "	<div class='alert alert-success'>#{note}<br><br>"
			note_html << "		<div align='right'>#{note_date}&nbsp;&nbsp;&nbsp;&nbsp;"
			if user.mid != nil
				note_html << "	<input type='checkbox' id='#{e['code']}'>&nbsp;"
				note_html << "	<span onclick=\"deleteNote( '#{e['code']}' )\">#{lp[2]}</span>"
			end
			note_html << '</div></div></div>'
			note_html << '<div class="col-2"></div>'
		end
	else
		note_html << e['mcode']

	end
	note_html << '</div>'
end


#### HTML
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-10">
			<div class="row">
				<textarea  class="form-control" id='note' value=''></textarea><br>
			</div>
			<div class="row">
				<div class='col-4'>


					<form method='post' enctype='multipart/form-data' id='photo_form_note'>
						<div class="input-group input-group-sm">
							<label class='input-group-text'>#{lp[26]}</label>
							<input type='file' class='form-control' name='photo_note' onchange="photoNoteSave( '' )">
						</div>
					</form>
				</div>
				<div class='col-2'></div>
				<div class='col'>
					<div class="row"><button class='btn btn-sm btn-outline-primary' onclick="writeNote()">#{lp[1]}</button></div>
				</div>
			</div>
			<br>
			#{note_html}
		</div>

		<div class="col-2">

		</div>
	</div>
</div>
HTML

puts html
