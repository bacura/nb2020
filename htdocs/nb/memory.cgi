#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 memory editor 0.14b (2022/10/29)

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'memory'
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
		list_html << "<td><input type='text' size='32' id='#{category_list[c]}' value='#{category_list[c]}' DISABLED></td>"
		list_html << "<td>#{pointer_num[c]}</td>"
		list_html << "<td><button type='button' class='btn btn-primary btn-sm' onclick=\"listPointer( '#{category_list[c]}' )\"\">#{lp[2]}</button></td>"
		list_html << "<td></td>"
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
def new_pointer( category, pointer, memory, rank, category_set, post_process, user, lp )
	disabled = ''
	disabled = 'DISABLED' if user.status < 8

	rank_select_html = ''
	rank_select_html << "<select class='form-select form-select-sm' id='rank' #{disabled}>"
	1.upto( 5 ) do |c|
		if c == rank
			rank_select_html << "<option value='#{c}' SELECTED>#{c}</option>"
		else
			rank_select_html << "<option value='#{c}'>#{c}</option>"
		end
	end
	rank_select_html << "</select>"

	category_select_html = ''
	category_select_html << "<select class='form-select form-select-sm' id='mvcategory' #{disabled}>"
	category_set.each do |e|
		if e == category
			category_select_html << "<option value='#{e}' SELECTED>#{e}</option>"
		else
			category_select_html << "<option value='#{e}'>#{e}</option>"
		end
	end
	category_select_html << "</select>"

	move_button = ''
	move_button = "<button type='button' class='btn btn-success btn-sm' onclick=\"movePMemory( '#{category}', '#{pointer}', '#{post_process}' )\">#{lp[12]}</button>" if user.status >= 8

	save_button = ''
	save_button = "<button type='button' class='btn btn-success btn-sm' onclick=\"savePMemory( '#{category}', '#{post_process}' )\">#{lp[13]}</button>" if user.status >= 8

	delete_button =  ''
	delete_button = "<input type='checkbox' id='deletepm_check'>&nbsp;<button type='button' class='btn btn-danger btn-sm' onclick=\"deletePMemory( '#{category}', '#{pointer}', '#{post_process}' )\">#{lp[3]}</button>" if user.status >= 8

	new_html = <<-"NEW"
	<div class='row'>
		<div class='col-6'>
			<div class='input-group input-group-sm'>
				<span class='input-group-text' id='inputGroup-sizing-sm'>#{lp[9]}</span>
				<input type='text' class='form-control' id='pointer' value='#{pointer}' #{disabled}>
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
				#{move_button}
			</div>
		</div>
	</div><br>
NEW

	memory_html = <<-"MEMORY"
	<div class='row'>
		<textarea class='form-control' rows='5' aria-label='memory' id='memory' #{disabled}>#{memory}</textarea>
	</div><br>
	<div class='row'>
		<div class='col-1'>#{save_button}</div>
		<div class='col-9'></div>
		<div class='col-2' align='right'>#{delete_button}</div>
	</div>
MEMORY

	return new_html, memory_html
end


#### EXPAND memory
def extend_linker( memory, depth )
	depth += 1 if depth < 5
	link_pointer = memory.scan( /\{\{[^\}\}]+\}\}/ )
	link_pointer.uniq!

	memory_ = memory
	link_pointer.each do |e|
		pointer = e.sub( '{{', "" ).sub( '}}', "" )
		pointer.gsub!( '<', "&lt;" )
		pointer.gsub!( '>', "&gt;" )

		pointer_ = e.sub( '{{', "<span class='memory_link' onclick=\"memoryOpenLink( '#{pointer}', '#{depth}' )\">" )
		pointer_.sub!( '}}', "</span>" )
		memory_.gsub!( e, pointer_ )
	end
	memory_.gsub!( "\n", "<br>\n" )

	return memory_
end


#### Alike pointer
def alike_pointer( key )
	pointer = ''
	pointer_h = Hash.new
	score = 0.0

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

		r = mdb( "SELECT pointer from #{$MYSQL_TB_MEMORY};", false, @debug )
		r.each do |e|
			normal_pointer = e['pointer'].tr( 'ぁ-ん０-９A-ZA-Z', 'ァ-ン0-9a-za-z' )
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
			pointer_h[e['pointer']] = score_ / large_size
		end

		ap = pointer_h.max do |k, v| k[1] <=> v[1] end
		score = ap[1].round( 1 )
		pointer = ap[0] if score >= 1.5
	rescue
	end

	return pointer, score
end


# Add new pointer form
def new_pointer_form( lp, user, pointer )
	html = ''
	if user.status >= 8
		r = mdb( "SELECT DISTINCT category from #{$MYSQL_TB_MEMORY};", false, @debug )
		if r.first
			html << "<div class='input-group input-group-sm'>"
			html << "<label class='input-group-text'>#{lp[4]}</label>"
			html << "<select class='form-select' id='nonmatch_categoly'>"
			r.each do |e| html << "<option value='#{e['category']}'>#{e['category']}</option>" end

			html << "</select>"
			html << "<button type='button' class='btn btn-outline-primary' onclick=\"newPMemoryNM( '#{pointer}', '' )\"`>#{lp[8]}</button>"
			html << "</div>"
		end
	end

	return html
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


#### Getting POST data
command = @cgi['command']
mode = @cgi['mode']
category = @cgi['category']
depth = @cgi['depth'].to_i
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
	mdb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='', memory='', category='#{category}', total_rank='1', rank='1', date='#{@datetime}';", false, @debug ) unless r.first

	new_html, memory_html = init( lp )

when 'change_category'
	mdb( "UPDATE #{$MYSQL_TB_MEMORY} SET category='#{new_category}' WHERE category='#{category}';", false, @debug )
	new_html, memory_html = init( lp )

when 'delete_category'
	mdb( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", false, @debug )
	new_html, memory_html = init( lp )

when 'list_pointer'
	new_html, memory_html = list( category, lp )

when 'new_pointer'
	if pointer != ''
		r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug )
		pointer = r.first['pointer']
		memory = r.first['memory']
		rank = r.first['rank']
	end

	category_set = []
	r = mdb( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY};", false, @debug )
	r.each do |e| category_set << e['category'] end

	new_html, memory_html = new_pointer( category, pointer, memory, rank, category_set, post_process, user, lp )

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

when 'refer'
	puts "Referencing memory" if @debug
	pointer.gsub!( '　', ' ' )
	pointer.gsub!( /\s+/, ' ' )
	a = pointer.split( ' ' )
	score = 0

	a.each do |e|
		r = mdb( "SELECT * from #{$MYSQL_TB_MEMORY} WHERE pointer='#{e}';", false, @debug )
		if r.first
			puts "Finding in DB<br>" if @debug
			pointer = ''
			memory_html << "<div class='row'>"
			memory_html << "<div class='col-8'><span class='memory_pointer'>#{e}</span>&nbsp;&nbsp;<span class='badge bg-info text-dark' onclick=\"memoryOpenLink( '#{e}', '1' )\">#{lp[15]}</span></div>"
			memory_html << "<div class='col-4' align='right'>"
			memory_html << new_pointer_form( lp, user, e )
			memory_html << "</div>"
			memory_html << "</div>"

			r.each do |ee|
				edit_button = ''
				edit_button = "&nbsp;<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick=\"newPMemory( '#{ee['category']}', '#{ee['pointer']}', 'back' )\">#{lp[3]}</button>" if user.status >= 8
				memory_html << extend_linker( ee['memory'], depth )
				memory_html << "<div align='right'>#{ee['category']} / #{ee['date'].year}/#{ee['date'].month}/#{ee['date'].day}#{edit_button}</div>"
			end

			count = r.first['count'].to_i + 1
			mdb( "UPDATE #{$MYSQL_TB_MEMORY} SET count='#{count}' WHERE pointer='#{e}';", false, @debug )
			mdb( "INSERT INTO #{$MYSQL_TB_SLOGM} SET user='#{user.name}', words='#{e}', score='9', date='#{@datetime}';", false ,@debug )
		else
			puts "No finding in DB<br>" if @debug
			a_pointer, score = alike_pointer( e )
			unless a_pointer == ''
				rr = mdb( "SELECT * from #{$MYSQL_TB_MEMORY} WHERE pointer='#{a_pointer}';", false, @debug )
				pointer = ''
				memory_html << "<div class='row'>"
				memory_html << "<div class='col-8'><span class='memory_pointer'>#{a_pointer}&nbsp;??</span>&nbsp;&nbsp;<span class='badge bg-info text-dark' onclick=\"memoryOpenLink( '#{e}', '1' )\">#{lp[15]}</span></div>"
				memory_html << "<div class='col-4' align='right'>"
				memory_html << new_pointer_form( lp, user, e )
				memory_html << "</div>"
				memory_html << "</div>"

				rr.each do |ee|
					edit_button = ''
					edit_button = "&nbsp;<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick=\"newPMemory( '#{ee['category']}', '#{ee['pointer']}', 'back' )\">#{lp[3]}</button>" if user.status >= 8
					memory_html << extend_linker( ee['memory'], depth )
					memory_html << "<div align='right'>#{ee['category']} / #{ee['date'].year}/#{ee['date'].month}/#{ee['date'].day}#{edit_button}</div>"
				end
				count = rr.first['count'].to_i + 1
				mdb( "UPDATE #{$MYSQL_TB_MEMORY} SET count='#{count}' WHERE pointer='#{a_pointer}';", false, @debug )
			end
			mdb( "INSERT INTO #{$MYSQL_TB_SLOGM} SET user='#{user.name}', words='#{e}', score='#{score}', date='#{@datetime}';", false ,@debug )
		end
	end

	if memory_html == ''
		memory_html << "<div class='row'>"
		memory_html << "<div class='col'>#{lp[14]} (#{pointer})</div>"
		memory_html << "</div>"
		memory_html << "<br>"

		memory_html << "<div class='row'>"
		memory_html << "<div class='col-6'>"
		memory_html << new_pointer_form( lp, user, pointer )
		memory_html << "</div>"
		memory_html << "</div>"
	end
end


title = ''
title = "<div class='col'><h5>#{lp[1]} #{category}</h5></div>" if command != 'refer'
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'>#{title}</div>
	</div>
	#{memory_html}
</div>
HTML

puts html
