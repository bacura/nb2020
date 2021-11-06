# Weight keep module for Physique 0.00b
#encoding: utf-8

require 'time'

@module = 'weight-keep'

def physique_module( cgi, user, debug )
	l = module_lp( user.language )
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
		module_js( l )

		start_date = $DATE
		pal = 1.50

		res = mdb( "SELECT json FROM #{$MYSQL_TB_MODJ} WHERE user='#{user.name}' and module='#{@module}';", false, debug )
		if res.first
			mod_cfg_h = JSON.parse( res.first['json'] )
			start_date = mod_cfg_h[@module]['start_date']
			pal = mod_cfg_h[@module]['pal'].to_f
		end

		sex_ = [l['male'], l['female']]
		female_selected = ''
		female_selected = 'SELECTED ' if sex == 1

html = <<-"HTML"
		<div class='row'>
			<div class='col'><h5>#{l['chart_name']}</h5></div>
		</div>

		<div class='row'>
		<div class='col-6'>
		<table class='table table-sm'>
			<thead><th></th><th>#{l['sex']}</th><th>#{l['age']}</th><th>#{l['height']}</th><th>#{l['weight']}</th></thead>
			<tr><td></td><td>#{sex_[sex]}</td><td>#{age}</td><td>#{height}</td><td>#{weight}</td></tr>
		</table>
		</div>
		</div>

		<div class='row'>
			<div class='col-3'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>#{l['start_date']}</span>
					<input type='date' class='form-control' id='start_date' value='#{start_date}' onchange='drawChart()'>
				</div>
			</div>
			<div class='col-3'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">#{l['pal']}</label>
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

		m_energy = calc_energy( recent_weight, height, age, sex, pal )
		delta_weight = recent_weight - weight
		delta_energy = 0.0
		if delta_weight > 0
			if delta_weight > 1
				delta_energy = 7200 / 24
				m_energy = ( m_energy / 100 ).floor * 100 - delta_energy
			else
				delta_energy = delta_weight * 7200 / 24
				m_energy = ( m_energy / 100 ).round * 100 - delta_energy
			end
		else
			if delta_weight < -1
				delta_energy = -7200 /24
				m_energy = ( m_energy / 100 ).ceil * 100 - delta_energy
			else
				delta_energy = delta_weight * 7200 / 24
				m_energy = ( m_energy / 100 ).round * 100 - delta_energy
			end
		end
		m_energy -= 200 if pgene == 1

		raw = []
		raw[0] = x_day.unshift( 'x_day' ).join( ',' )
		raw[1] = measured_weight.unshift( l['data_weight'] ).join( ',' )
		raw[2] = bfr.unshift( l['data_bfr'] ).join( ',' )
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
		html << "  <span class='input-group-text'>#{l['menergy']}</span>"
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


def module_js( l )
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
					#{l['data_bfr']}: 'y2',
				},
				labels: false,
				type : 'line',
				colors: {
					#{l['data_weight']}: '#dc143c',
					#{l['data_bfr']}: '#228b22'
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
					label: { text: '#{l['label_weight']}', position: 'outer-middle' }
				},
				y2: {
					show: true,
		    		type: 'linear',
					padding: {top: 200, bottom: 100},
 					tick: { format: d3.format("01d") },
 					label: { text: '#{l['label_bfr']}', position: 'outer-middle' }
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
		var rd_weight = ['#{l['data_latest']}'];
		var rd_bfr = ['rd_bfr'];
		var p_weight = ['#{l['data_recent']}'];
		var p_bfr = ['p_bfr'];
		var r_weight = ['#{l['data_past']}'];
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
				xs: { #{l['data_latest']}:'rd_bfr', #{l['data_recent']}:'p_bfr', #{l['data_past']}:'r_bfr' },
				labels: true,
				type : 'scatter',
				colors: { #{l['data_latest']}:'#dc143c', #{l['data_recent']}:'#00ff00', #{l['data_past']}:'#c0c0c0'}
			},

			axis: {
		    	x: {
					label: { text: '#{l['label_bfr']}', position: 'outer-center' },
					padding: {left: 1, right: 1 },
					tick: { fit: false }
				},
				y: {
					label: { text: '#{l['label_weight']}', position: 'outer-middle' },
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
		document.getElementById( 'menergy' ).value = menergy;
	});

};

drawChart();

</script>
JS
	puts js
end


def module_lp( language )
	l = Hash.new
	l['jp'] = { 'male' => "男性",\
		'female' => "女性",\
		'chart_name' => "維持チャート",\
		'sex' => "代謝的性別",\
		'age' => "年齢",\
		'height' => "身長（cm）",\
		'weight' => "維持体重（kg）",\
		'start_date' => "開始日",\
		'pal' => "身体活動レベル",\
		'menergy' => "目安摂取エネルギー（kcal）",\
		'data_weight' => "体重",\
		'data_bfr' => "体脂肪率",\
		'label_weight' => "体重 (kg)",\
		'label_bfr' => "体脂肪率 (%)",\
		'data_past' => "過去",\
		'data_recent' => "最近",\
		'data_latest' => "直近"
	}

	return l[language]
end