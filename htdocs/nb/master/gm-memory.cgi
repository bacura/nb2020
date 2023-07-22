#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 GM memory editor 0.02b (2023/07/17)

#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require '../soul'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'list' 	=> "記憶一覧",\
		'delete' 	=> "削除",\
		'category' 	=> "カテゴリー",\
		'item_num' 	=> "項目数",\
		'new_cate' 	=> "新規カテゴリー",\
		'regist' 	=> "登録",\
		'new_reg' 	=> "新規登録",\
		'key'	=> "キー",\
		'memory'	=> "記憶",\
		'rank' 	=> "ランク",\
		'move' 	=> "移動",\
		'save' 	=> "保存",\
		'memory_edit' => "記憶管理:"
	}

	return l[language]
end

#### init
def init( l, db )
	category_list = []
	pointer_num = []


	r = db.query( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY};", false )
	r.each do |e|
		rr = db.query( "SELECT pointer FROM #{$MYSQL_TB_MEMORY} WHERE category='#{e['category']}';", false )
		category_list << e['category']
		pointer_num << rr.size
	end

	list_html = ''
	category_list.size.times do |c|
		list_html << "<tr>"
		list_html << "<td><input type='text' size='32' id='#{category_list[c]}' value='#{category_list[c]}' onchange=\"changeCategory( '#{category_list[c]}' )\"></td>"
		list_html << "<td>#{pointer_num[c]}</td>"
		list_html << "<td><button type='button' class='btn btn-primary btn-sm' onclick=\"listPointerGM( '#{category_list[c]}' )\"\">#{l['list']}</button></td>"
		list_html << "<td><input type='checkbox' id='delete_check#{c}'>&nbsp;"
		list_html << "<button type='button' class='btn btn-danger btn-sm' onclick=\"deleteCategory( '#{category_list[c]}', 'delete_check#{c}' )\">#{l['delete']}</button></td>"
		list_html << "</tr>"
	end

	memory_html = <<-"MEMORY"
	<table class='table table-striped'>
	<thead>
	<th>#{l['cotegory']}</th>
	<th>#{l['item_num']}</th>
	<th></th>
	<th></th>
	</thead>
		#{list_html}
	</table>
MEMORY

	new_html = <<-"NEW"
	<div class='row'>
		<div class='col-6'></div>
		<div class='col-6'>
			<div class="input-group input-group">
				<span class='input-group-text' id='inputGroup-sizing-sm'>#{l['new_cate']}</span>
 				<input type='text' class='form-control' id='category'>
				<button type='button' class='btn btn-success' onclick="saveCategory()">#{l['regist']}</button>
			</div>
		</div>
	</div>
	<br>
NEW

	return new_html, memory_html
end

#### Listing pointers
def list( category, l, db )
	new_html = ''
	memory_html = ''

	new_html << "<div class='row'>"
	new_html << "<div class='col-10'></div>"
	new_html << "<div class='col-2'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"newPMemoryGM( '#{category}', '', 'front' )\">#{l['new_reg']}</button></div>"
	new_html << "</div>"
	new_html << "</div>"

	r = db.query( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", false )
	memory_html << "<table class='table table-sm table-striped'>"
	memory_html << "<thead>"
	memory_html << "<th>#{'key'}</th>"
	memory_html << "<th>#{l['memory']}</th>"
	memory_html << "<th>#{l['rank']}</th>"
	memory_html << "</thead>"

	c = 0
	r.each do |e|
		memory_html << "<tr onclick=\"newPMemoryGM( '#{category}', '#{e['pointer']}', 'front' )\">"
		memory_html << "<td>#{e['pointer']}</td>"
		if e['memory'].size > 80
			memory_html << "<td>#{e['memory'][0, 80]}...</td>"
		else
			memory_html << "<td>#{e['memory']}</td>"
		end
		memory_html << "<td>#{e['rank']}</td>"
		memory_html << "</tr>"
		c += 1
	end
	memory_html << "</table>"

	return new_html, memory_html
end


#### Pointer editor
def new_pointer( category, pointer, memory, rank, category_set, post_process, l )
	rank_select_html = ''
	rank_select_html << "<select class='form-select form-select-sm' id='rank'>"
	1.upto( 5 ) do |c|
		if c == rank
			rank_select_html << "<option value='#{c}' SELECTED>#{c}</option>"
		else
			rank_select_html << "<option value='#{c}'>#{c}</option>"
		end
	end
	rank_select_html << "</select>"

	category_select_html = ''
	category_select_html << "<select class='form-select form-select-sm' id='mvcategory'>"
	category_set.each do |e|
		if e == category
			category_select_html << "<option value='#{e}' SELECTED>#{e}</option>"
		else
			category_select_html << "<option value='#{e}'>#{e}</option>"
		end
	end
	category_select_html << "</select>"

	new_html = <<-"NEW"
	<div class='row'>
		<div class='col-6'>
			<div class='input-group input-group-sm'>
				<span class='input-group-text' id='inputGroup-sizing-sm'>#{l['key']}</span>
				<input type='text' class='form-control' id='pointer' value='#{pointer}'>
			</div>
		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text' for='rank'>#{l['rank']}</label>
				#{rank_select_html}
			</div>
		</div>
		<div class='col-4'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text' for='mvcategory'>#{l['category']}</label>
				#{category_select_html}
				<button type='button' class='btn btn-success btn-sm' onclick="movePMemory( '#{category}', '#{pointer}', '#{post_process}' )">#{l['move']}</button>
			</div>
		</div>
	</div><br>
NEW

	memory_html = <<-"MEMORY"
	<div class='row'>
		<textarea class='form-control' rows='5' aria-label='memory' id='memory'>#{memory}</textarea>
	</div><br>
	<div class='row'>
		<div class='col-1'><button type='button' class='btn btn-success btn-sm' onclick="savePMemory( '#{category}', '#{post_process}' )">#{l['save']}</button></div>
		<div class='col-9'></div>
		<div class='col-2' align='right'><input type='checkbox' id='deletepm_check'>&nbsp;
		<button type='button' class='btn btn-danger btn-sm' onclick="deletePMemory( '#{category}', '#{pointer}', '#{post_process}' )">#{l['delete']}</button></div>
	</div>
MEMORY

	return new_html, memory_html
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
db = Db.new( user, @debug, false )


#### GM check
if user.status < 8
	puts "GM error."
	exit
end


#### Getting POST data
command = @cgi['command']
mode = @cgi['mode']
category = @cgi['category']
new_category = @cgi['new_category']
mvcategory = @cgi['mvcategory']
pointer = @cgi['pointer']
rank = @cgi['rank'].to_i
post_process = @cgi['post_process']
memory = @cgi['memory']
memory_solid = @cgi['memory']
memory_solid.gsub!( ',', "\t" ) if memory_solid != nil && memory_solid != ''
if @debug
	puts "command:#{command}<br>\n"
	puts "mode:#{mode}<br>\n"
	puts "category:#{category}<br>\n"
	puts "new_category:#{new_category}<br>\n"
	puts "mvcategory:#{mvcategory}<br>\n"
	puts "pointer:#{pointer}<br>\n"
	puts "rank:#{rank}<br>\n"
	puts "post_process:#{post_process}<br>\n"
#	puts "memory:#{memory}<br>\n"
#	puts "memory_solid:#{memory_solid}<br>\n"
	puts "<hr>\n"
end


memory_html = ''
new_html = ''
case command
when 'init'
	new_html, memory_html = init( l, db )

when 'save_category'
	r = db.query( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", true )
	db.query( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='', memory='', category='#{category}', rank='1', date='#{@datetime}';", true ) unless r.first

	new_html, memory_html = init( l, db )

when 'change_category'
	db.query( "UPDATE #{$MYSQL_TB_MEMORY} SET category='#{new_category}' WHERE category='#{category}';", true )
	new_html, memory_html = init( l, db )

when 'delete_category'
	db.query( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", true )
	new_html, memory_html = init( l, db )

when 'list_pointer'
	puts 'List_pointer<br>' if @debug
	new_html, memory_html = list( category, l ,db )

when 'new_pointer'
	puts 'New pointer<br>' if @debug
	if pointer != ''
		r = db.query( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false )
		if r.first
			pointer = r.first['pointer']
			memory = r.first['memory']
			rank = r.first['rank']
		end
	end

	category_set = []
	r = db.query( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY};", false )
	r.each do |e| category_set << e['category'] end

	new_html, memory_html = new_pointer( category, pointer, memory, rank, category_set, post_process, l )

when 'delete_pointer'
	db.query( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", true )

	exit() unless post_process == 'front'
	new_html, memory_html = list( category, l, db )

when 'save_pointer'
	r = db.query( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false )
	if r.first
		db.query( "UPDATE #{$MYSQL_TB_MEMORY} SET memory='#{memory_solid}', category='#{category}', rank='#{rank}', date='#{@datetime}' WHERE category='#{category}' AND pointer='#{pointer}';", true )
	else
		db.query( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='#{pointer}', memory='#{memory_solid}', category='#{category}', rank='#{rank}', date='#{@datetime}';", true )
	end

	exit() unless post_process == 'front'
	new_html, memory_html = list( category, l, db )

when 'move_pointer'
	r = db.query( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{mvcategory}' AND pointer='#{pointer}';", false )
	if r.first
		t = r.first['memory']
		t << memory
		db.query( "UPDATE #{$MYSQL_TB_MEMORY} SET memory='#{t}', rank='#{rank}', date='#{@datetime}' WHERE category='#{mvcategory}' AND pointer='#{pointer}';", true )
	else
		db.query( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='#{pointer}', memory='#{memory_solid}', category='#{mvcategory}', rank='#{rank}', date='#{@datetime}';", true )
	end
	db.query( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", true )

	exit() unless post_process == 'front'
	new_html, memory_html = list( category, l, db )

end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{l['memory_edit']} #{category}</h5></div>
	</div>
	#{new_html}
	#{memory_html}
</div>
HTML

puts html
