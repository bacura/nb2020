#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 memory editor 0.2.3b (2024/05/9)

#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'
require './body'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese 
	l['jp'] = {
		'mkanri'	=> "記憶:",\
		'edit'	=> "編集",\
		'category'	=> "カテゴリー",\
		'item_num'	=> "項目数",\
		'new'	=> "新規カテゴリー",\
		'key'	=> "キー",\
		'memory'	=> "記憶",\
		'rank'	=> "ランク",\
		'move'	=> "移動",\
		'save'	=> "保存",\
		'idkw'	=> "ちょっと何言っているかわからないです。",\
		'delete'	=> "削除",\
		'regist'	=> "新規登録",\
		're_search'	=> "再検索"
	}

	return l[language]
end


#### EXPAND memory
def extend_linker( user, solid, depth )
	photo = Media.new( user )
	photo.base = 'memory'
	depth += 1 if depth < 5

	content_ = ''
	content_line = solid['content'].split( "\n" )
	content_line.each do |e|
		if /^\@/ =~ e
			t = e.delete( '@' )
			content_ << "<span class='print_comment'>(#{t})</span>\n"
		elsif /^\!/ =~ e
			t = e.delete( '!' )
			content_ << "<span class='print_subtitle'>#{t}</span>\n"
		elsif /^\#/ =~ e
			#
		elsif /^\~/ =~ e
			t = e.delete( '~' )
			content_ << "<a href='#{t}' target='blank_'>#{t}</a>" + "\n"
		elsif /^\[\]/ =~ e
			t = e.chomp.sub( /^\[\]/, '' )
			content_ << "<table>"
			rows = t.split( '[]' )
			rows.each do |row|
				content_ << "<tr>"
				cols = row.split('|')
					cols.each do |ee| content_ << "<td style='padding-top:0.2em; padding-bottom:0.2em; padding-left:0.5em; padding-right:0.5em; border-bottom:solid 1px; border-top:solid 1px;'>#{ee}</td>" end
				content_ << "</tr>"
			end
			content_ << "</table>\n"
		else
			content_ << e + "\n"
		end
	end

	link_pointer = solid['content'].scan( /\{\{[^\}\}]+\}\}/ )
	link_pointer.uniq!
	link_pointer.each do |e|
		t = e.sub( '{{', "" ).sub( '}}', "" )
		t.gsub!( '<', "&lt;" )
		t.gsub!( '>', "&gt;" )

		pointer_ = e.sub( '{{', "<span class='memory_link' onclick=\"memoryOpenLink( '#{t}', '#{depth}' )\">" )
		pointer_.sub!( '}}', "</span>" )
		content_.gsub!( e, pointer_ )
	end
	content_.gsub!( "\n", "<br>\n" )
	photo.origin = solid['code']
	photo.get_series()
	add_photo = photo.html_series( '-tn', 100, 1 )
	add_photo = '' if add_photo == 'No photo'
	content_ << add_photo

	return content_
end


#### Alike pointer
def alike_pointer( key, user )
	pointer = ''
	pointer_h = Hash.new
	score = 0.0
	memory = Memory.new( user )

	begin
		normal = key.tr( 'ぁ-ん０-９A-ZA-Z', 'ァ-ン0-9a-za-z' )
		normal.gsub!( '一', '1' )
		normal.gsub!( '二', '2' )
		normal.gsub!( '三', '3' )
		normal.gsub!( '四', '4' )
		normal.gsub!( '五', '5' )
		normal.gsub!( '六', '6' )
		normal.gsub!( '七', '7' )
		normal.gsub!( '八', '8' )
		normal.gsub!( '九', '9' )
		normal.gsub!( '（', '(' )
		normal.gsub!( '）', ')' )
		normal.gsub!( '％', '%' )
		normal.gsub!( '．', '.' )
		normal.gsub!( '＝', '=' )
		normal.gsub!( '＋', '+' )
		normal.gsub!( '－', '-' )

		pointers = memory.get_pointers()
		pointers.each do |e|
			normal_pointer = e.tr( 'ぁ-ん０-９A-ZA-Z', 'ァ-ン0-9a-za-z' )
			normal_pointer.gsub!( '一', '1' )
			normal_pointer.gsub!( '二', '2' )
			normal_pointer.gsub!( '三', '3' )
			normal_pointer.gsub!( '四', '4' )
			normal_pointer.gsub!( '五', '5' )
			normal_pointer.gsub!( '六', '6' )
			normal_pointer.gsub!( '七', '7' )
			normal_pointer.gsub!( '八', '8' )
			normal_pointer.gsub!( '九', '9' )
			normal_pointer.gsub!( '（', '(' )
			normal_pointer.gsub!( '）', ')' )
			normal_pointer.gsub!( '％', '%' )
			normal_pointer.gsub!( '．', '.' )
			normal_pointer.gsub!( '＝', '=' )
			normal_pointer.gsub!( '＋', '+' )
			normal_pointer.gsub!( '－', '-' )
			small = ''
			large = ''
			large_size = 1
			score_ = 0.0

			if normal.size <= normal_pointer.size
				small = normal
				large = normal_pointer
				large_size = normal_pointer.size
			else
				small = normal_pointer
				large = normal
				large_size = normal.size
			end

			a = small.split( '' )
			follower = ''

			a.each do |ee|
				begin
					if /#{follower}#{ee}/ =~ large
						score_ += 3 if /#{follower}#{ee}/ =~ large
						follower = ee
					elsif /#{ee}/ =~ large
						score_ += 1 if /#{ee}/ =~ large
						follower = ee
					else
						follower = ''
					end
				rescue
					follower = ''
				end
			end
			pointer_h[e] = score_ / large_size
		end

		ap = pointer_h.max do |k, v| k[1] <=> v[1] end
		score = ap[1].round( 1 )
		pointer = ap[0] if score >= 1.5
	rescue
	end

	return pointer, score
end


# Add new pointer form
def new_pointer_form( memory, l )
	html = "<div class='input-group input-group-sm'>"
	html << "<label class='input-group-text'>#{l['category']}</label>"
	html << "<select class='form-select' id='ref_new_categoly'>"
	categories = memory.get_categories()
	categories.each do |e| html << "<option value='#{e}'>#{e}</option>" end
	html << "</select>"
	html << "<button type='button' class='btn btn-outline-primary' onclick=\"newMemory( '', '#{memory.pointer}', 'refer' )\"`>#{l['regist']}</button>"
	html << "</div>"

	return html
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
db = Db.new( user, @debug, false )
memory = Memory.new( user )

#### Getting POST data
command = @cgi['command']
code = @cgi['code']
mode = @cgi['mode']
category = @cgi['category']
depth = @cgi['depth'].to_i
#new_category = @cgi['new_category']
#mvcategory = @cgi['mvcategory']
pointer = @cgi['pointer']
words = @cgi['words']
#post_process = @cgi['post_process']
#memory = @cgi['memory']
#memory_solid = @cgi['memory']
#memory_solid.gsub!( ',', "\t" ) if memory_solid != nil && memory_solid != ''
if @debug
	puts "command:#{command}<br>\n"
	puts "code:#{code}<br>\n"
	puts "mode:#{mode}<br>\n"
	puts "category:#{category}<br>\n"
#	puts "new_category:#{new_category}<br>\n"
	puts "pointer:#{pointer}<br>\n"
	puts "words:#{words}<br>\n"
#	puts "memory:#{memory}<br>\n"
#	puts "memory_solid:#{memory_solid}<br>\n"
	puts "<hr>\n"
end


memory_html = ''
new_html = ''
case command
when 'open'
	if pointer != ''
		r = db.query( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false )
		code = r.first['code']
		pointer = r.first['pointer']
		memory = r.first['memory']
		rank = r.first['rank']
	end

	category_set = []
	r = db.query( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY};", false )
	r.each do |e| category_set << e['category'] end

	new_html, memory_html = new_pointer( code, category, pointer, memory, rank, category_set, post_process, db, l )

when 'refer'
	puts "Referencing memory" if @debug
	words.gsub!( '　', ' ' )
	words.gsub!( /\s+/, ' ' )
	a = words.split( ' ' )
	score = 0

	a.each do |e|
		memory.pointer = e
		memory_solid = memory.get_solid( '' )

		if memory_solid.size > 0
			puts "Finding in DB<br>" if @debug
			memory_html << "<div class='row'>"
			memory_html << "<div class='col-8'><span class='memory_pointer'>#{e}</span>&nbsp;&nbsp;<span class='badge bg-info text-dark' onclick=\"memoryOpenLink( '#{e}', '1' )\">#{l['re_search']}</span></div>"
			memory_html << "<div class='col-4' align='right'>"
			memory_html << new_pointer_form( memory, l )
			memory_html << "</div>"
			memory_html << "</div>"

			memory_solid.each do |ee|
				r = db.query( "SELECT aliasu FROM #{$MYSQL_TB_USER} WHERE user='#{ee['user']}';", false )
				if r.first
					radio_name = r.first['aliasu'] if r.first['aliasu'] != ''
				else
					radio_name = ee['aliasu']
				end

				edit_button = ''
				edit_button = "&nbsp;<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick=\"editMemory( '#{ee['code']}', 'refer' )\">#{l['edit']}</button>"
				memory_html << extend_linker( user, ee, depth )
				memory_html << "<div align='right'>#{ee['category']} / #{ee['date'].year}/#{ee['date'].month}/#{ee['date'].day} (#{radio_name}) #{edit_button}</div>"
				db.query( "INSERT INTO #{$MYSQL_TB_SLOGM} SET user='#{user.name}', words='#{e}', score='9', date='#{@datetime}';", true )
			end
		else
			puts "No finding in DB<br>" if @debug
			a_pointer, score = alike_pointer( e, user )
			unless a_pointer == ''
				memory.pointer = a_pointer
				memory_solid = memory.get_solid( '' )

				r = db.query( "SELECT aliasu FROM #{$MYSQL_TB_USER} WHERE user='#{user.name}';", false )
				if r.first
					radio_name = r.first['aliasu'] if r.first['aliasu'] != ''
				else
					radio_name = user.name
				end

				pointer = ''
				memory_html << "<div class='row'>"
				memory_html << "<div class='col-8'><span class='memory_pointer'>#{a_pointer}&nbsp;??</span>&nbsp;&nbsp;<span class='badge bg-info text-dark' onclick=\"memoryOpenLink( '#{a_pointer}', '1' )\">#{l['re_search']}</span></div>"
				memory_html << "<div class='col-4' align='right'>"
				memory_html << new_pointer_form( memory, l )
				memory_html << "</div>"
				memory_html << "</div>"

				memory_solid.each do |ee|
					edit_button = ''
					edit_button = "&nbsp;<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick=\"editMemory( '#{ee['code']}', 'refer' )\">#{l['edit']}</button>"
					memory_html << extend_linker( user, ee, depth )
					memory_html << "<div align='right'>#{ee['category']} / #{ee['date'].year}/#{ee['date'].month}/#{ee['date'].day} (#{radio_name}) #{edit_button}</div>"
				end
			end
			db.query( "INSERT INTO #{$MYSQL_TB_SLOGM} SET user='#{user.name}', words='#{e}', score='#{score}', date='#{@datetime}';", true )
		end
	end

	if memory_html == ''
		memory_html << "<div class='row'>"
		memory_html << "<div class='col'>#{l['idkw']} (#{words})</div>"
		memory_html << "</div>"
		memory_html << "<br>"

		memory_html << "<div class='row'>"
		memory_html << "<div class='col-4'>"
		memory_html << new_pointer_form( memory, l )
		memory_html << "</div>"
		memory_html << "</div>"
	end

#when 'refer_code'
#	puts "Referencing memory code" if @debug
#	r = db.query( "SELECT * from #{$MYSQL_TB_MEMORY} WHERE code='#{code}';", false )
#	if r.first
#		puts "Finding in DB<br>" if @debug
#		pointer = r.first['pointer']
#		memory_html << "<div class='row'>"
#		memory_html << "<div class='col-8'><span class='memory_pointer'>#{pointer}</span>&nbsp;&nbsp;<span class='badge bg-info text-dark' onclick=\"memoryOpenLink( '#{pointer}', '1' )\">#{l['re_search']}</span></div>"
#		memory_html << "<div class='col-4' align='right'>"
#		memory_html << new_pointer_form( db, pointer, l )
#		memory_html << "</div>"
#		memory_html << "</div>"
#
#		edit_button = ''
#		edit_button = "&nbsp;<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick=\"newPMemoryGM( '#{code}', '#{r.first['category']}', '#{r.first['pointer']}', 'back' )\">#{l['edit']}</button>" if user.status >= 8
#		memory_html << extend_linker( db, r.first, depth )
#		memory_html << "<div align='right'>#{r.first['category']} / #{r.first['date'].year}/#{r.first['date'].month}/#{r.first['date'].day}#{edit_button}</div>"
#	else
#		puts "No finding in DB<br>" if @debug
#	end
end


title = ''
title = "<div class='col'><h5>#{l['mkanri']} #{category}</h5></div>" if command != 'refer'
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'>#{title}</div>
	</div>
	#{memory_html}
</div>
HTML

puts html
