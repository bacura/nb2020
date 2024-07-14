#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 recipe list 0.4.1 (2024/07/13)
	

#==============================================================================
# STATIC
#==============================================================================
@debug = false
script = File.basename( $0, '.cgi' )

#==============================================================================
# LIBRARY
#==============================================================================
require './soul'
require './body'

#==============================================================================
# DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'recipel' 	=> "レシピ帳",\
		'words' 	=> "検索語：",\
		'norecipe' 	=> "検索条件のレシピは見つかりませんでした",\
		'prevp' 	=> "前項",\
		'nextp' 	=> "次項",\
		'range' 	=> "表示範囲",\
		'all' 		=> "全て",\
		'all_ns'	=> "全て（ー調%）",\
		'draft' 	=> "仮組",\
		'protect' 	=> "保護",\
		'public' 	=> "公開",\
		'normal' 	=> "無印",\
		'favoriter' => "お気に入り",\
		'publicou' 	=> "公開(他ユーザー)",\
		'type'	 	=> "料理スタイル",\
		'role' 		=> "献立区分",\
		'tech'	 	=> "調理区分",\
		'chomi'	 	=> "[ 調味％ ]",\
		'time' 		=> "目安時間(分)",\
		'cost'	 	=> "目安費用(円)",\
		'limit' 	=> "絞　り　込　み",\
		'reset' 	=> "条件クリア",\
		'photo' 	=> "写真",\
		'name' 		=> "レシピ名",\
		'status' 	=> "ステータス",\
		'family' 	=> "親子集合",\
		'display'	=> "表示数",\
		'delete'	=> "削除",\
		'pick'		=> "コードピック",\
		'com' 		=> "コマンド",\
		'menu' 		=> "献立＋",\
		'koyomi' 	=> "こよみ＋",\
		'daughter' 	=> "娘＋",\
		'import' 	=> "取込",\
		'print' 	=> "印刷",\
		'crosshair' => "<img src='bootstrap-dist/icons/crosshair.svg' style='height:1.0em; width:1.0em;'>",\
		'command' 	=> "<img src='bootstrap-dist/icons/command.svg' style='height:1.2em; width:1.2em;'>",\
		'globe' 	=> "<img src='bootstrap-dist/icons/globe.svg' style='height:1.2em; width:1.2em;'>",\
		'lock'		=> "<img src='bootstrap-dist/icons/lock-fill.svg' style='height:1.2em; width:1.2em;'>",\
		'cone' 		=> "<img src='bootstrap-dist/icons/cone-striped.svg' style='height:1.2em; width:1.2em;'>",\
		'table' 	=> "<img src='bootstrap-dist/icons/motherboard.svg' style='height:2.4em; width:2.4em;'>",\
		'calendar' 	=> "<img src='bootstrap-dist/icons/calendar-plus.svg' style='height:2.4em; width:2.4em;'>",\
		'printer' 	=> "<img src='bootstrap-dist/icons/printer.svg' style='height:2.4em; width:2.4em;'>",\
		'diagram' 	=> "<img src='bootstrap-dist/icons/diagram-3.svg' style='height:2.4em; width:2.4em;'>",\
		'cp2words'	=> "<img src='bootstrap-dist/icons/eyedropper.svg' style='height:2.4em; width:2.4em;'>",\
		'trash'		=> "<img src='bootstrap-dist/icons/trash-red.svg' style='height:2.4em; width:2.4em;'>",\
		'root' 		=> "<img src='bootstrap-dist/icons/person-circle.svg' style='height:1.2em; width:1.2em;'>",\
		'favorite' 	=> "<img src='bootstrap-dist/icons/star-fill-y.svg' style='height:1.2em; width:1.2em;'>",\
		'space' 	=> "　"
	}

	return l[language]
end


#### 表示範囲
def range_html( range, l )
	range_select = []
	7.times do |i|
		if range == i
			range_select[i] = 'SELECTED'
		else
			range_select[i] = ''
		end
	end

	html = l['range']
	html << '<select class="form-select form-select-sm" id="range">'
	html << "<option value='0' #{range_select[0]}>#{l['all']}</option>"
	html << "<option value='1' #{range_select[1]}>#{l['favoriter']}</option>"
	html << "<option value='2' #{range_select[2]}>#{l['draft']}</option>"
	html << "<option value='3' #{range_select[3]}>#{l['protect']}</option>"
	html << "<option value='4' #{range_select[4]}>#{l['public']}</option>"
	html << "<option value='5' #{range_select[5]}>#{l['normal']}</option>"
	html << "<option value='6' #{range_select[6]}>#{l['publicou']}</option>"
	html << '</select>'

	return html
end


#### 料理スタイル生成
def type_html( type, l )
	html = l['type']
	html << '<select class="form-select form-select-sm" id="type">'
	html << "<option value='99'>#{l['all']}</option>"
	@recipe_type.size.times do |c|
		html << "<option value='#{c}' #{$SELECT[type == c]}>#{@recipe_type[c]}</option>"
	end
	html << '</select>'

	return html
end


#### 献立区分
def role_html( role, l )
	html = l['role']
	html << '<select class="form-select form-select-sm" id="role">'
	html << "<option value='99'>#{l['all_ns']}</option>"
	@recipe_role.size.times do |c|
		html << "<option value='#{c}' #{$SELECT[role == c]}>#{@recipe_role[c]}</option>"
	end
	html << "<option value='100' #{$SELECT[role == 100]}>#{l['chomi']}</option>"
	html << '</select>'

	return html
end


#### 調理区分
def tech_html( tech, l )
	html = l['tech']
	html << '<select class="form-select form-select-sm" id="tech">'
	html << "<option value='99'>#{l['all']}</option>"
	@recipe_tech.size.times do |c|
		html << "<option value='#{c}' #{$SELECT[tech == c]}>#{@recipe_tech[c]}</option>"
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
		html << "<option value='#{c}' #{$SELECT[time == c]}>#{@recipe_time[c]}</option>"
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
		html << "<option value='#{c}' #{$SELECT[cost == c]}>#{@recipe_cost[c]}</option>"
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
	html << "<li class='page-item active'><a class='page-link' onclick=\"recipeListP( 1 )\">1</a></li>" if page_end == 0

	html << "<li class='page-item'><a class='page-link' onclick=\"recipeListP( '#{page_max}' )\">…#{page_max}</a></li>" unless page_end == page_max
	if page == page_max
		html << "<li class='page-item disabled'><span class='page-link'>#{l['nextp']}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"recipeListP( #{page + 1} )\">#{l['nextp']}</span></li>"
	end
	html << '  </ul>'

	return html
end


def referencing( words, db, sql_where_ij )
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
		db.query( "INSERT INTO #{$MYSQL_TB_SLOGR} SET user='#{db.user.name}', words='#{e}', date='#{@datetime}';", true )
		r = db.query( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE alias='#{e}';", false )
		if r.first
			rr = db.query( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE class1='#{r.first['org_name']}' OR class2='#{r.first['org_name']}' OR class3='#{r.first['org_name']}';", false )
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
			return db.query( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{e}' AND ( user='#{db.user.name}' OR public='1' );", false )
		else
			return db.query( "SELECT t1.* FROM #{$MYSQL_TB_RECIPE} AS t1 INNER JOIN #{$MYSQL_TB_RECIPEI} AS t2 ON t1.code = t2.code #{sql_where_ij} AND t2.word='#{e}';", false )
		end
	end
end


def recipe_line( recipe, user, page, color, l )
	html = "<tr style='font-size:medium; background-color:#{color};' oncontextmenu=\"modalTip( '#{recipe.code}' )\">"

	if recipe.media[0] != nil
		html << "<td><img src='#{$PHOTO}/#{recipe.media[0]}-tns.jpg' class='photo_tns' onclick=\"modalPhoto( '#{recipe.media[0]}' )\"></td>"
	else
		html << "<td>-</td>"
	end

	tags =''
	recipe.tag().each do |e| tags << "&nbsp;<span class='list_tag badge bbg' onclick=\"searchDR( '#{e}' )\">#{e}</span>" end
	if user.status >= 1
		html << "<td onclick=\"initCB( 'load', '#{recipe.code}', '#{recipe.user.name}' )\">#{recipe.name}</td><td>#{tags}</td>"
	else
		html << "<td><a href='login.cgi'>#{recipe.name}</a></td><td>#{tags}</td>"
	end

	html << "<td>"
	if recipe.favorite == 1
		html << l['favorite']
	else
		html << l['space']
	end

	if recipe.public == 1
		html << l['globe']
	else
		html << l['space']
	end

	if recipe.protect == 1
		html << l['lock']
	else
		html << l['space']
	end

	if recipe.draft == 1
		html << l['cone']
	else
		html << l['space']
	end
	html << "</td>"

	html << "<td onclick=\"modalTip( '#{recipe.code}' )\">#{l['command']}</td>"
	html << "</tr>"

	return html
end

#==============================================================================
# Main
#==============================================================================

user = User.new( @cgi )
l = language_pack( user.language )
db = Db.new( user, @debug, false )

r = db.query( "SELECT icache, recipe FROM cfg WHERE user='#{user.name}';", false )
if r.first
	if r.first['icache'].to_i == '1'
		html_init_cache( nil )
	else
		html_init( nil )
	end
else
	html_init_cache( nil )
end

page = 1
page_limit = 50
range = 0
type = 99
role = 99
tech = 99
time = 99
cost = 99
family = 0
words = nil
recipe_cfg = Hash.new

begin
	recipe_cfg = JSON.parse( r.first['recipe'] ) if r.first['recipe'] != nil && r.first['recipe'] != ''
	p recipe_cfg if @debug
	page = recipe_cfg['page'].to_i
	page = 1 if page == 0
	page_limit = recipe_cfg['page_limit'].to_i
	page_limit = 50 if page_limit == 0
	range = recipe_cfg['range'].to_i
	type = recipe_cfg['type'].to_i
	role = recipe_cfg['role'].to_i
	tech = recipe_cfg['tech'].to_i
	time = recipe_cfg['time'].to_i
	cost = recipe_cfg['cost'].to_i
	family = recipe_cfg['family'].to_i
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
	family = 0
	words = nil

when 'refer'
	page = 1
	range = 0
	type = 99
	role = 99
	tech = 99
	time = 99
	cost = 99
	family = 0
	words = @cgi['words']
	puts "words: #{words}<br>" if @debug

when 'delete'
	puts "Deleting photos<br>" if @debug
	if user.status != 7
		puts "Deleting media from DB, Real<br>" if @debug
		target_media = Media.new( user )
		target_media.origin = code
		target_media.get_series()
		target_media.delete_series( true )

		puts "Deleting recipe from DB<br>" if @debug
		recipe = Recipe.new( user )
		recipe.code = code
		recipe.delete_db

		puts "Clearing Sum<br>" if @debug
		r = db.query( "SELECT code FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false )
		db.query( "UPDATE #{$MYSQL_TB_SUM} SET code='', name='', dish=1 WHERE user='#{user.name}';", true ) if r.first['code'] == code
	end
when 'subspecies'
	# Loading original recipe
	if user.status != 7
		recipe = Recipe.new( user )
		recipe.load_db( code, true )

		# Copying phots
		new_media_code = generate_code( user.name, 'p' )
		new_recipe_code = generate_code( user.name, 'r' )

		source_media = Media.new( user )
		source_media.origin = code
		source_media.get_series()

		source_media.series.each do |e|
			FileUtils.cp( "#{$PHOTO_PATH}/#{e}-tns.jpg", "#{$PHOTO_PATH}/#{new_media_code}-tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{e['code']}-tns.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{e}-tn.jpg", "#{$PHOTO_PATH}/#{new_media_code}-tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{e['code']}-tn.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{e}-tn.jpg", "#{$PHOTO_PATH}/#{new_media_code}.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{e['code']}-tn.jpg" )
			
			new_media = Media.new( user )
			new_media.origin = new_recipe_code
			new_media.code = new_media_code
			new_media.date = @datetime
			new_media.base = 'recipe'
			new_media.alt = recipe.name
			new_media.save_db()
		end

		# Insertinbg recipe into DB
		recipe.user.name = user.name
		recipe.code = new_recipe_code
		recipe.favorite = 0
		recipe.public = 0
		recipe.protect = 0
		recipe.draft = 1
		recipe.date = @datetime
		recipe.root = code
		recipe.insert_db
	end

when 'limit'
	page = @cgi['page'].to_i
	page = 1 if page == 0
	page_limit = @cgi['page_limit'].to_i
	range = @cgi['range'].to_i
	type = @cgi['type'].to_i
	role = @cgi['role'].to_i
	tech = @cgi['tech'].to_i
	time = @cgi['time'].to_i
	cost = @cgi['cost'].to_i
	family = @cgi['family'].to_i
	words = @cgi['words']

when 'modal_body'
	page = @cgi['page'].to_i
	recipe = Recipe.new( user )
    recipe.load_db( code, true )

	puts "<table class='table table-borderless'><tr>"

	if user.status >= 1 && recipe.user.name == user.name
		puts "<td align='center' onclick=\"addingMeal( '#{recipe.code}', '#{recipe.name}' )\">#{l['table']}<br><br>#{l['menu']}</td>"
	end

	if user.status >= 2 && recipe.user.name == user.name
		puts "<td align='center' onclick=\"addKoyomi( '#{recipe.code}' )\">#{l['calendar']}<br><br>#{l['koyomi']}</td>"
	end

	puts "<td align='center' onclick=\"print_templateSelect( '#{recipe.code}' )\">#{l['printer']}<br><br>#{l['print']}</td>"

	if user.status >= 1 && recipe.user.name == user.name && ( recipe.root == nil || recipe.root == '' )
		puts "<td align='center' onclick=\"recipeImport( 'subspecies', '#{recipe.code}', '#{page}' )\">#{l['diagram']}<br><br>#{l['daughter']}</td>"
	elsif user.status >= 1 && recipe.user.name == user.name
		puts "<td align='center' onclick=\"initCB( 'load', '#{recipe.root}', '#{recipe.user.name}' )\">#{l['root']}<br><br>#{l['import']}</td>"
	end

	if user.status >= 1 && recipe.user.name == user.name
		puts "<td align='center' onclick=\"cp2words( '#{recipe.code}', '' )\">#{l['cp2words']}<br><br>#{l['pick']}</td>"
	end

	if recipe.user.name == user.name && recipe.protect == 0
		puts "<td align='center' ><input type='checkbox' id='#{recipe.code}'>&nbsp;<span onclick=\"recipeDelete( '#{recipe.code}', #{page} )\">#{l['trash']}</span><br><br>#{l['delete']}</td>"
	end

	puts '</tr></table>'

	exit

when 'modal_label'
	recipe = Recipe.new( user )
    recipe.load_db( code, true )
    puts recipe.name

	exit
end

range = 5 if user.status == 0
if @debug
	puts "page: #{page}<br>"
	puts "range: #{range}<br>"
	puts "type: #{type}<br>"
	puts "role: #{role}<br>"
	puts "tech: #{tech}<br>"
	puts "time: #{time}<br>"
	puts "cost: #{cost}<br>"
	puts "recipe_code_list: #{recipe_code_list}<br>"
	puts "family: #{family}<br>"
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
# 自分のお気に入り
when 1
	sql_where << "user='#{user.name}' AND name!='' AND favorite='1'"
	sql_where_ij << "t1.user='#{user.name}' AND t1.name!='' AND t1.favorite='1'"
# 自分の下書き
when 2
	sql_where << "user='#{user.name}' AND name!='' AND draft='1'"
	sql_where_ij << "t1.user='#{user.name}' AND t1.name!='' AND t1.draft='1'"
# 自分の保護
when 3
	sql_where << "user='#{user.name}' AND protect='1' AND name!=''"
	sql_where_ij << "t1.user='#{user.name}' AND t1.protect='1' AND t1.name!=''"
# 自分の公開
when 4
	sql_where << "user='#{user.name}' AND public='1' AND name!=''"
	sql_where_ij << "t1.user='#{user.name}' AND t1.public='1' AND t1.name!=''"
# 自分の無印
when 5
	sql_where << "user='#{user.name}' AND public='0' AND draft='0' AND name!=''"
	sql_where_ij << "t1.user='#{user.name}' AND t1.public='0' AND t1.draft='0' AND t1.name!=''"
# 他の公開
when 6
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
	res = referencing( words, db, sql_where_ij )
	ref_msg = "#{l['words']}#{words}<br>#{l['norecipe']}" if res.size == 0

	recipe_num = res.size
	offset = ( page - 1 ) * page_limit
	limit = offset + page_limit
else
	r = db.query( "SELECT COUNT(*) FROM #{$MYSQL_TB_RECIPE} #{sql_where};", false )
	recipe_num = r.first['COUNT(*)']

	offset = ( page - 1 ) * page_limit
	res = db.query( "SELECT * FROM #{$MYSQL_TB_RECIPE} #{sql_where} ORDER BY name LIMIT #{offset}, #{page_limit};", false )
end
res.each do |e|
	o = Recipe.new( user )
	o.load_db( e, false )
	o.load_media
	recipes << o
end


puts "Paging parts<br>" if @debug
page_max = recipe_num / page_limit
page_start = 1
page_max += 1 if ( recipe_num % page_limit ) != 0
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


puts "families<br>" if @debug
family_pair = Hash.new
family_recipes = Hash.new
if family == 1
	recipes.each do |e|
		r = db.query( "SELECT code FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}' and root='#{e.code}' ORDER BY name;", false )
		daughters = []
		daughter_recipes = []
		r.each do |ee|
			daughters << ee['code']

			ro = Recipe.new( user )
      		ro.load_db( ee['code'], true )
			daughter_recipes << ro
		end
		if daughters.size > 0
			family_pair[e.code] = daughters
			family_recipes[e.code] = daughter_recipes
		end
	end
end


puts "Recipe HTML parts<br>" if @debug
recipe_html = ''
recipes.each do |e|
	if family == 1
		if e.root == '' && family_pair[e.code] == nil
			recipe_html << recipe_line( e, user, page, 'aliceblue', l )

		elsif family_pair.key?( e.code )
			recipe_html << recipe_line( e, user, page, 'lavender', l )

			family_recipes[e.code].each do |ee|
				recipe_html << recipe_line( ee, user, page, 'snow', l )
			end
		end
	else
		recipe_html << recipe_line( e, user, page, 'aliceblue', l )
	end
end


puts "Page limit HTML parts<br>" if @debug
page_limit_html = ''
nums = [25, 50, 75, 100, 150, 200]
nums.each do |e|
	page_limit_html << "<option value='#{e}' #{$SELECT[ e == page_limit]}>#{e}</option>"
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-6'><h5>#{l['recipel']} <span onclick='recipe3ds()'>#{l['crosshair']}</span> (#{recipe_num}) #{ref_msg}</h5></div>
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
		<div class='col-6'>
			<div class="form-check">
  				<input class="form-check-input" type="checkbox" id="family" #{checked( family )}>
  				<label class='form-check-label'>#{l['family']}</label>
			</div>
		</div>
		<div class='col' align="right">
			<span class="badge rounded-pill npill" type="button" onclick="recipeList( 'reset' )">#{l['reset']}</span>
		</div>
	</div>
	<br>

	<table class="table table-sm table-hover">
		<thead class="table-light">
			<tr>
				<td>#{l['photo']}</td>
				<td>#{l['name']}</td>
				<td></td>
				<td>#{l['status']}</td>
				<td>#{l['com']}</td>
			</tr>
		</thead>
			#{recipe_html}
	</table>

	<div class='row'>
		<div class='col-2'>
			<div class="input-group">
				<label class="input-group-text" for="page_limit">#{l['display']}</label>
				<select class="form-select form-select-sm" id='page_limit'>
					#{page_limit_html}
				</select>
			</div>
		</div>
		<div class='col-5'>
		</div>
		<div class='col-5'>#{html_paging}</div>
	</div>
</div>
HTML

puts html


#==============================================================================
# POST PROCESS
#==============================================================================

#### 検索設定の保存
#words = nil if recipe_code_list.size == 0


recipe_cfg['page'] = page
recipe_cfg['page_limit'] = page_limit

recipe_cfg['range'] = range
recipe_cfg['type'] = type
recipe_cfg['role'] = role
recipe_cfg['tech'] = tech
recipe_cfg['time'] = time
recipe_cfg['cost'] = cost

recipe_cfg['family'] = family
recipe_cfg['words'] = words

recipe_ = JSON.generate( recipe_cfg )
r = db.query( "SELECT * FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false )
if r.first
	db.query( "UPDATE #{$MYSQL_TB_CFG} SET recipe='#{recipe_}' WHERE user='#{user.name}';", true )
else
	db.query( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{user.name}', recipe='#{recipe_}';", true )
end

#==============================================================================
# FRONT SCRIPT START
#==============================================================================
if command == 'init'
	js = <<-"JS"
<script type='text/javascript'>

// Displaying recipe list with narrow down
var recipeListP = function( page ){
	const range = document.getElementById( "range" ).value;
	const type = document.getElementById( "type" ).value;
	const role = document.getElementById( "role" ).value;
	const tech = document.getElementById( "tech" ).value;
	const time = document.getElementById( "time" ).value;
	const cost = document.getElementById( "cost" ).value;
	const words = document.getElementById( "words" ).value;
	const page_limit = document.getElementById( "page_limit" ).value;

	let family = 0;
	if( document.getElementById( "family" ).checked ){ family = 1; }

	$.post( "recipel.cgi", { command:'limit', range:range, type:type, role:role, tech:tech, time:time, cost:cost, page:page, words:words, family:family, page_limit:page_limit }, function( data ){ $( "#L1" ).html( data );});
};


// Displaying recipe list after delete
var recipeDelete = function( code, page ){
	const range = document.getElementById( "range" ).value;
	const type = document.getElementById( "type" ).value;
	const role = document.getElementById( "role" ).value;
	const tech = document.getElementById( "tech" ).value;
	const time = document.getElementById( "time" ).value;
	const cost = document.getElementById( "cost" ).value;
	const page_limit = document.getElementById( "page_limit" ).value;

	let family = 0;
	if( document.getElementById( "family" ).checked ){ family = 1; }

	if( document.getElementById( code ).checked ){
		$.post( "recipel.cgi", { command:'delete', code:code, range:range, type:type, role:role, tech:tech, time:time, cost:cost, page:page, family:family, page_limit:page_limit }, function( data ){
			$.post( "recipel.cgi", { command:'limit', range:range, type:type, role:role, tech:tech, time:time, cost:cost, page:page, family:family, page_limit:page_limit }, function( data ){
				$( "#L1" ).html( data );
				displayVIDEO( 'Removed' );
				$( '#modal_tip' ).modal( 'hide' );
			});
		});
	} else{
		displayVIDEO( 'Check! (>_<)' );
	}
};


// Generationg subSpecies
var recipeImport = function( com, code, page ){
	const range = document.getElementById( "range" ).value;
	const type = document.getElementById( "type" ).value;
	const role = document.getElementById( "role" ).value;
	const tech = document.getElementById( "tech" ).value;
	const time = document.getElementById( "time" ).value;
	const cost = document.getElementById( "cost" ).value;
	const page_limit = document.getElementById( "page_limit" ).value;

	let family = 0;
	if( document.getElementById( "family" ).checked ){ family = 1; }

	$.post( "recipel.cgi", { command:com, code:code, range:range, type:type, role:role, tech:tech, time:time, cost:cost, page:page, family:family, page_limit:page_limit }, function( data ){
		$( "#L1" ).html( data );
		displayVIDEO( 'Recipe has branched' );
		$( '#modal_tip' ).modal( 'hide' );

//		var code_user = data.split( ':' );
//		initCB( 'view', code_user[0], code_user[1] );
	});
};

// Modal Tip for fcz list
var modalTip = function( code ){
	$.post( "#{script}.cgi", { command:'modal_body', code:code }, function( data ){
		$( "#modal_tip_body" ).html( data );
		$.post( "#{script}.cgi", { command:'modal_label', code:code }, function( data ){
			$( "#modal_tip_label" ).html( data );
			$( '#modal_tip' ).modal( 'show' );
		});
	});
}

</script>

JS

	puts js
end
