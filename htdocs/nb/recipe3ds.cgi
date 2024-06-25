#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 recipe 3D plotter 0.0.0 (2024/06/18)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )


#==============================================================================
#LIBRARY
#==============================================================================
require './soul'


#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'plot_size' => "プロットサイズ",\
		'y_log' 	=> "Y軸Log",\
		'dsp_label'	=> "ラベル表示",\
		'plot'		=> "プ ロ ッ ト",\
		'more'		=> "以上",\
		'less'		=> "以下",\
		'xcomp'		=> "X軸成分",\
		'ycomp'		=> "y軸成分",\
		'zcomp'		=> "z軸成分",\
		'range'		=> "表示範囲",\
		'style'		=> "料理スタイル",\
		'role'		=> "献立区分",\
		'tech'		=> "調理区分",\
		'time'		=> "表目安時間(分)",\
		'cost'		=> "目安費用(円)",\
		'all'		=> "全て",\
		'draft'		=> "下書き",\
		'protect'	=> "保護",\
		'public'	=> "公開",\
		'no_mark'	=> "無印",\
		'public_'	=> "公開(他ユーザー)",\
		'no_def'	=> "未設定",\
		'all_ns'	=> "全て（調味系除く）",\
		'chomi'		=> "[ 調味％ ]",\
		'reset'		=> "リセット"
	}

	return l[language]
end


#### Display range
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
	html << "<option value='4' #{range_select[4]}>#{l['no_mark']}</option>"
	html << "<option value='5' #{range_select[5]}>#{l['public_']}</option>"
	html << '</select>'

	return html
end


#### 料理スタイル生成
def type_html( type, l )
	html = l['style']
	html << '<select class="form-select form-select-sm" id="type">'
	html << "<option value='99'>#{l['no_def']}</option>"
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
	html << "<option value='99'>#{l['all_ns']}</option>"
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
	html << "<option value='99'>#{l['no_def']}</option>"
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
	html << "<option value='99'>#{l['no_def']}</option>"
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
	html << "<option value='99'>#{l['no_def']}</option>"
	@recipe_cost.size.times do |c|
		s = ''
		s = 'SELECTED' if cost == c
		html << "<option value='#{c}' #{s}>#{@recipe_cost[c]}</option>"
	end
	html << '</select>'

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

r = db.query( "SELECT recipe3ds FROM cfg WHERE user='#{user.name}';", false )
recipe3ds_cfg = Hash.new
recipe3ds_cfg = JSON.parse( r.first['recipe3ds'] ) if r.first['recipe3ds'] != nil && r.first['recipe3ds'] != ''


#### POST
command = @cgi['command']
if @debug
	puts "command: #{command}<br>"
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
zml = 0
zrange = 0


case command
when 'plott_area'

	html = <<-"HTML"
<div class="row">
	<div class='col-1'>
		#{l['plot_size']}<br>
		<select class="form-select form-select-sm" id="frame_size">
			<option value='0.5'>50%</option>
			<option value='0.7'>70%</option>
			<option value='0.9'>90%</option>
		</select>
		<br>
		<div class="form-check form-switch">
			<label class="form-check-label">#{l['y_log']}</label>
			<input class="form-check-input" type="checkbox" id="y_log">
		</div>
		<br>
		<div class="form-check form-switch">
			<label class="form-check-label">#{l['dsp_label']}</label>
			<input class="form-check-input" type="checkbox" id="label_on">
		</div>
	</div>
	<div class='col'><div id='recipe3ds_plott' align='center'></div>
</div>

HTML

	puts html
	exit( 0 )
when 'plott_data', 'monitor'
	range = @cgi['range'].to_i
	type = @cgi['type'].to_i
	role = @cgi['role'].to_i
	tech = @cgi['tech'].to_i
	time = @cgi['time'].to_i
	cost = @cgi['cost'].to_i

	xitem = @cgi['xitem']
	yitem = @cgi['yitem']
	zitem = @cgi['zitem']
	zml = @cgi['zml'].to_i
	zrange = @cgi['zrange'].to_i
else
	range = recipe3ds_cfg['range'].to_i
	type = recipe3ds_cfg['type'].to_i
	role = recipe3ds_cfg['role'].to_i
	tech = recipe3ds_cfg['tech'].to_i
	time = recipe3ds_cfg['time'].to_i
	cost = recipe3ds_cfg['cost'].to_i
	xitem = recipe3ds_cfg['xitem']
	yitem = recipe3ds_cfg['yitem']
	zitem = recipe3ds_cfg['zitem']
	zml =  recipe3ds_cfg['zml'].to_i
	zrange =  recipe3ds_cfg['zrange'].to_i
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
	puts "zml: #{zml}<br>"
	puts "zrange: #{zrange}<br>"
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

if role == 99
	sql_where << " AND recipe.role!='100' AND recipe.role!='7'"
else
	sql_where << " AND recipe.role='#{role}'"
end

sql_where << " AND recipe.tech='#{tech}'" unless tech == 99
sql_where << " AND recipe.time='#{time}'" unless time == 99
sql_where << " AND recipe.cost='#{cost}'" unless cost == 99


if command == 'plott_data' || command == 'monitor'
	tb1 = "#{$MYSQL_TB_FCZ}"
	tb2 = "#{$MYSQL_TB_RECIPE}"
	xitems = []
	yitems = []
	zitems = []
	names = []
	codes = []

	q = "SELECT #{tb1}.#{xitem}, #{tb1}.#{yitem}, #{tb1}.#{zitem}, #{tb2}.name, #{tb2}.code FROM #{tb1} INNER JOIN #{tb2} ON #{tb1}.origin=#{tb2}.code #{sql_where} ORDER BY #{tb1}.#{zitem};"

	r = db.query( q, false )
	r.each do |e|
		xt = e[xitem]
		yt = e[yitem]
		zt = e[zitem]
		xt = 0 if xt == nil
		yt = 0 if yt == nil
		zt = 0 if zt == nil
		xitems << xt.to_f
		yitems << yt.to_f
		zitems << zt.to_f
		nt = e['name']
		nt.gsub!( '(', '（')
		nt.gsub!( ')', '）')
		nt.gsub!( ':', '：')
		names << nt
		codes << e['code']
	end

	xmax = xitems.max
	x_tickv = []
	x_tickv = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0] if xmax < 1
	x_tickv = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] if xmax >= 1
	x_tickv = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100] if xmax >= 10
	x_tickv = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000] if xmax >= 100
	x_tickv = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000] if xmax >= 1000
	x_tickv = [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000] if xmax >= 10000

	if command == 'plott_data' || @debug
		raw = []
		raw[0] = xitems.unshift( @fct_name[xitem] ).join( ',' )
		raw[1] = yitems.unshift( @fct_name[yitem] ).join( ',' )
		raw[2] = names.join( ',' )
		raw[3] = codes.join( ',' )
		raw[4] = x_tickv.join( ',' )
		puts raw.join( ':' )

		exit( 0 ) if command == 'plott_data'
	end

	puts "#{@fct_name[xitem]}： #{xitems.min} ～ #{xitems.max}<br>"
	puts "#{@fct_name[yitem]}： #{yitems.min} ～ #{yitems.max}<br>"
	puts "#{@fct_name[zitem]}： #{zitems.min} ～ #{zitems.max}<br>"
	puts "[#{xitems.size}][#{names.size}][#{codes.size}]<br>"

	#### 検索設定の保存
	recipe_ = JSON.generate( { "range" => range, "type" => type, "role" => role, "tech" => tech, "time" => time, "cost" => cost, "xitem" => xitem, "yitem" => yitem, "zitem" => zitem, "zml" => zml, "zrange" => zrange } )
	db.query( "UPDATE #{$MYSQL_TB_CFG} SET recipe3ds='#{recipe_}' WHERE user='#{user.name}';", true )

	exit( 0 )
end


#### 検索条件HTML
html_range = range_html( range, l )
html_type = type_html( type, l )
html_role = role_html( role, l )
html_tech = tech_html( tech, l )
html_time = time_html( time, l )
html_cost = cost_html( cost, l )


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
s = []
s[zml] = 'SELECTED'
zml_select << "<option value='0' #{s[0]}>#{l['more']}</option>"
zml_select << "<option value='1' #{s[1]}>#{l['less']}</option>"
zml_select << '</select>'


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
				<label class="input-group-text">#{l['xcomp']}</label>
				#{xselect}
			</div>
		</div>
		<div class='col-2'>
		</div>
		<div class='col-4'>
			<div class="input-group mb-3">
				<label class="input-group-text">#{l['zcomp']}</label>
				#{zselect}
			</div>
		</div>
		<div class='col-2'>
			#{zml_select}
		</div>
	</div>
	<div class='row'>
		<div class='col-4'>
			<div class="input-group mb-3">
				<label class="input-group-text">#{l['ycomp']}</label>
				#{yselect}
			</div>
		</div>
		<div class='col-2'>
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
		<button class="btn btn-info btn-sm" type="button" onclick="recipe3dsPlottDraw()">#{l['plot']}</button>
	</div>
	<br>
	<div class='row'>
		<div class='col-12' align="right"><span class="badge rounded-pill npill" type="button" onclick="recipe3dsReset()">#{l['reset']}</span></div>
	</div>
</div>
HTML

puts html

#==============================================================================
#POST PROCESS
#==============================================================================


#==============================================================================
#FRONT SCRIPT
#==============================================================================

if command == 'init'
	js = <<-"JS"
<script type='text/javascript'>


// Dosplaying recipe by scatter plott
var recipe3dsReset = function(){
	document.getElementById( "range" ).value = 0;
	document.getElementById( "type" ).value = 99;
	document.getElementById( "role" ).value = 99;
	document.getElementById( "tech" ).value = 99;
	document.getElementById( "time" ).value = 99;
	document.getElementById( "cost" ).value = 99;

	document.getElementById( "xitem" ).value = 'ENERC';
	document.getElementById( "yitem" ).value = 'ENERC';

	document.getElementById( "zitem" ).value = 'ENERC';
	document.getElementById( "zml" ).value = 0;
	document.getElementById( "zrange" ).value = 0;
};

JS

	puts js 
end
