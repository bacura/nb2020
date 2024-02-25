#! /usr/bin/ruby
#encoding: utf-8
#Nutritoin browser note 0.1b (2024/02/16)


#==============================================================================
# STATIC
#==============================================================================
@debug = true
#script = File.basename( $0, '.cgi' )


#==============================================================================
# LIBRARY
#==============================================================================
require './soul'

#==============================================================================
# DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'pencil'	=> "<img src='bootstrap-dist/icons/pencil.svg' style='height:3em; width:3em;'>",\
		'trash'		=> "<img src='bootstrap-dist/icons/trash.svg' style='height:1.5em; width:1.2em;'>",\
		'camera'	=> "<img src='bootstrap-dist/icons/camera.svg' style='height:1.2em; width:1.2em;'>"
	}

	return l[language]
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
db = Db.new( user, @debug, false )


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
		r = db.query( "SELECT aliasu from #{$MYSQL_TB_USER} WHERE user='#{user.mom}';", false )
		if r.first
			aliasm = r.first['aliasu']
			aliasm = user.mom if aliasm == '' || aliasm == nil
		end
	end
	p @datetime, note_code, aliasm,note if @debug
	db.query( "INSERT INTO #{$MYSQL_TB_NOTE} SET code='#{note_code}', user='#{user.name}', aliasm='#{aliasm}', note='#{note}', datetime='#{@datetime}';", true )

when 'photo'
	aliasm = ''
	if user.name != user.mom and user.mom != ''
		r = db.query( "SELECT aliasu from #{$MYSQL_TB_USER} WHERE user='#{user.mom}';", false )
		if r.first
			aliasm = r.first['aliasu']
			aliasm = user.mom if aliasm == '' || aliasm == nil
		end
	end

	note_code = generate_code( user.name, 'n' )
	db.query( "UPDATE #{$MYSQL_TB_MEDIA} SET code='#{note_code}' WHERE code='note_tmp_new' AND user='#{user.name}';", true )

	r = db.query( "SELECT code FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' AND origin='#{note_code}';", false )
	if r.first
		db.query( "INSERT INTO #{$MYSQL_TB_NOTE} SET origin='#{note_code}', code='#{r.first['code']}', user='#{user.name}', aliasm='#{aliasm}', note='', datetime='#{@datetime}';", true )
	else
		db.query( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE origin='note_tmp_new' AND user='#{user.name}';", true )
	end

	exit()
when 'delete'
	note_code = @cgi['code']
	p note_code if @debug
	db.query( "DELETE FROM #{$MYSQL_TB_NOTE} WHERE code='#{note_code}';", true )

when 'photo_upload'
	new_photo = Media.new( user )
	new_photo.load_cgi( @cgi )
	new_photo.save_photo( @cgi )
    new_photo.get_series()
    new_photo.save_db()

	code = @cgi['origin']
	recipe.load_db( code, true )

when 'photo_mv'
	target_photo = Media.new( user )
	target_photo.load_cgi( @cgi )
    target_photo.get_series()
    target_photo.move_series()
 
	code = @cgi['origin']
	recipe.load_db( code, true )

when 'photo_del'
	target_photo = Media.new( user )
	target_photo.load_cgi( @cgi )
	target_photo.delete_file( true )
	target_photo.delete_db( true )

	code = @cgi['origin']
	recipe.load_db( code, true )
end


daughter_delete = true

####
puts 'Extract note<br>' if @debug
note_html = ''
r = db.query( "SELECT * FROM #{$MYSQL_TB_NOTE} WHERE user='#{user.name}' ORDER BY datetime DESC;", false )
r.each do |e|
	note_date =  "#{e['datetime'].year}-#{e['datetime'].month}-#{e['datetime'].day} #{e['datetime'].hour}:#{e['datetime'].min}"

	note = e['note'].gsub( "\n", '<br>' )
puts e['code']
	note_html << '<div class="row">'
p e['aliasm']

	if e['media'] == nil
		if e['aliasm'] == ''
			note_html << '<div class="col-2"></div>'
			note_html << "<div class='col-9' >"
			note_html << "	<div class='alert alert-light'>#{note}<br><br>"
			note_html << "		<div align='right'>#{note_date}&nbsp;&nbsp;&nbsp;&nbsp;"
			if daughter_delete
				note_html << "			<input type='checkbox' id='#{e['code']}'>&nbsp;"
				note_html << "			<span onclick=\"deleteNote( '#{e['code']}' )\">#{l['trash']}</span>"
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
				note_html << "	<span onclick=\"deleteNote( '#{e['code']}' )\">#{l['trash']}</span>"
			end
			note_html << '</div></div></div>'
			note_html << '<div class="col-2"></div>'
		end
	else

		if e['aliasm'] == ''
			note_html << '<div class="col-2"></div>'
			note_html << "<div class='col-9' align='right'>"
			note_html << "<a href='#{$PHOTO}/#{e['code']}.jpg' target='photo'><img src='#{$PHOTO}/#{e['code']}-tn.jpg' class='img-thumbnail'></a><br>"
			note_html << "#{note_date}&nbsp;&nbsp;&nbsp;&nbsp;"
			if daughter_delete
				note_html << "<input type='checkbox' id='#{e['code']}'>&nbsp;"
				note_html << "<span onclick=\"deleteNoteP( '#{e['code']}', '#{e['media']}' )\">#{l['trash']}</span>"
			end
			note_html << '</div>'
			note_html << "<div class='col-1'>#{user.aliasu}</div>"
		else
			note_html << "<div class='col-1'>#{e['aliasm']}</div>"
			note_html << "<div class='col-9' align='left'>"
			note_html << "<a href='#{$PHOTO}/#{e['code']}.jpg' target='photo'><img src='#{$PHOTO}/#{e['code']}-tn.jpg' class='img-thumbnail'></a><br>"
			note_html << "#{note_date}&nbsp;&nbsp;&nbsp;&nbsp;"
			if user.mid != nil
				note_html << "<input type='checkbox' id='#{e['code']}'>&nbsp;"
				note_html << "<span onclick=\"deleteNoteP( '#{e['code']}', '#{e['media']}' )\">#{l['trash']}</span>"
			end
			note_html << '</div>'
			note_html << '<div class="col-2"></div>'
		end
	end
	note_html << '</div><br>'
end


#### HTML
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-10">
			<div class="row">
				<textarea  class="form-control" id='note' value=''></textarea><br>
			</div>
			<br>
			<div class="row">
				<div class='col-5'>
					<form method='post' enctype='multipart/form-data' id='photo_form'>
						<div class="input-group input-group-sm">
							<label class='input-group-text'>#{l['camera']}</label>
							<input type='file' class='form-control' name='photo' onchange="photoNoteSave( 'note_tmp_new', '', '', 'note' )">
						</div>
					</form>
				</div>
			</div>
			<br>
			#{note_html}
		</div>

		<div class="col-2">
			<button class='btn btn-sm btn-success' onclick="writeNote()">#{l['pencil']}</button>
		</div>
	</div>
</div>
HTML

puts html





