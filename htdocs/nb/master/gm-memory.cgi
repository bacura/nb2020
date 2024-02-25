#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 GM memory 0.00b (2024/02/23)

#==============================================================================
# STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )
tmp = 'tmp_tmp'

#==============================================================================
# LIBRARY
#==============================================================================
require '../soul'
require '../brain'
require '../body'

#==============================================================================
# DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'list' 	=> "ポインタ一覧",\
		'delete' 	=> "削除",\
		'category' 	=> "カテゴリー",\
		'user' 	=> "ユーザー",\
		'new_cate' 	=> "新規カテゴリー",\
		'regist' 	=> "登録",\
		'new_reg' 	=> "新規ポインタ登録",\
		'key'	=> "ポインタ",\
		'memory'	=> "記憶",\
		'rank' 	=> "ランク",\
		'move' 	=> "移動",\
		'save' 	=> "保存",\
		'camera'	=> "<img src='bootstrap-dist/icons/camera.svg' style='height:1.2em; width:1.2em;'>",\
		'memory_edit' => "記憶管理GM:"
	}

	return l[language]
end

#### init category list
def html_category_list( memory, l )
	html = '<table class="table table-striped">'
	html << '<thead>'
	html << "<th>#{l['category']}</th>"
	html << '<th></th>'
	html << '<th></th>'
	html << '</thead>'

	categories = memory.get_categories()
	categories.each.with_index do |e, i|
		html << "<tr>"
		html << "<td><input type='text' size='32' id='#{e}' value='#{e}' onchange=\"changeCategory( '#{e}' )\"></td>"
		html << "<td><button type='button' class='btn btn-primary btn-sm' onclick=\"listPointers( '#{e}' )\"\">#{l['list']}</button></td>"
		html << "<td><input type='checkbox' id='delete_check#{i}'>&nbsp;"
		html << "<button type='button' class='btn btn-danger btn-sm' onclick=\"deleteCategory( '#{e}', 'delete_check#{i}' )\">#{l['delete']}</button></td>"
		html << "</tr>"
	end

	html << '</table>'

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

puts 'GM check<br>' if @debug
if user.status < 8
	puts "GM error."
	exit
end


puts 'Getting POST data<br>' if @debug
command = @cgi['command']
mode = @cgi['mode']
code = @cgi['code']
category = @cgi['category']
new_category = @cgi['new_category']
#mvcategory = @cgi['mvcategory']
pointer = @cgi['pointer']
#rank = @cgi['rank'].to_i
#post_process = @cgi['post_process']
content = @cgi['content']
#memory_solid = @cgi['memory']
#memory_solid.gsub!( ',', "\t" ) if memory_solid != nil && memory_solid != ''
if @debug
	puts "command:#{command}<br>\n"
	puts "mode:#{mode}<br>\n"
	puts "category:#{category}<br>\n"
	puts "new_category:#{new_category}<br>\n"
#	puts "mvcategory:#{mvcategory}<br>\n"
	puts "pointer:#{pointer}<br>\n"
#	puts "rank:#{rank}<br>\n"
#	puts "post_process:#{post_process}<br>\n"
#	puts "memory:#{memory}<br>\n"
#	puts "memory_solid:#{memory_solid}<br>\n"
	puts "<hr>\n"
end


html_list = ''
case command
when 'init'
	html_list = html_category_list( memory, l )

when 'save'
	memory.load_cgi( @cgi )
	memory.code = generate_code( user.name, 'k' )
	memory.pointer = tmp
	memory.content = tmp
	memory.date = @datetime
	memory.save_db()

	html_list = html_category_list( memory, l )

when 'change'
	memory.load_cgi( @cgi )
	memory.change_category( new_category )

	html_list = html_category_list( memory, l )

when 'delete'
	memory.load_cgi( @cgi )
	memory.delete_category()

	html_list = html_category_list( memory, l )

when 'pointers'
	html_list = "<div class='row'>"
	html_list << "<div class='col' align='right'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"newPMemoryGM( '', '#{category}', '', 'front' )\">#{l['new_reg']}</button></div>"
	html_list << "</div>"
	html_list << "</div>"

	html_list << "<table class='table table-sm table-striped'>"
	html_list << "<thead>"
	html_list << "<th>#{l['key']}</th>"
	html_list << "<th>#{l['memory']}</th>"
	html_list << "<th>#{l['user']}</th>"
	html_list << "</thead>"

	memory.load_cgi( @cgi )
	memory_solid = memory.get_solid()
	memory_solid.each do |e|
		code, pointer, content, uname = e.split( '::' )
		content = '' if content == nil

		html_list << "<tr onclick=\"newPMemoryGM( '#{code}', '#{memory.category}', '#{pointer}', 'front' )\">"
		html_list << "<td>#{pointer}</td>"

		if content.size > 80
			html_list << "<td>#{content[0, 80]}...</td>"
		else
			html_list << "<td>#{content}</td>"
		end
		html_list << "<td>#{uname}</td>"
		html_list << "</tr>"
	end
	html_list << "</table>"
end


puts 'HTML<br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{l['memory_edit']} #{category}</h5></div>
	</div>

	<div class='row'>
		<div class='col-7'></div>
		<div class='col-5'>
			<div class="input-group input-group-sm">
				<span class='input-group-text' id='inputGroup-sizing-sm'>#{l['new_cate']}</span>
 				<input type='text' class='form-control' id='new_category'>
				<button type='button' class='btn btn-success' onclick="newCategory()">#{l['regist']}</button>
			</div>
		</div>
	</div>
	<br>

	#{html_list}
</div>
HTML

puts html
