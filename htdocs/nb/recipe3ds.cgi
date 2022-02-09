#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 recipe 3D plotter 0.05b


#==============================================================================
#LIBRARY
#==============================================================================
require './soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'recipe3ds'
@debug = true


#==============================================================================
#DEFINITION
#==============================================================================

#### 表示範囲
def range_html( range, lp )
	range_select = []
	0.upto( 5 ) do |i|
		if range == i
			range_select[i] = 'SELECTED'
		else
			range_select[i] = ''
		end
	end

	html = lp[22]
	html << '<select class="form-select form-select-sm" id="range">'
	html << "<option value='0' #{range_select[0]}>#{lp[23]}</option>"
	html << "<option value='1' #{range_select[1]}>#{lp[24]}</option>"
	html << "<option value='2' #{range_select[2]}>#{lp[25]}</option>"
	html << "<option value='3' #{range_select[3]}>#{lp[26]}</option>"
	html << "<option value='4' #{range_select[4]}>#{lp[27]}</option>"
	html << "<option value='5' #{range_select[5]}>#{lp[28]}</option>"
	html << '</select>'

	return html
end


#### 料理スタイル生成
def type_html( type, lp )
	html = lp[29]
	html << '<select class="form-select form-select-sm" id="type">'
	html << "<option value='99'>#{lp[23]}</option>"
	@recipe_type.size.times do |c|
		s = ''
		s = 'SELECTED' if type == c
		html << "<option value='#{c}' #{s}>#{@recipe_type[c]}</option>"
	end
	html << '</select>'

	return html
end


#### 献立区分
def role_html( role, lp )
	html = lp[30]
	html << '<select class="form-select form-select-sm" id="role">'
	html << "<option value='99'>#{lp[23]}</option>"
	@recipe_role.size.times do |c|
		s = ''
		s = 'SELECTED' if role == c
		html << "<option value='#{c}' #{s}>#{@recipe_role[c]}</option>"
	end
	s = ''
	s = 'SELECTED' if role == 100
	html << "<option value='100' #{s}>#{lp[19]}</option>"
	html << '</select>'

	return html
end


#### 調理区分
def tech_html( tech, lp )
	html = lp[31]
	html << '<select class="form-select form-select-sm" id="tech">'
	html << "<option value='99'>#{lp[23]}</option>"
	@recipe_tech.size.times do |c|
		s = ''
		s = 'SELECTED' if tech == c
		html << "<option value='#{c}' #{s}>#{@recipe_tech[c]}</option>"
	end
html << '</select>'

	return html
end


#### 目安時間
def time_html( time, lp )
	html = lp[32]
	html << '<select class="form-select form-select-sm" id="time">'
	html << "<option value='99'>#{lp[23]}</option>"
	@recipe_time.size.times do |c|
		s = ''
		s = 'SELECTED' if time == c
		html << "<option value='#{c}' #{s}>#{@recipe_time[c]}</option>"
	end
	html << '</select>'

	return html
end


#### 目安費用
def cost_html( cost, lp )
	html = lp[33]
	html << '<select class="form-select form-select-sm" id="cost">'
	html << "<option value='99'>#{lp[23]}</option>"
	@recipe_cost.size.times do |c|
		s = ''
		s = 'SELECTED' if cost == c
		html << "<option value='#{c}' #{s}>#{@recipe_cost[c]}</option>"
	end
	html << '</select>'

	return html
end


def referencing( words, uname )
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

	# Referencing recipe code
	recipe_code_list = []
	true_query.each do |e|
		if e =~ /\-r\-/
			recipe_code_list << e
		else
			r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPEI} WHERE word='#{e}' AND ( user='#{uname}' OR public='1' );", false, @debug )
			r.each do |ee|
				recipe_code_list << ee['code']
			end
		end
	end
	recipe_code_list.uniq!

	return recipe_code_list
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
#user.debug if @debug
lp = user.load_lp( script )


r = mdb( "SELECT recipe FROM cfg WHERE user='#{user.name}';", false, @debug )
recipe_cfg = Hash.new
recipe_cfg = JSON.parse( r.first['recipe'] ) if r.first['recipe'] != nil && r.first['recipe'] != ''


#### POST
command = @cgi['command']
words = @cgi['words']
if @debug
	puts "command: #{command}<br>"
	puts "words: #{words}<br>"
	puts "<hr>"
end


#### 検索条件設定
page = 1
range = 0
type = 99
role = 99
tech = 99
time = 99
cost = 99
xitem = 'ENERC'
yitem = 'ENERC'
zitem = 'ENERC'
xlog = 0
ylog = 0
zml = 0
zrange = 0
recipe_code_list = []

case command
when 'init'
	range = recipe_cfg['range'].to_i
	type = recipe_cfg['type'].to_i
	role = recipe_cfg['role'].to_i
	tech = recipe_cfg['tech'].to_i
	time = recipe_cfg['time'].to_i
	cost = recipe_cfg['cost'].to_i
	xitem = recipe_cfg['xitem']
	yitem = recipe_cfg['yitem']
	zitem = recipe_cfg['zitem']
	xlog = recipe_cfg['xlog'].to_i
	ylog = recipe_cfg['ylog'].to_i
	zml =  recipe_cfg['zml'].to_i
	zrange =  recipe_cfg['zrange'].to_i
when 'reset'
	words = ''

when 'refer'
	recipe_code_list = referencing( words, user.name ) if words != '' && words != nil
	words = "#{lp[39]}#{words}<br>#{lp[1]}" if recipe_code_list.size == 0
	page = 1

when 'plott_area'
	puts '<div class="row">'
	puts "<div class='col'><div id='recipe3ds_plott' align='center'></div>"
	puts '</div>'

	exit( 0 )
when 'plott_data'
	range = @cgi['range'].to_i
	type = @cgi['type'].to_i
	role = @cgi['role'].to_i
	tech = @cgi['tech'].to_i
	time = @cgi['time'].to_i
	cost = @cgi['cost'].to_i

	xitem = @cgi['xitem']
	xlog = @cgi['xlog'].to_i
	yitem = @cgi['yitem']
	ylog = @cgi['ylog'].to_i
	zitem = @cgi['zitem']
	zml = @cgi['zml'].to_i
	zrange = @cgi['zrange'].to_i
else
	range = @cgi['range'].to_i
	type = @cgi['type'].to_i
	role = @cgi['role'].to_i
	tech = @cgi['tech'].to_i
	time = @cgi['time'].to_i
	cost = @cgi['cost'].to_i

	xitem = @cgi['xitem']
	yitem = @cgi['yitem']
	zitem = @cgi['zitem']
	xlog = @cgi['xlog'].to_i
	ylog = @cgi['ylog'].to_i
	zml = @cgi['zml'].to_i
	zrange = @cgi['zrange'].to_i

	recipe_code_list = referencing( recipe_cfg['words'], user.name )
	words = recipe_cfg['words']
end
if @debug
	puts "range: #{range}<br>"
	puts "type: #{type}<br>"
	puts "role: #{role}<br>"
	puts "tech: #{tech}<br>"
	puts "time: #{time}<br>"
	puts "cost: #{cost}<br>"
	puts "xitem: #{xitem}<br>"
	puts "yitem: #{yitem}<br>"
	puts "zitem: #{zitem}<br>"
	puts "xlog: #{xlog}<br>"
	puts "ylog: #{ylog}<br>"
	puts "zml: #{zml}<br>"
	puts "zrange: #{zrange}<br>"
	puts "recipe_code_list: #{recipe_code_list}<br>"
	puts "<hr>"
end


#### WHERE setting
sql_where = 'WHERE '
case range
# 自分の全て
when 0
	sql_where << "recipe.user='#{user.name}' AND recipe.name!=''"
# 自分の下書き
when 1
	sql_where << "recipe.user='#{user.name}' AND recipe.name!='' AND recipe.draft='1'"
# 自分の保護
when 2
	sql_where << "recipe.user='#{user.name}' AND recipe.protect='1' AND recipe.name!=''"
# 自分の公開
when 3
	sql_where << "recipe.user='#{user.name}' AND recipe.public='1' AND recipe.name!=''"
# 自分の無印
when 4
	sql_where << "recipe.user='#{user.name}' AND recipe.public='0' AND recipe.draft='0' AND recipe.name!=''"
# 他の公開
when 5
	sql_where << "recipe.public='1' AND recipe.user!='#{user.name}' AND recipe.name!=''"
else
	sql_where << "recipe.user='#{user.name}' AND recipe.name!=''"
end

sql_where << " AND recipe.type='#{type}'" unless type == 99
sql_where << " AND recipe.role='#{role}'" unless role == 99
sql_where << " AND recipe.tech='#{tech}'" unless tech == 99
sql_where << " AND recipe.time>0 AND recipe.time<=#{time}" unless time == 99
sql_where << " AND recipe.cost>0 AND recipe.cost<=#{cost}" unless cost == 99


if command == 'plott_data'
	tb1 = "#{$MYSQL_TB_FCZ}"
	tb2 = "#{$MYSQL_TB_RECIPE}"

	q = "SELECT #{tb1}.#{xitem}, #{tb1}.#{yitem}, #{tb1}.#{zitem} FROM #{tb1} INNER JOIN #{tb2} ON #{tb1}.origin=#{tb2}.code #{sql_where} ORDER BY #{tb1}.#{zitem};"
puts q
	r = mdb( q, false, @debug )
	r.each do |e|
		puts "#{e[zitem]}<br>"
	end

	exit( 0 )
end




#### 検索条件HTML
html_range = range_html( range, lp )
html_type = type_html( type, lp )
html_role = role_html( role, lp )
html_tech = tech_html( tech, lp )
html_time = time_html( time, lp )
html_cost = cost_html( cost, lp )


####
xselect = '<select class="form-select" id="xitem">'
@fct_item.each do |e|
	unless e == 'FG' || e == 'FN' || e == 'SID' || e == 'Tagnames' || e == 'REFUSE' || e == 'Notice'
		s = ''
		s = 'SELECTED' if e == xitem
		xselect << "<option value='#{e}' #{s}>#{@fct_name[e]}</option>"
	end
end
xselect << '</select>'

yselect = '<select class="form-select" id="yitem">'
@fct_item.each do |e|
	unless e == 'FG' || e == 'FN' || e == 'SID' || e == 'Tagnames' || e == 'REFUSE' || e == 'Notice'
		s = ''
		s = 'SELECTED' if e == yitem
		yselect << "<option value='#{e}' #{s}>#{@fct_name[e]}</option>"
	end
end
yselect << '</select>'

zselect = '<select class="form-select" id="zitem">'
@fct_item.each do |e|
	unless e == 'FG' || e == 'FN' || e == 'SID' || e == 'Tagnames' || e == 'REFUSE' || e == 'Notice'
		s = ''
		s = 'SELECTED' if e == zitem
		zselect << "<option value='#{e}' #{s}>#{@fct_name[e]}</option>"
	end
end
zselect << '</select>'

zml_select = '<select class="form-select" id="zml">'
if zml == 1
	zml_select << "<option value='1' SELECTED>以下</option>"
else
	zml_select << "<option value='0'>以上</option>"
end
zml_select << '</select>'

xlog_check = ''
ylog_check = 'CHECKED' if xlog == 1

xlog_check = ''
ylog_check = 'CHECKED' if ylog == 1


puts "Control HTML<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'>#{html_range}</div>
		<div class='col'>#{html_type}</div>
		<div class='col'>#{html_role}</div>
		<div class='col'>#{html_tech}</div>
		<div class='col'>#{html_time}</div>
		<div class='col'>#{html_cost}</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-4'>
			<div class="input-group mb-3">
				<label class="input-group-text">X軸成分</label>
				#{xselect}
			</div>
		</div>
		<div class='col-2'>
			<input class="form-check-input mt-0" type="checkbox" id="xlog">&nbsp;対数
		</div>
		<div class='col-4'>
			<div class="input-group mb-3">
				<label class="input-group-text">補助成分</label>
				#{yselect}
			</div>
		</div>
		<div class='col-2'>
			#{zml_select}
		</div>
	</div>
	<div class='row'>
		<div class='col-4'>
			<div class="input-group mb-3">
				<label class="input-group-text">Y軸成分</label>
				#{zselect}
			</div>
		</div>
		<div class='col-2'>
			<input class="form-check-input mt-0" type="checkbox" id="ylog">&nbsp;対数
		</div>
		<div class='col-4'>
			<label class="form-label"></label>
			<input type="range" class="form-range" min="0" max="100" step="5" id="zrange" value='0'>
		</div>
		<div class='col-2'>
			<div class="input-group mb-3">
				<input type="text" class="form-control" value='0' id='zrangev' disabled>
				<span class="input-group-text">%</span>
			</div>
		</div>
	</div>
	<div class='row'>
		<div class='col-3'><button class="btn btn-outline-primary btn-sm" type="button" onclick="recipe3ds_plott()">#{lp[13]}</button></div>
		<div class='col-3'><button class="btn btn-outline-warning btn-sm" type="button" onclick="recipe3dsReset()">#{lp[14]}</button></div>
	</div>
</div>
HTML

puts html

#### 検索設定の保存
recipe_ = JSON.generate( { "page" => page, "range" => range, "type" => type, "role" => role, "tech" => tech, "time" => time, "cost" => cost, "words" => words } )
mdb( "UPDATE #{$MYSQL_TB_CFG} SET recipe='#{recipe_}' WHERE user='#{user.name}';", false, @debug )
