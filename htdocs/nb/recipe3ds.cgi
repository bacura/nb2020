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
		'all' 		=> "全て",\
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
		'range'		=> "表示範囲",\
		'style'		=> "料理スタイル",\
		'time'		=> "表目安時間(分)",\
		'cost'		=> "目安費用(円)",\
		'no_def'	=> "未設定",\
		'all_ns'	=> "全て（ー調%）",\
		'plot_size' => "表示サイズ",\
		'x_log' 	=> "X軸Log",\
		'y_log' 	=> "Y軸Log",\
		'x_zoom' 	=> "X軸Zoom",\
		'y_zoom' 	=> "Y軸Zoom",\
		'more'		=> "以上",\
		'less'		=> "未満",\
		'xcomp'		=> "X成分",\
		'ycomp'		=> "Y成分",\
		'zcomp'		=> "Z成分",\
		'reset'		=> "リセット",\
		'plot'		=> "<img src='bootstrap-dist/icons/crosshair.svg' style='height:1.0em; width:1.0em;'> プ ロ ッ ト",\
		'crosshair' => "<img src='bootstrap-dist/icons/crosshair.svg' style='height:1.0em; width:1.0em;'>"
	}

	return l[language]
end

#### Display range
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

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
db = Db.new( user, @debug, false )

#### POST
command = @cgi['command']
if @debug
	puts "command: #{command}<br>"
	puts "<hr>"
end


#### 検索条件設定
recipe_cfg = Hash.new
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
area_size = 0.6
x_zoom = false
y_log = 'linner'

r = db.query( "SELECT recipe FROM cfg WHERE user='#{user.name}';", false )
begin
	recipe_cfg = JSON.parse( r.first['recipe'] )

	range = recipe_cfg['range'].to_i
	type = recipe_cfg['type'].to_i
	role = recipe_cfg['role'].to_i
	tech = recipe_cfg['tech'].to_i
	time = recipe_cfg['time'].to_i
	cost = recipe_cfg['cost'].to_i

	xitem = recipe_cfg['xitem'].to_s
	yitem = recipe_cfg['yitem'].to_s
	zitem = recipe_cfg['zitem'].to_s
	zml = recipe_cfg['zml'].to_i
	zrange = recipe_cfg['zrange'].to_i

	area_size = recipe_cfg['area_size'].to_f
	x_zoom = recipe_cfg['x_zoom'].to_s
	y_log = recipe_cfg['y_log'].to_s
rescue
end

case command
when 'plott_area'
	area_size_option = ''
	area_size_value = [ 0.8, 0.7, 0.6, 0.5 ]
	area_size_text = %w( Max Large Medium Small )
	4.times do |c|
		area_size_option << "<option value='#{area_size_value[c]}' #{$SELECT[area_size_value[c] == area_size]}>#{area_size_text[c]}</option>"
	end

html = <<-"PLOTT"
	<div class="row">
		<div class='col-2'>
			#{l['plot_size']}<br>
			<select class="form-select form-select-sm" id="area_size" onchange="resize()">
				#{area_size_option}
			</select>
			<br>
			<br>

<!--			<div class="form-check form-switch">
				<label class="form-check-label">#{l['x_log']}</label>
				<input class="form-check-input" type="checkbox" id="x_log" DISABLED>
			</div>
			<br>
			<br>
-->
			<div class="form-check form-switch">
				<label class="form-check-label">#{l['x_zoom']}</label>
				<input class="form-check-input" type="checkbox" id="x_zoom" #{$CHECK[x_zoom=='true']}>
			</div>
			<br>
			<br>

			<div class="form-check form-switch">
				<label class="form-check-label">#{l['y_log']}</label>
				<input class="form-check-input" type="checkbox" id="y_log" #{$CHECK[y_log == 'log']}>
			</div>
			<br>
			<br>
<!--
			<div class="form-check form-switch">
				<label class="form-check-label">#{l['y_zoom']}</label>
				<input class="form-check-input" type="checkbox" id="y_zoom" DISABLED>
			</div>
-->
		</div>
		<div class='col-10'>
			<div id='recipe3ds_plott' align='center'></div>
		</div>
	</div>


PLOTT

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

	area_size = @cgi['area_size'].to_f
	x_zoom = @cgi['x_zoom']
	y_log = @cgi['y_log'].to_s

when 'reset'
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

	area_size = 0.6
	x_zoom = false
	y_log = 'linner'
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

#Z成分カットオフ
if zml == 1
	sql_where << " AND #{zitem}<#{zrange}"
else
	sql_where << " AND #{zitem}>=#{zrange}"
end

sql_where << " AND recipe.tech='#{tech}'" unless tech == 99
sql_where << " AND recipe.time='#{time}'" unless time == 99
sql_where << " AND recipe.cost='#{cost}'" unless cost == 99

case command
when 'plott_area'
when 'plott_data'
	tb1 = "#{$MYSQL_TB_FCZ}"
	tb2 = "#{$MYSQL_TB_RECIPE}"
	xitems = []
	yitems = []
	zitems = []
	names = []
	codes = []

	r = db.query( "SELECT #{tb1}.#{xitem}, #{tb1}.#{yitem}, #{tb1}.#{zitem}, #{tb2}.name, #{tb2}.code FROM #{tb1} INNER JOIN #{tb2} ON #{tb1}.origin=#{tb2}.code #{sql_where};", false )

	if  r.first
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

		ymax = yitems.max
		y_tickv = []
		y_tickv = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0] if ymax < 1
		y_tickv = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] if ymax >= 1
		y_tickv = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100] if ymax >= 10
		y_tickv = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000] if ymax >= 100
		y_tickv = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000] if ymax >= 1000
		y_tickv = [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000] if ymax >= 10000


		label_x = @fct_name[xitem].split( '(' )[0]
		label_x = "#{label_x} (#{@fct_unit[xitem]})" 
		label_y = @fct_name[yitem].split( '(' )[0]
		label_y = "#{label_y} (#{@fct_unit[yitem]})" 
		if label_x == label_y
			label_x = label_x + '_x'
			label_y = label_y + '_y'
		end

		raw = []
		raw[0] = xitems.unshift( label_x ).join( '[]' )
		raw[1] = yitems.unshift( label_y ).join( '[]' )
		raw[2] = names.join( '[]' )
		raw[3] = codes.join( '[]' )
		raw[4] = x_tickv.join( '[]' )
		raw[5] = y_tickv.join( '[]' )

		puts raw.join( '{}' )

	else
		puts '0'
	end


when 'monitor'
#	puts "#{@fct_name[xitem]}： #{xitems.min} ～ #{xitems.max}<br>"
#	puts "#{@fct_name[yitem]}： #{yitems.min} ～ #{yitems.max}<br>"
#	puts "#{@fct_name[zitem]}： #{zitems.min} ～ #{zitems.max}<br>"
#	puts "[#{xitems.size}][#{names.size}][#{codes.size}]<br>"

else
	#### 検索条件HTML
	html_range = range_html( range, l )
	html_type = type_html( type, l )
	html_role = role_html( role, l )
	html_tech = tech_html( tech, l )
	html_time = time_html( time, l )
	html_cost = cost_html( cost, l )

	####
	xselect = '<select class="form-select" id="xitem">'
	@fct_item.each.with_index do |e, i|
		unless e == 'FG' || e == 'FN' || e == 'SID' || e == 'Tagnames' || e == 'REFUSE' || e == 'Notice'
			xselect << "<option value='#{e}' #{$SELECT[e == xitem]}>#{@fct_name[e]}</option>"
		end
	end
	xselect << '</select>'

	yselect = '<select class="form-select" id="yitem">'
	@fct_item.each do |e|
		unless e == 'FG' || e == 'FN' || e == 'SID' || e == 'Tagnames' || e == 'REFUSE' || e == 'Notice'
			yselect << "<option value='#{e}' #{$SELECT[e == yitem]}>#{@fct_name[e]}</option>"
		end
	end
	yselect << '</select>'

	zselect = '<select class="form-select" id="zitem">'
	@fct_item.each do |e|
		unless e == 'FG' || e == 'FN' || e == 'SID' || e == 'Tagnames' || e == 'REFUSE' || e == 'Notice'
			zselect << "<option value='#{e}' #{$SELECT[e == zitem]}>#{@fct_name[e]}</option>"
		end
	end
	zselect << '</select>'

	zml_select = '<select class="form-select" id="zml">'
	zml_select << "<option value='0' >#{l['more']}</option>"
	zml_select << "<option value='1' #{$SELECT[zitem]}>#{l['less']}</option>"
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
			<div class="input-group input-group-sm mb-3">
				<label class="input-group-text">#{l['xcomp']}</label>
				#{xselect}
			</div>
		</div>
		<div class='col-4'>
			<div class="input-group input-group-sm  mb-3">
				<label class="input-group-text">#{l['ycomp']}</label>
				#{yselect}
			</div>
		</div>
		<div class='col-4'>
			<div class="input-group input-group-sm  mb-3">
				<label class="input-group-text">#{l['zcomp']}</label>
				#{zselect}
			</div>
		</div>
	</div>
	<div class='row'>
		<div class='col-8'>
		</div>
		<div class='col-4'>
			<div class="input-group input-group-sm mb-3">
				<input type="number" class="form-control" min="0" value='0' id='zrange'>
				#{zml_select}
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

end

puts html

#==============================================================================
#POST PROCESS
#==============================================================================

if command == 'monitor'
	#### 検索設定の保存
	recipe_cfg['range'] = range
	recipe_cfg['type'] = type
	recipe_cfg['role'] = role
	recipe_cfg['tech'] = tech
	recipe_cfg['time'] = time
	recipe_cfg['cost'] = cost

	recipe_cfg['xitem'] = xitem
	recipe_cfg['yitem'] = yitem
	recipe_cfg['zitem'] = zitem
	recipe_cfg['zml'] = zml
	recipe_cfg['zrange'] = zrange

	recipe_cfg['area_size'] = area_size
	recipe_cfg['x_zoom'] = x_zoom
	recipe_cfg['y_log'] = y_log

	recipe_ = JSON.generate( recipe_cfg )
	r = db.query( "SELECT recipe FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false )
	if r.first
		db.query( "UPDATE #{$MYSQL_TB_CFG} SET recipe='#{recipe_}' WHERE user='#{user.name}';", true )
	else
		db.query( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{user.name}', recipe='#{recipe_}';", true )
	end
end

#==============================================================================
#FRONT SCRIPT
#==============================================================================

if command == 'init'

	js = <<-"JS"
<script type='text/javascript'>

// Dosplaying recipe by scatter plott
var recipe3dsPlottDraw = function(){
	const range = document.getElementById( "range" ).value;
	const type = document.getElementById( "type" ).value;
	const role = document.getElementById( "role" ).value;
	const tech = document.getElementById( "tech" ).value;
	const time = document.getElementById( "time" ).value;
	const cost = document.getElementById( "cost" ).value;

	const xitem = document.getElementById( "xitem" ).value;
	const yitem = document.getElementById( "yitem" ).value;
	const zitem = document.getElementById( "zitem" ).value;
	const zml = document.getElementById( "zml" ).value;
	const zrange = document.getElementById( "zrange" ).value;

	const area_size = document.getElementById( "area_size" ).value;
	if( document.getElementById( "x_zoom" ).checked ){ var x_zoom = true; }else{ var x_zoom = false; }
	if( document.getElementById( "y_log" ).checked ){ var y_log = 'log'; }else{ var y_log = 'linear'; }

	$.post( "recipe3ds.cgi", { command:'monitor', range:range, type:type, role:role, tech:tech, time:time, cost:cost,
		xitem:xitem, yitem:yitem, zitem:zitem, zml:zml, zrange:zrange, area_size:area_size, x_zoom:x_zoom, y_log:y_log }, function( data ){
		$( "#L3" ).html( data );
	});

	$.post( "recipe3ds.cgi", { command:'plott_data', range:range, type:type, role:role, tech:tech, time:time, cost:cost,
		xitem:xitem, yitem:yitem, zitem:zitem, zml:zml, zrange:zrange, area_size:area_size, x_zoom:x_zoom, y_log:y_log }, function( raw ){

		if( raw == 0 ){
			displayVIDEO( 'No match found' );
			return;
		}

		const column = ( String( raw )).split( '{}' );
		const x_values = ( String( column[0] )).split('[]');
		const y_values = ( String( column[1] )).split('[]');
		const names = ( String( column[2] )).split('[]');
		const codes = ( String( column[3] )).split('[]');
		const x_tickv = ( String( column[4] )).split('[]');
		const y_tickv = ( String( column[5] )).split('[]');

		const plott_size = document.documentElement.clientWidth
		const frame_rate = document.getElementById( "area_size" ).value;

		if ( window.chart_recipe3d != null ){
			window.chart_recipe3d.destroy();
			displayVIDEO( 'Flush!' );
		}

		window.chart_recipe3d = c3.generate({
			bindto: '#recipe3ds_plott',
			size:{ width: plott_size * frame_rate, height: plott_size * frame_rate },

			data: {
				columns: [
					x_values,	// x軸
					y_values,	// y軸
				],
			    x: x_values[0],
				type: 'scatter',
				onclick: function ( d ) {
					searchDR( codes[d['index']] );
                }
//				colors:{ x_values[0]: '#ff44FF' }
			},
			axis: {
			    x: {
			    	type: 'linear',
			    	label: x_values[0],
			    	min:0,
					tick: {
						fit: true,
						count: 10,
						format: d3.format( "01d" ),
						values: x_tickv
					},
					padding: { left: 0, right: 10 }
				},
			    y: {
			    	label: y_values[0],
			    	type: y_log,
			    	min: 0,
					tick: {
						fit: true,
						count: 10,
						format: d3.format( "01d" ),
						values: y_tickv
					},
			  		padding: { top: 10, bottom: 0 }
			    }
			},
			zoom: { enabled: x_zoom },
			point: {
				r: 8,
				focus: { expand: { r: 10 }}
			 },
			grid: {
     			x: { show: true },
        		y: { show: true }
            },
			legend: { show: false },
			tooltip: {
				grouped: false,
				contents: function ( d, defaultTitleFormat, defaultValueFormat, color ) {
					var tooltip_html = '<table style="background-color:#ffffff; font-size:1.5em;">';
					tooltip_html += '<tr><td colspan="2"  style="background-color:mistyrose;">' + names[d[0].index] + '</td></tr>'
					tooltip_html += '<tr><td>' + x_values[0] + '</td><td>: ' + d[0].x + '</td></tr>'
					tooltip_html += '<tr><td>' + y_values[0] + '</td><td>: ' + d[0].value + '</td></tr>'
					tooltip_html += '</table>'

					return tooltip_html;
				}
			},
		});
	});
};


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

// Dosplaying recipe by scatter plott
var resize = function(){
	const plott_size = document.documentElement.clientWidth
	const frame_rate = document.getElementById( "area_size" ).value;

	window.chart_recipe3d.resize({
		height: plott_size * frame_rate,
		width: plott_size * frame_rate
	});
};

$( document ).ready( function(){
	recipe3dsPlottDraw();
});


JS

	puts js 
end
