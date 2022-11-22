#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 recipe list 0.23b (2022/11/22)


#==============================================================================
#STATIC
#==============================================================================
script = 'recipel'
page_limit = 50
@debug = false


#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require 'fileutils'
require "./language_/#{script}.lp"


#==============================================================================
#DEFINITION
#==============================================================================

#### 表示範囲
def range_html( range, l )
	range_select = []
	0.upto( 5 ) do |i|
		if range == i
			range_select[i] = 'SELECTED'
		else
			range_select[i] = ''
		end
	end

	html = l['range']
	html << '<select class="form-select form-select-sm" id="range">'
	html << "<option value='0' #{range_select[0]}>#{l['all']}</option>"
	html << "<option value='1' #{range_select[1]}>#{l['draft']}</option>"
	html << "<option value='2' #{range_select[2]}>#{l['protect']}</option>"
	html << "<option value='3' #{range_select[3]}>#{l['public']}</option>"
	html << "<option value='4' #{range_select[4]}>#{l['normal']}</option>"
	html << "<option value='5' #{range_select[5]}>#{l['publicou']}</option>"
	html << '</select>'

	return html
end


#### 料理スタイル生成
def type_html( type, l )
	html = l['type']
	html << '<select class="form-select form-select-sm" id="type">'
	html << "<option value='99'>#{l['all']}</option>"
	@recipe_type.size.times do |c|
		s = ''
		s = 'SELECTED' if type == c
		html << "<option value='#{c}' #{s}>#{@recipe_type[c]}</option>"
	end
	html << '</select>'

	return html
end


#### 献立区分
def role_html( role, l )
	html = l['role']
	html << '<select class="form-select form-select-sm" id="role">'
	html << "<option value='99'>#{l['all']}</option>"
	@recipe_role.size.times do |c|
		s = ''
		s = 'SELECTED' if role == c
		html << "<option value='#{c}' #{s}>#{@recipe_role[c]}</option>"
	end
	s = ''
	s = 'SELECTED' if role == 100
	html << "<option value='100' #{s}>#{l['chomi']}</option>"
	html << '</select>'

	return html
end


#### 調理区分
def tech_html( tech, l )
	html = l['tech']
	html << '<select class="form-select form-select-sm" id="tech">'
	html << "<option value='99'>#{l['all']}</option>"
	@recipe_tech.size.times do |c|
		s = ''
		s = 'SELECTED' if tech == c
		html << "<option value='#{c}' #{s}>#{@recipe_tech[c]}</option>"
	end
html << '</select>'

	return html
end


#### 目安時間
def time_html( time, l )
	html = l['time']
	html << '<select class="form-select form-select-sm" id="time">'
	html << "<option value='99'>#{l['all']}</option>"
	@recipe_time.size.times do |c|
		s = ''
		s = 'SELECTED' if time == c
		html << "<option value='#{c}' #{s}>#{@recipe_time[c]}</option>"
	end
	html << '</select>'

	return html
end


#### 目安費用
def cost_html( cost, l )
	html = l['cost']
	html << '<select class="form-select form-select-sm" id="cost">'
	html << "<option value='99'>#{l['all']}</option>"
	@recipe_cost.size.times do |c|
		s = ''
		s = 'SELECTED' if cost == c
		html << "<option value='#{c}' #{s}>#{@recipe_cost[c]}</option>"
	end
	html << '</select>'

	return html
end


#### ページングパーツ
def pageing_html( page, page_start, page_end, page_max, l )
	html = ''
	html << '<ul class="pagination pagination-sm justify-content-end">'
	if page == 1
		html << "<li class='page-item disabled'><span class='page-link'>#{l['prevp']}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"recipeListP( #{page - 1} )\">#{l['prevp']}</span></li>"
	end
	html << "<li class='page-item'><a class='page-link' onclick=\"recipeListP( '1' )\">1…</a></li>" unless page_start == 1

	page_start.upto( page_end ) do |c|
		active = ''
		active = ' active' if page == c
		html << "<li class='page-item#{active}'><a class='page-link' onclick=\"recipeListP( #{c} )\">#{c}</a></li>"
	end

	html << "<li class='page-item'><a class='page-link' onclick=\"recipeListP( '#{page_max}' )\">…#{page_max}</a></li>" unless page_end == page_max
	if page == page_max
		html << "<li class='page-item disabled'><span class='page-link'>#{l['nextp']}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"recipeListP( #{page + 1} )\">#{l['nextp']}</span></li>"
	end
	html << '  </ul>'

	return html
end


def referencing( words, uname, sql_where_ij )
	words.gsub!( /\s+/, "\t")
	words.gsub!( /　+/, "\t")
	words.gsub!( /,+/, "\t")
	words.gsub!( /、+/, "\t")
	words.gsub!( /\t{2,}/, "\t")
	query_word = words.split( "\t" )
	query_word.uniq!

	# Recoding query & converting by DIC
	true_query = []
	query_word.each do |e|
		mdb( "INSERT INTO #{$MYSQL_TB_SLOGR} SET user='#{uname}', words='#{e}', date='#{@datetime}';", false, @debug )
		r = mdb( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE alias='#{e}';", false, @debug )
		if r.first
			rr = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE class1='#{r.first['org_name']}' OR class2='#{r.first['org_name']}' OR class3='#{r.first['org_name']}';", false, @debug )
			if rr.first
				rr.each do |ee| true_query << ee['name'] end
			else
				true_query << r.first['org_name']
			end
		else
			true_query << e
		end
	end
	true_query.uniq!

	if @debug
		puts "query_word:#{query_word}<br>"
		puts "true_query:#{true_query}<br>"
		puts "<hr>"
	end

	# Referencing recipe
	true_query.each do |e|
		if e =~ /\-r\-/
			return mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{e}' AND ( user='#{uname}' OR public='1' );", false, @debug )
		else
			return mdb( "SELECT t1.* FROM #{$MYSQL_TB_RECIPE} AS t1 INNER JOIN #{$MYSQL_TB_RECIPEI} AS t2 ON t1.code = t2.code #{sql_where_ij} AND t2.word='#{e}';", false, @debug )
		end
	end
end

#==============================================================================
# Main
#==============================================================================

user = User.new( @cgi )
l = language_pack( user.language )


r = mdb( "SELECT icache, recipe, recipel_max FROM cfg WHERE user='#{user.name}';", false, false )
if r.first['icache'].to_i == '1'
	html_init_cache( nil )
else
	html_init( nil )
end


page = 1
range = 0
type = 99
role = 99
tech = 99
time = 99
cost = 99
words = nil
page_limit = r.first['recipel_max'].to_i if r.first['recipel_max'].to_i > 0
recipe_cfg = Hash.new
begin
	recipe_cfg = JSON.parse( r.first['recipe'] ) if r.first['recipe'] != nil && r.first['recipe'] != ''
	page = recipe_cfg['page'].to_i
	page = 1 if page == 0
	range = recipe_cfg['range'].to_i
	type = recipe_cfg['type'].to_i
	role = recipe_cfg['role'].to_i
	tech = recipe_cfg['tech'].to_i
	time = recipe_cfg['time'].to_i
	cost = recipe_cfg['cost'].to_i
	words = recipe_cfg['words']
rescue
end
puts recipe_cfg if @debug


#### POST
command = @cgi['command']
code = @cgi['code']
if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "<hr>"
end


recipe_code_list = []
ref_msg = ''
case command
when 'reset'
	page = 1
	range = 0
	type = 99
	role = 99
	tech = 99
	time = 99
	cost = 99
	words = nil
when 'refer'
	words = @cgi['words']
	puts "words: #{words}<br>" if @debug
	page = 1

when 'delete'
	puts "Deleting photos<br>" if @debug
	r = mdb( "SELECT mcode FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' and code='#{code}';", false, @debug )
	r.each do |e|
		File.unlink "#{$PHOTO_PATH}/#{e['mcode']}-tns.jpg" if File.exist?( "#{$PHOTO_PATH}/#{e['mcode']}-tns.jpg" )
		File.unlink "#{$PHOTO_PATH}/#{e['mcode']}-tn.jpg" if File.exist?( "#{$PHOTO_PATH}/#{e['mcode']}-tn.jpg" )
		File.unlink "#{$PHOTO_PATH}/#{e['mcode']}.jpg" if File.exist?( "#{$PHOTO_PATH}/#{e['mcode']}.jpg" )
	end
	mdb( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' AND code='#{code}';", false, @debug )

	puts "Deleting recipe from DB<br>" if @debug
	recipe = Recipe.new( user.name )
	recipe.code = code
	recipe.delete_db

	puts "Clearing Sum<br>" if @debug
	r = mdb( "SELECT code FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	mdb( "UPDATE #{$MYSQL_TB_SUM} SET code='', name='', dish=1 WHERE user='#{user.name}';", false, @debug ) if r.first['code'] == code

when 'subspecies'
	# Loading original recipe
	recipe = Recipe.new( user.name )
	recipe.load_db( code, true )

	# Copying phots
	new_media_code = generate_code( user.name, 'p' )
	new_recipe_code = generate_code( user.name, 'r' )
	r = mdb( "SELECT mcode, origin FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' and code='#{code}';", false, @debug )
	if r.first
		r.each do |e|
			FileUtils.cp( "#{$PHOTO_PATH}/#{e['mcode']}-tns.jpg", "#{$PHOTO_PATH}/#{new_media_code}-tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{e['mcode']}-tns.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{e['mcode']}-tn.jpg", "#{$PHOTO_PATH}/#{new_media_code}-tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{e['mcode']}-tn.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{e['mcode']}-tn.jpg", "#{$PHOTO_PATH}/#{new_media_code}.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{e['mcode']}-tn.jpg" )
			mdb( "INSERT INTO #{$MYSQL_TB_MEDIA} SET user='#{user.name}', code='#{new_recipe_code}', mcode='#{new_media_code}', origin='#{r.first['origin']}', date='#{@datetime}';", false, @debug )
		end
	end

	# Insertinbg recipe into DB
	recipe.code = new_recipe_code
	recipe.public = 0
	recipe.protect = 0
	recipe.draft = 1
	recipe.date = @datetime
	recipe.root = code if command == 'subspecies'
	recipe.insert_db

when 'limit'
	page = @cgi['page'].to_i
	page = 1 if page == 0
	range = @cgi['range'].to_i
	type = @cgi['type'].to_i
	role = @cgi['role'].to_i
	tech = @cgi['tech'].to_i
	time = @cgi['time'].to_i
	cost = @cgi['cost'].to_i
end
if @debug
	puts "page: #{page}<br>"
	puts "range: #{range}<br>"
	puts "type: #{type}<br>"
	puts "role: #{role}<br>"
	puts "tech: #{tech}<br>"
	puts "time: #{time}<br>"
	puts "cost: #{cost}<br>"
	puts "recipe_code_list: #{recipe_code_list}<br>"
	puts "<hr>"
end


#### WHERE setting
sql_where = 'WHERE '
sql_where_ij = 'WHERE '
case range
# 自分の全て
when 0
	sql_where << " user='#{user.name}' AND name!=''"
	sql_where_ij << " t1.user='#{user.name}' AND t1.name!=''"
# 自分の下書き
when 1
	sql_where << "user='#{user.name}' AND name!='' AND draft='1'"
	sql_where_ij << "t1.user='#{user.name}' AND t1.name!='' AND t1.draft='1'"
# 自分の保護
when 2
	sql_where << "user='#{user.name}' AND protect='1' AND name!=''"
	sql_where_ij << "t1.user='#{user.name}' AND t1.protect='1' AND t1.name!=''"
# 自分の公開
when 3
	sql_where << "user='#{user.name}' AND public='1' AND name!=''"
	sql_where_ij << "t1.user='#{user.name}' AND t1.public='1' AND t1.name!=''"
# 自分の無印
when 4
	sql_where << "user='#{user.name}' AND public='0' AND draft='0' AND name!=''"
	sql_where_ij << "t1.user='#{user.name}' AND t1.public='0' AND t1.draft='0' AND t1.name!=''"
# 他の公開
when 5
	sql_where << "public='1' AND user!='#{user.name}' AND name!=''"
	sql_where_ij << "t1.public='1' AND t1.user!='#{user.name}' AND t1.name!=''"
else
	sql_where << " user='#{user.name}' AND name!=''"
	sql_where_ij << " t1.user='#{user.name}' AND t1.name!=''"
end

sql_where << " AND type='#{type}'" unless type == 99
sql_where << " AND role='#{role}'" unless role == 99
sql_where << " AND tech='#{tech}'" unless tech == 99
sql_where << " AND time>0 AND time<=#{time}" unless time == 99
sql_where << " AND cost>0 AND cost<=#{cost}" unless cost == 99

sql_where_ij << " AND t1.type='#{type}'" unless type == 99
sql_where_ij << " AND t1.role='#{role}'" unless role == 99
sql_where_ij << " AND t1.tech='#{tech}'" unless tech == 99
sql_where_ij << " AND t1.time>0 AND t1.time<=#{time}" unless time == 99
sql_where_ij << " AND t1.cost>0 AND t1.cost<=#{cost}" unless cost == 99


#### 検索条件HTML
html_range = range_html( range, l )
html_type = type_html( type, l )
html_role = role_html( role, l )
html_tech = tech_html( tech, l )
html_time = time_html( time, l )
html_cost = cost_html( cost, l )


puts "Recipe list<br>" if @debug
recipes = []
recipe_num = 0
res = nil
ref_msg = words
if words != '' && words != nil
	res = referencing( words, user.name, sql_where_ij )
	ref_msg = "#{l['words']}#{words}<br>#{l['norecipe']}" if res.size == 0

	recipe_num = res.size
	offset = ( page - 1 ) * page_limit
	limit = offset + page_limit
else
	r = mdb( "SELECT COUNT(*) FROM #{$MYSQL_TB_RECIPE} #{sql_where};", false, @debug )
	recipe_num = r.first['COUNT(*)']

	offset = ( page - 1 ) * page_limit
	res = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} #{sql_where} ORDER BY name LIMIT #{offset}, #{page_limit};", false, @debug )
end
res.each do |e|
	o = Recipe.new( user.name )
	o.load_db( e, false )
	o.load_media
	recipes << o
end


puts "Paging parts<br>" if @debug
page_max = recipe_num / page_limit + 1
page_start = 1
page_end = page_max
if page_end > 5
	if page > 3
		page_start = page - 3
		page_start = page_max - 6 if page_max - page_start < 7
	end
	if page_end - page < 3
		page_end = page_max
	else
		page_end = page + 3
		page_end = 7 if page_end < 7
	end
else
	page_end = page_max
end
html_paging = pageing_html( page, page_start, page_end, page_max, l )


recipe_html = ''
recipes.each do |e|
	recipe_html << '<tr style="font-size:medium;">'
	if e.media[0] != nil
		recipe_html << "<td><a href='#{$PHOTO}/#{e.media[0]}.jpg' target='photo'><img src='#{$PHOTO}/#{e.media[0]}-tns.jpg'></a></td>"
	else
		recipe_html << "<td>-</td>"
	end

	tags =''
	e.tag().each do |ee| tags << "&nbsp;<span class='list_tag badge bbg' onclick=\"searchDR( '#{ee}' )\">#{ee}</span>" end
	recipe_html << "<td onclick=\"initCB( 'load', '#{e.code}', '#{e.user}' )\">#{e.name}</td><td>#{tags}</td>"

	recipe_html << "<td>"
	if e.public == 1
		recipe_html << l['globe']
	else
		recipe_html << l['space']
	end

	if e.protect == 1
		recipe_html << l['lock']
	else
		recipe_html << l['space']
	end

	if e.draft == 1
		recipe_html << l['cone']
	else
		recipe_html << l['space']
	end
	recipe_html << "</td>"
	recipe_html << "<td>"

	if user.status >= 2 && e.user == user.name
		recipe_html << "	<span onclick=\"addingMeal( '#{e.code}', '#{e.name}' )\">#{l['table']}</span>&nbsp;&nbsp;"
	end

	if user.status >= 2 && e.user == user.name
		recipe_html << "&nbsp;<span onclick=\"addKoyomi( '#{e.code}' )\">#{l['calendar']}</span>&nbsp;&nbsp;"
	end

	recipe_html << "	<span onclick=\"print_templateSelect( '#{e.code}' )\">#{l['printer']}</span>&nbsp;&nbsp;"

	if user.status >= 2 && e.user == user.name && ( e.root == nil || e.root == '' )
		recipe_html << "	<span onclick=\"recipeImport( 'subspecies', '#{e.code}', '#{page}' )\">#{l['diagram']}</span>"
	end

	if user.status >= 2 && e.user == user.name && ( e.root == nil || e.root == '' )
		recipe_html << "	<span onclick=\"cp2words( '#{e.code}', '' )\">#{l['dropper']}</span>"
	end
	recipe_html << "</td>"

	if e.user == user.name
		if e.protect == 0
			recipe_html << "<td><input type='checkbox' id='#{e.code}'>&nbsp;<span onclick=\"recipeDelete( '#{e.code}', #{page} )\">#{l['trash']}</span></td>"
		else
			recipe_html << "<td></td>"
		end
	end
	recipe_html << '</tr>'
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-7'><h5>#{l['recipel']} (#{recipe_num}) #{ref_msg}</h5></div>
		<div class='col-5'>#{html_paging}</div>
	</div>
	<br>
	<div class='row'>
		<div class='col'>#{html_range}</div>
		<div class='col'>#{html_type}</div>
		<div class='col'>#{html_role}</div>
		<div class='col'>#{html_tech}</div>
		<div class='col'>#{html_time}</div>
		<div class='col'>#{html_cost}</div>
	</div><br>
	<div class='row'>
		<button class="btn btn-info btn-sm" type="button" onclick="recipeListP( '#{page}' )">#{l['limit']}</button>
	</div>
	<br>
	<div class='row'>
		<div class='col' align="right"><span class="badge rounded-pill npill" type="button" onclick="recipeList( 'reset' )">#{l['reset']}</span></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
		<tr>
			<td>#{l['photo']}</td>
			<td>#{l['name']}</td>
			<td></td>
			<td>#{l['status']}</td>
			<td>#{l['operation']}</td>
			<td></td>
		</tr>
	</thead>

		#{recipe_html}
	</table>

	<div class='row'>
		<div class='col-7'></div>
		<div class='col-5'>#{html_paging}</div>
	</div>
</div>
HTML

puts html

#### 検索設定の保存
#words = nil if recipe_code_list.size == 0
recipe_ = JSON.generate( { "page" => page, "range" => range, "type" => type, "role" => role, "tech" => tech, "time" => time, "cost" => cost, "words" => words } )
mdb( "UPDATE #{$MYSQL_TB_CFG} SET recipe='#{recipe_}' WHERE user='#{user.name}';", false, @debug )
