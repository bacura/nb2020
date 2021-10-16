# Weight module for Physique 0.00b
#encoding: utf-8

require 'time'

@module = 'weight'

def physique_module( cgi, user, debug )
	lp = module_lp( user.language )
	persed_today = Time.parse( $DATE )

	#importing from config
	res = mdb( "SELECT * FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, debug )
	birth = res.first['birth']
	sex = res.first['sex'].to_i
	weight = res.first['weight'].to_f
	height = res.first['height'].to_f
	age = ( Date.today.strftime( "%Y%m%d" ).to_i - birth.strftime( "%Y%m%d" ).to_i ) / 10000

	html = ''
	case cgi['step']
	when 'form'
		module_js()

		start_date = $DATE
		pal = 1.50


		eenergy = calc_energy( weight, height, age, sex, pal )

		res = mdb( "SELECT json FROM #{$MYSQL_TB_MODJ} WHERE user='#{user.name}' and module='#{@module}';", false, debug )
		if res.first
			mod_cfg_h = JSON.parse( res.first['json'] )
			start_date = mod_cfg_h[@module]['start_date']
			pal = mod_cfg_h[@module]['pal'].to_f
			eenergy = mod_cfg_h[@module]['eenergy'].to_i
		end

		sex_ = [lp[1], lp[2]]
		female_selected = ''
		female_selected = 'SELECTED ' if sex == 1

html = <<-"HTML"
		<div class='row'>
		<h5>#{lp[3]}</h5>
		</div>

		<div class='row'>
		<div class='col-6'>
		<table class='table table-sm'>
			<thead><th></th><th>#{lp[4]}</th><th>#{lp[5]}</th><th>#{lp[6]}</th><th>#{lp[7]}</th></thead>
			<tr><td></td><td>#{sex_[sex]}</td><td>#{age}</td><td>#{height}</td><td>#{weight}</td></tr>
		</table>
		</div>
		</div>

		<div class='row'>
			<div class='col-3'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>#{lp[8]}</span>
					<input type='date' class='form-control' id='start_date' value='#{start_date}'>
				</div>
			</div>
			<div class='col-3'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">#{lp[9]}</label>
					<input type='number' min='0.5' max='2.5' step='0.01' class='form-control' id='pal' value='#{pal}'>
				</div>
			</div>

			<div class='col-3'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>#{lp[10]}</span>
					<input type='number' class='form-control' id='eenergy' min='0' value='#{eenergy}'>
				</div>
			</div>
			<div class='col-2' align="right">
				<button class='btn btn-sm btn-primary' onclick="drawChart()">#{lp[11]}</button>
			</div>
		</div>
HTML
	when 'raw'
		start_date = cgi['start_date']
		pal = cgi['pal'].to_f
		eenergy = cgi['eenergy'].to_i

		json = JSON.generate( { @module => { "start_date" => start_date, "pal" => pal, "eenergy" => eenergy }} )
		res = mdb( "SELECT module FROM #{$MYSQL_TB_MODJ} WHERE user='#{user.name}' AND module='#{@module}';", false, debug )
		if res.first
			mdb( "UPDATE #{$MYSQL_TB_MODJ} SET json='#{json}' WHERE user='#{user.name}' AND module='#{@module}';", false, debug )
		else
			mdb( "INSERT INTO #{$MYSQL_TB_MODJ} SET json='#{json}', user='#{user.name}', module='#{@module}';", false, debug )
		end

		# X axis
		x_day = []
		0.upto( 95 ) do |c| x_day[c] = c end

		#Koyomiex config
		puts "Loading config<br>" if @debug
		weight_kex = 0
		denergy_kex = 0
		r = mdb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
		if r.first
			a = r.first['koyomiex'].split( ':' )
			a.size.times do |c|
				aa = a[c].split( "\t" )
 				weight_kex = c if aa[0] == '3'
				denergy_kex = c if aa[0] == '9'
			end
		end

		# measured weight & delta energy
		measured = []
		denergy = []
		persed_date = Time.parse( start_date )
		0.upto( 95 ) do |c|
			break if persed_date > persed_today
			target_date = persed_date.strftime( "%Y-%m-%d" )
			r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND date='#{target_date}';", false, @debug )
			if r.first
				measured[c] = r.first["item#{weight_kex}"].to_f
				denergy[c] = ( r.first["item#{denergy_kex}"].to_i ) * -1
			else
				measured[c] = nil
				denergy[c] = 0
			end
			persed_date += 86400
		end

		#Day 4 stable weight
		d4sw = []
		persed_date = Time.parse( start_date ) + 86400
		pre_measured = measured[0]
		d4sw[0] = measured[0]
		1.upto( 96 ) do |c|
			break if persed_date > persed_today
			measured[c] = pre_measured if measured[c] == nil
			case c
			when 1
				d4sw[1] = ( measured[1] + ( measured[0] / 2 )) / 1.5
			when 2
				d4sw[2] = ( measured[2] + ( measured[1] / 2 ) + ( measured[0] / 4 )) / 1.75
			else
				d4sw[c] = ( measured[c] + ( measured[c-1] / 2 ) + ( measured[c-2] / 4 ) + ( measured[c-3] / 8 )) / 1.875
			end
			pre_measured = measured[c]
			persed_date += 86400
		end
		d4sw.map! do |x| x.round( 1 ) end

		#Intake enargy
		ienergy = []
		persed_date = Time.parse( start_date )
		0.upto( 95 ) do |c|
			break if persed_date > persed_today
			target_date = persed_date.strftime( "%Y-%m-%d" )
			res_koyomi = mdb( "SELECT fzcode FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND freeze=1 AND tdiv!=4 AND date='#{target_date}';", false, debug )
			if res_koyomi.first
				res_fcz = mdb( "SELECT ENERC_KCAL FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND code='#{res_koyomi.first['fzcode']}';", false, debug )
				if res_fcz.first
					ienergy[c] = res_fcz.first['ENERC_KCAL'].to_i
				else
					ienergy[c] = 0
				end
			else
				ienergy[c] = 0
			end
			persed_date += 86400
		end

		#Actual enargy
		aenergy = []
		persed_date = Time.parse( start_date )
		0.upto( 95 ) do |c|
			break if persed_date > persed_today
			if ienergy[c] == nil
				aenergy[c] = denergy[c]
			else
				aenergy[c] = ienergy[c] + denergy[c]
			end
			persed_date += 86400
		end

		#Guide weight
		guide = []
		guide[0] = measured[0]
		guide[0] = weight if measured[0] == nil
		1.upto( 95 ) do |c|
			cenergy = calc_energy( guide[c-1], height, age, sex, pal )
			guide[c] = ( guide[0] - (( cenergy.to_f - eenergy.to_f ) / 7200 * c ))
		end
		guide.map! do |x| x.round( 1 ) end

		#Theoletical weight
		theoletic = []
		theoletic[0] = measured[0]
		theoletic[0] = weight if measured[0] == nil
		persed_date = Time.parse( start_date ) + 86400
		1.upto( 95 ) do |c|
			break if persed_date > persed_today
			cenergy = calc_energy( theoletic[c-1], height, age, sex, pal )
			theoletic[c] = ( theoletic[c-1] - (( cenergy.to_f - aenergy[c] ) / 7200 ))
			persed_date += 86400
		end
		theoletic.map! do |x| x.round( 1 ) end




		raw = []
		raw[0] = x_day.unshift( 'x_day' ).join( ',' )
		raw[1] = guide.unshift( 'ガイド体重' ).join( ',' )
		raw[2] = theoletic.unshift('理論体重').join( ',' )
		raw[3] = d4sw.unshift( 'D4安定体重' ).join( ',' )
		raw[4] = ienergy.unshift( '摂取エネルギー' ).join( ',' )
		raw[5] = denergy.unshift( 'Δ消費エネルギー' ).join( ',' )
		raw[6] = aenergy.unshift( '実エネルギー' ).join( ',' )
		puts raw.join( ':' )
		exit

	when 'chart'
		html = '<div class="row">'
		html << '<div class="col-1"></div>'
		html << '<div class="col-10"><div id="physique_weight_chart" align="center"></div></div>'
		html << '<div class="col-1"></div>'
		html << '</div>'
	end

	return html
end


def calc_energy( weight, height, age, sex, pal )
	result = 0
	if sex == 0
		result = (( 0.0481 * weight + 0.0234 * height - 0.0138 * age - 0.4235 ) * 1000 / 4.186 )
	else
		result = (( 0.0481 * weight + 0.0234 * height - 0.0138 * age - 0.9708 ) * 1000 / 4.186 )
	end
	eer_result = ( result * pal )

	return eer_result
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

var drawChart = function(){
	dl2 = true;
//	dl3 = true;
	displayBW();

	var start_date = document.getElementById( "start_date" ).value;
	var pal = document.getElementById( "pal" ).value;
	var eenergy = document.getElementById( "eenergy" ).value;

//	$.post( "physique.cgi", { mod:'weight', step:'raw', start_date:start_date, pal:pal, eenergy:eenergy }, function( data ){ $( "#L3" ).html( data );});
	$.post( "physique.cgi", { mod:'weight', step:'raw', start_date:start_date, pal:pal, eenergy:eenergy }, function( raw ){

		var column = raw.split( ':' );
		var chart = c3.generate({
			bindto: '#physique_weight_chart',
			size: { width: 960, height: 450 },

			data: {
				columns: [
					column[0].split(','),	// x_day
					column[1].split(','),	// ガイド体重
					column[2].split(','),	// 理論体重
					column[3].split(','),	// D4安定体重
					column[4].split(','),	// 摂取エネルギー
					column[5].split(','), 	// Δ消費エネルギー
					column[6].split(',') 	// 実エネルギー
				],
				x: 'x_day',
				axes: {
					摂取エネルギー: 'y2',
					Δ消費エネルギー: 'y2',
					実エネルギー: 'y2'
				},
				labels: false,
				type : 'line',
				types: { 摂取エネルギー: 'area-step', Δ消費エネルギー: 'area-step', 実エネルギー: 'area-step' },
				colors: {
					ガイド体重: '#d3d3d3',
					理論体重: '#228b22',
					D4安定体重: '#dc143c',
					摂取エネルギー: '#ffd700',
					Δ消費エネルギー: '#00ffff',
					実エネルギー: '#d2691e'
				},
				regions: {
					ガイド体重: { 'start':0, 'style':'dashed' }
				}
			},

			axis: {
		    	x: {
		    		type: 'indexed',
					label: { text: '経過日数', position: 'outer-center' }
				},
				y: {
		    		type: 'linear',
					label: { text: '体重 (kg)', position: 'outer-middle' }
				},
				y2: {
					show: true,
		    		type: 'linear',
		    		max: 4000,
					label: { text: 'エネルギー (kcal)', position: 'outer-middle' }
				}
			},

			legend: {
				show: true,
				position: 'right'
			},

			bar: { width: { ratio: 1.0 }},
			point: { show: true, r: 2 }
		});
	});
};
</script>
JS
	puts js
end


def module_lp( language )
	mlp = Hash.new
	mlp['jp'] = []
	mlp['jp'][1] = "男性"
	mlp['jp'][2] = "女性"
	mlp['jp'][3] = "体重管理"
	mlp['jp'][4] = "代謝的性別"
	mlp['jp'][5] = "年齢"
	mlp['jp'][6] = "身長（cm）"
	mlp['jp'][7] = "初期体重（kg）"
	mlp['jp'][8] = "開始日"
	mlp['jp'][9] = "身体活動レベル"
	mlp['jp'][10] = "予定エネルギー（kcal）"
	mlp['jp'][11] = "チャート描画・更新"

	return mlp[language]
end