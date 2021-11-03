# Weight keep module for Physique 0.00b
#encoding: utf-8

require 'time'

@module = 'weight-keep'

def physique_module( cgi, user, debug )
	lp = module_lp( user.language )
	persed_today = Time.parse( $DATE )

	#importing from config
	r = mdb( "SELECT bio FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, debug )
	if r.first
		if r.first['bio'] != nil && r.first['bio'] != ''
			bio = JSON.parse( r.first['bio'] )
			sex = bio['sex'].to_i
			birth = Time.parse( bio['birth'] )
			height = bio['height'].to_f * 100
			weight = bio['weight'].to_f
			kexow = bio['kexow'].to_i
			pgene = bio['pgene'].to_i
			age = ( Date.today.strftime( "%Y%m%d" ).to_i - birth.strftime( "%Y%m%d" ).to_i ) / 10000
		end
	end

	html = ''
	case cgi['step']
	when 'form'
		module_js( lp )

		start_date = $DATE
		pal = 1.50

		res = mdb( "SELECT json FROM #{$MYSQL_TB_MODJ} WHERE user='#{user.name}' and module='#{@module}';", false, debug )
		if res.first
			mod_cfg_h = JSON.parse( res.first['json'] )
			start_date = mod_cfg_h[@module]['start_date']
			pal = mod_cfg_h[@module]['pal'].to_f
		end

		sex_ = [lp[1], lp[2]]
		female_selected = ''
		female_selected = 'SELECTED ' if sex == 1

html = <<-"HTML"
		<div class='row'>
			<div class='col-11'><h5>#{lp[3]}</h5></div>
			<div class="col-1">#{lp[110]}</div>
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
					<input type='date' class='form-control' id='start_date' value='#{start_date}' onchange='drawChart()'>
				</div>
			</div>
			<div class='col-3'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">#{lp[9]}</label>
					<input type='number' min='0.5' max='2.5' step='0.01' class='form-control' id='pal' value='#{pal}' onchange='drawChart()'>
				</div>
			</div>
		</div>
HTML
	when 'raw'
		start_date = cgi['start_date']
		pal = cgi['pal'].to_f

		json = JSON.generate( { @module => { "start_date" => start_date, "pal" => pal }} )
		res = mdb( "SELECT module FROM #{$MYSQL_TB_MODJ} WHERE user='#{user.name}' AND module='#{@module}';", false, debug )
		if res.first
			mdb( "UPDATE #{$MYSQL_TB_MODJ} SET json='#{json}' WHERE user='#{user.name}' AND module='#{@module}';", false, debug )
		else
			mdb( "INSERT INTO #{$MYSQL_TB_MODJ} SET json='#{json}', user='#{user.name}', module='#{@module}';", false, debug )
		end

		# X axis
		x_day = []
		persed_date = Time.parse( start_date )
		while persed_date <= persed_today do
			x_day << persed_date.strftime( "%Y-%m-%d" )
			persed_date += 86400
		end

		#Koyomiex config
		puts "Loading config<br>" if @debug
		weight_kex = -1
		bfr_kex = -1
		r = mdb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
		if r.first
			a = r.first['koyomiex'].split( ':' )
			a.size.times do |c|
				aa = a[c].split( "\t" )
 				weight_kex = c if aa[0] == '3'
				bfr_kex = c if aa[0] == '5'
			end
		end


		# measured weight & body fat tate
		measured_weight = []
		bfr = []
		recent_weight = 0.0
		persed_date = Time.parse( start_date )
		while persed_date <= persed_today do
			target_date = persed_date.strftime( "%Y-%m-%d" )
			r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND date='#{target_date}';", false, @debug )
			if r.first
				if weight_kex >= 0
					measured_weight << r.first["item#{weight_kex}"].to_f
					recent_weight = r.first["item#{weight_kex}"].to_f if r.first["item#{weight_kex}"].to_f != 0
				else
					measured_weight << 'NA'
				end
				if bfr_kex >= 0
					bfr << r.first["item#{bfr_kex}"].to_f
				else
					bfr << 'NA'
				end
			else
				measured_weight << 'NA'
				bfr << 'NA'
			end
			persed_date += 86400
		end

		delta_weight = recent_weight - weight
		delta_energy = 0.0
		if delta_weight > 0
			if delta_weight > 1
				delta_energy = -7200 / 24
			else
				delta_energy = - delta_weight * 7200 / 24
			end
		else
			if delta_weight < -1
				delta_energy = 7200 /24
			else
				delta_energy = delta_weight * 7200 / 24
			end
		end
		m_energy = calc_energy( recent_weight, height, age, sex, pal ) + delta_energy
		m_energy -= 200 if pgene == 1

		raw = []
		raw[0] = x_day.unshift( 'x_day' ).join( ',' )
		raw[1] = measured_weight.unshift( lp[100] ).join( ',' )
		raw[2] = bfr.unshift( lp[101] ).join( ',' )
		raw[9] = m_energy.to_i

		puts raw.join( ':' )
		exit

	when 'chart'
		html = '<div class="row">'
		html << "<div class='col-9'><div id='physique_#{@module}-chart' align='center'></div></div>"
		html << "<div class='col-3'><div id='physique_#{@module}-chart-sub' align='center'></div>"
		html << '</div>'

	when 'notice'
		html << '<div class="row">'
		html << '<div class="col-3">'
		html << "<div class='input-group input-group-sm'>"
		html << "  <span class='input-group-text'>#{lp[11]}</span>"
		html << "  <input type='text' class='form-control form-control-sm' id='menergy' value='' DISABLED>"
		html << "</div>"
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


def module_js( lp )
	js = <<-"JS"
<script type='text/javascript'>

var drawChart = function(){
	dl3 = true;
	displayBW();

	var start_date = document.getElementById( "start_date" ).value;
	var pal = document.getElementById( "pal" ).value;

	$.post( "physique.cgi", { mod:'#{@module}', step:'notice' }, function( data ){ $( "#L3" ).html( data );});
	$.post( "physique.cgi", { mod:'#{@module}', step:'raw', start_date:start_date, pal:pal }, function( raw ){

		var column = ( String( raw )).split( ':' );
		var x_day = ( String( column[0] )).split(',');
		var y_weight = ( String( column[1] )).split(',');
		var y_bfr = ( String( column[2] )).split(',');

		var chart = c3.generate({
			bindto: '#physique_#{@module}-chart',

			data: {
				columns: [
					x_day,
					y_weight,
					y_bfr
				],
				x: 'x_day',
				axes: {
					#{lp[101]}: 'y2',
				},
				labels: false,
				type : 'line',
				colors: {
					#{lp[100]}: '#dc143c',
					#{lp[101]}: '#228b22'
				},
			},

			axis: {
		    	x: {
		    		type: 'timeseries',
		    		tick: { culling:true }
				},
				y: {
		    		type: 'linear',
					padding: {top: 100, bottom: 200 },
					label: { text: '#{lp[102]}', position: 'outer-middle' }
				},
				y2: {
					show: true,
		    		type: 'linear',
					padding: {top: 200, bottom: 100},
 					tick: { format: d3.format("01d") },
 					label: { text: '#{lp[103]}', position: 'outer-middle' }
				}
			},

			legend: {
				show: true,
				position: 'bottom'
			},

			line: { connectNull: true, step: { type: 'step' }},
			zoom: { enabled: true, type: 'drag' },
			point: { show: true, r: 1 }
		});

//--------------------------------------------------------------------------
		var day_size = x_day.length - 1;
		var rd_weight = ['#{lp[106]}'];
		var rd_bfr = ['rd_bfr'];
		var p_weight = ['#{lp[105]}'];
		var p_bfr = ['p_bfr'];
		var r_weight = ['#{lp[104]}'];
		var r_bfr = ['r_bfr'];
		var rd_flag = true;
		var p_flag = true;
		for( i = day_size; i >= 1; i-- ){
			if( y_weight[i] != 'NA' ){
				if( rd_flag ){
					rd_weight.push( y_weight[i] );
					rd_bfr.push( y_bfr[i] );
					rd_flag = false;
				}else if( p_flag ){
					p_weight.push( y_weight[i] );
					p_bfr.push( y_bfr[i] );
					if( i <= day_size - 23 ){
						p_flag = false;
					}
				}else{
					r_weight.push( y_weight[i] );
					r_bfr.push( y_bfr[i] );
				}
			}
		}

		var chart_sub = c3.generate({
			bindto: '#physique_#{@module}-chart-sub',

			data: {
				columns: [
					r_weight,
					r_bfr,
					p_weight,
					p_bfr,
					rd_weight,
					rd_bfr
				],
				xs: { #{lp[106]}:'rd_bfr', #{lp[105]}:'p_bfr', #{lp[104]}:'r_bfr' },
				labels: true,
				type : 'scatter',
				colors: { #{lp[106]}:'#dc143c', #{lp[105]}:'#00ff00', #{lp[104]}:'#c0c0c0'}
			},

			axis: {
		    	x: {
					label: { text: '#{lp[103]}', position: 'outer-center' },
					padding: {left: 1, right: 1 },
					tick: { fit: false }
				},
				y: {
					label: { text: '#{lp[102]}', position: 'outer-middle' },
					padding: {top: 20, bottom: 20 },
					tick: { fit: false }
				},
			},
			grid: {
     			x: { show: true },
        		y: { show: true }
            },
			legend: { show: true, position: 'bottom' },
			point: { show: true, r: 4 },
			tooltip: { show: false }
		});

		var menergy = column[9];
		displayVIDEO(menergy);
		document.getElementById( 'menergy' ).value = menergy;
	});

};

drawChart();

</script>
JS
	puts js
end


def module_lp( language )
	mlp = Hash.new
	mlp['jp'] = []
	mlp['jp'][1] = "男性"
	mlp['jp'][2] = "女性"
	mlp['jp'][3] = "維持チャート"
	mlp['jp'][4] = "代謝的性別"
	mlp['jp'][5] = "年齢"
	mlp['jp'][6] = "身長（cm）"
	mlp['jp'][7] = "維持体重（kg）"
	mlp['jp'][8] = "開始日"
	mlp['jp'][9] = "身体活動レベル"
	mlp['jp'][10] = "予定エネルギー（kcal）"
	mlp['jp'][11] = "目安摂取エネルギー（kcal）"
	mlp['jp'][100] = "体重"
	mlp['jp'][101] = "体脂肪率"
	mlp['jp'][102] = "体重 (kg)"
	mlp['jp'][103] = "体脂肪率 (%)"
	mlp['jp'][104] = "過去"
	mlp['jp'][105] = "最近"
	mlp['jp'][106] = "直近"

	return mlp[language]
end