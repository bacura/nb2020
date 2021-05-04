#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 GM memory editor 0.01b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'gm-memory'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### init
def init( lp )
	category_list = []
	pointer_num = []
	r = mdb( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY};", false, @debug )
	r.each do |e|
		rr = mdb( "SELECT pointer FROM #{$MYSQL_TB_MEMORY} WHERE category='#{e['category']}';", false, @debug )
		category_list << e['category']
		pointer_num << rr.size
	end

	list_html = ''
	category_list.size.times do |c|
		list_html << "<tr>"
		list_html << "<td><input type='text' size='32' id='#{category_list[c]}' value='#{category_list[c]}' onchange=\"changeCategory( '#{category_list[c]}' )\"></td>"
		list_html << "<td>#{pointer_num[c]}</td>"
		list_html << "<td><button type='button' class='btn btn-primary btn-sm' onclick=\"listPointer( '#{category_list[c]}' )\"\">#{lp[2]}</button></td>"
		list_html << "<td><input type='checkbox' id='delete_check#{c}'>&nbsp;"
		list_html << "<button type='button' class='btn btn-danger btn-sm' onclick=\"deleteCategory( '#{category_list[c]}', 'delete_check#{c}' )\">#{lp[3]}</button></td>"
		list_html << "</tr>"
	end

	memory_html = <<-"MEMORY"
	<table class='table table-striped'>
	<thead>
	<th>#{lp[4]}</th>
	<th>#{lp[5]}</th>
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
				<span class='input-group-text' id='inputGroup-sizing-sm'>#{lp[6]}</span>
 				<input type='text' class='form-control' id='category'>
				<button type='button' class='btn btn-success' onclick="saveCategory()">#{lp[7]}</button>
			</div>
		</div>
	</div>
	<br>
NEW

	return new_html, memory_html
end

#### Listing pointers
def list( category, lp )
	new_html = ''
	memory_html = ''

	new_html << "<div class='row'>"
	new_html << "<div class='col-10'></div>"
	new_html << "<div class='col-2'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"newPMemory( '#{category}', '', 'front' )\">#{lp[8]}</button></div>"
	new_html << "</div>"
	new_html << "</div>"

	r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", false, @debug )
	memory_html << "<table class='table table-sm table-striped'>"
	memory_html << "<thead>"
	memory_html << "<th>#{lp[9]}</th>"
	memory_html << "<th>#{lp[10]}</th>"
	memory_html << "<th>#{lp[11]}</th>"
	memory_html << "</thead>"

	c = 0
	r.each do |e|
		memory_html << "<tr onclick=\"newPMemory( '#{category}', '#{e['pointer']}', 'front' )\">"
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
def new_pointer( category, pointer, memory, rank, category_set, post_process, lp )
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
				<span class='input-group-text' id='inputGroup-sizing-sm'>#{lp[9]}</span>
				<input type='text' class='form-control' id='pointer' value='#{pointer}'>
			</div>
		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text' for='rank'>#{lp[11]}</label>
				#{rank_select_html}
			</div>
		</div>
		<div class='col-4'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text' for='mvcategory'>#{lp[4]}</label>
				#{category_select_html}
				<button type='button' class='btn btn-success btn-sm' onclick="movePMemory( '#{category}', '#{pointer}', '#{post_process}' )">#{lp[12]}</button>
			</div>
		</div>
	</div><br>
NEW

	memory_html = <<-"MEMORY"
	<div class='row'>
		<textarea class='form-control' rows='5' aria-label='memory' id='memory'>#{memory}</textarea>
	</div><br>
	<div class='row'>
		<div class='col-1'><button type='button' class='btn btn-success btn-sm' onclick="savePMemory( '#{category}', '#{post_process}' )">#{lp[13]}</button></div>
		<div class='col-9'></div>
		<div class='col-2' align='right'><input type='checkbox' id='deletepm_check'>&nbsp;
		<button type='button' class='btn btn-danger btn-sm' onclick="deletePMemory( '#{category}', '#{pointer}', '#{post_process}' )">#{lp[3]}</button></div>
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
lp = user.load_lp( script )


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
	new_html, memory_html = init( lp )

when 'save_category'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", false, @debug )
	mdb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='', memory='', category='#{category}', rank='1', date='#{@datetime}';", false, @debug ) unless r.first

	new_html, memory_html = init( lp )

when 'change_category'
	mdb( "UPDATE #{$MYSQL_TB_MEMORY} SET category='#{new_category}' WHERE category='#{category}';", false, @debug )
	new_html, memory_html = init( lp )

when 'delete_category'
	mdb( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", false, @debug )
	new_html, memory_html = init( lp )

when 'list_pointer'
	puts 'List_pointer<br>' if @debug
	new_html, memory_html = list( category, lp )

when 'new_pointer'
	puts 'New pointer<br>' if @debug
	if pointer != ''
		r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug )
		if r.first
			pointer = r.first['pointer']
			memory = r.first['memory']
			rank = r.first['rank']
		end
	end

	category_set = []
	r = mdb( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY};", false, @debug )
	r.each do |e| category_set << e['category'] end

	new_html, memory_html = new_pointer( category, pointer, memory, rank, category_set, post_process, lp )

when 'delete_pointer'
	mdb( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug )

	exit() unless post_process == 'front'
	new_html, memory_html = list( category, lp )

when 'save_pointer'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false , @debug )
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_MEMORY} SET memory='#{memory_solid}', category='#{category}', rank='#{rank}', date='#{@datetime}' WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='#{pointer}', memory='#{memory_solid}', category='#{category}', rank='#{rank}', date='#{@datetime}';", false, @debug )
	end

	exit() unless post_process == 'front'
	new_html, memory_html = list( category, lp )

when 'move_pointer'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{mvcategory}' AND pointer='#{pointer}';", false , @debug )
	if r.first
		t = r.first['memory']
		t << memory
		mdb( "UPDATE #{$MYSQL_TB_MEMORY} SET memory='#{t}', rank='#{rank}', date='#{@datetime}' WHERE category='#{mvcategory}' AND pointer='#{pointer}';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='#{pointer}', memory='#{memory_solid}', category='#{mvcategory}', rank='#{rank}', date='#{@datetime}';", false, @debug )
	end
	mdb( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug )

	exit() unless post_process == 'front'
	new_html, memory_html = list( category, lp )

end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]} #{category}</h5></div>
	</div>
	#{new_html}
	#{memory_html}
</div>
HTML

puts html
