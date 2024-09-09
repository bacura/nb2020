# Weight keep module for Physique 0.06b (2024/08/07)
#encoding: utf-8

@debug = false

def physique_module( cgi, db )
	l = module_lp( db.user.language )
	mod = cgi['mod']
	today_p = Time.parse( @datetime )

	puts "LOAD bio config<br>" if @debug
	r = db.query( "SELECT bio FROM #{$MYSQL_TB_CFG} WHERE user='#{db.user.name}';", false )
	if r.first
		if r.first['bio'] != nil && r.first['bio'] != ''
			bio = JSON.parse( r.first['bio'] )
			sex = bio['sex'].to_i
			birth = Time.parse( bio['birth'] )
			height = bio['height'].to_f * 100
			weight = bio['weight'].to_f
			pgene = bio['pgene'].to_i
			age = ( Date.today.strftime( "%Y%m%d" ).to_i - birth.strftime( "%Y%m%d" ).to_i ) / 10000
		end
	end

	if height == nil || weight == nil || age == nil
		puts l['error_no-set']
		exit( 0 )
	end

	start_date = cgi['start_date']
	pal = cgi['pal'].to_f

	if pal == 0.0
		res = db.query( "SELECT json FROM #{$MYSQL_TB_MODJ} WHERE user='#{db.user.name}' and module='#{mod}';", false )
		if res.first
			mod_cfg_h = JSON.parse( res.first['json'] )
			start_date = mod_cfg_h[mod]['start_date']
			pal = mod_cfg_h[mod]['pal'].to_f
		end
	end
	start_date = @date if start_date == ""


	html = ''
	puts cgi['step'] if @debug
	case cgi['step']
	when 'form'
		module_js( mod, l )
		if pal == ''
			start_date = $DATE
			pal = 1.50
		end

		sex_ = [l['male'], l['female']]

		####
########
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
			<input type='date' class='form-control' id='start_date' value='#{start_date}' onchange='WeightKeepChartDraw()'>
		</div>
	</div>
	<div class='col-3'>
		<div class="input-group input-group-sm">
			<label class="input-group-text">#{l['pal']}</label>
			<input type='number' min='0.5' max='2.5' step='0.01' class='form-control' id='pal' value='#{pal}' onchange='noticeEER()'>
		</div>
	</div>
</div>
HTML
########
		####
	when 'raw'
		puts "SET date<br>" if @debug

		start_date_p = Time.parse( start_date )
		p start_date if @debug

		puts "SET X axis<br>" if @debug
		x_day = []
		start_date_p = Time.parse( start_date )
		while start_date_p <= today_p do
			x_day << start_date_p.strftime( "%Y-%m-%d" )
			start_date_p += 86400
		end

		puts "SET measured weight & body fat tate<br>" if @debug
		measured_weight = []
		bfr = []
		recent_weight = 0.0
		start_date_p = Time.parse( start_date )

		r = db.query( "SELECT * FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{db.user.name}' AND date>='#{start_date}';", false )
		r.each do |e|
			if e['cell'] != nil
				kexc = JSON.parse( e['cell'] )
				day_pass = (( Time.parse( e['date'].strftime( "%Y-%m-%d" ) ) - start_date_p ) / 86400 ).to_i
				measured_weight[day_pass] = kexc['体重'].to_f if kexc['体重'] != nil
				recent_weight = kexc['体重'].to_f if kexc['体重'] != nil
				bfr[day_pass] = kexc['体脂肪率'].to_f if kexc['体脂肪率'] != nil
			end
		end

		measured_weight.map! do |x|
			if x == nil || x == 0
				x = 'NA'
			else
				x = x
			end
		end

		bfr.map! do |x|
			if x == nil || x == 0
				x = 'NA'
			else
				x = x
			end
		end

		raw = []
		raw[0] = x_day.unshift( 'x_day' ).join( ',' )
		raw[1] = measured_weight.unshift( l['data_weight'] ).join( ',' )
		raw[2] = bfr.unshift( l['data_bfr'] ).join( ',' )

		puts raw.join( ':' )
		exit

	when 'results'
		html = '<div class="row">'
		html << "<div class='col-9'><div id='physique_#{mod}-chart' align='center'></div></div>"
		html << "<div class='col-3'><div id='physique_#{mod}-chart-sub' align='center'></div>"
		html << '</div>'


	when 'notice'
		puts "CALC energy<br>" if @debug

		r = db.query( "SELECT * FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{db.user.name}' AND date>='#{start_date}';", false )
		r.each do |e|
			if e['cell'] != nil
				kexc = JSON.parse( e['cell'] )
				recent_weight = kexc['体重'].to_f if kexc['体重'] != nil
			end
		end

		if recent_weight == nil
			puts "こよみ拡張記録に体重データがありません。"
			exit
		end

		m_energy = calc_energy( weight, height, age, sex, pal )
		delta_weight = recent_weight - weight
		delta_energy = 0.0

		if delta_weight > 0
			if delta_weight > 1
				delta_energy = 7200 / 24
				m_energy = (( m_energy - delta_energy ) / 100 ).floor * 100
			else
				delta_energy = delta_weight * 7200 / 24
				m_energy = (( m_energy - delta_energy ) / 100 ).round * 100
			end
		else
			if delta_weight < -1
				delta_energy = -7200 / 24
				m_energy = (( m_energy - delta_energy ) / 100 ).ceil * 100
			else
				delta_energy = delta_weight * 7200 / 24
				m_energy = (( m_energy - delta_energy ) / 100 ).round * 100
			end
		end
		m_energy -= 200 if pgene == 1

		html << '<div class="row">'
		html << '<div class="col-4">'
		html << "<div class='input-group input-group-sm'>"
		html << "  <span class='input-group-text'>#{l['menergy']}</span>"
		html << "  <input type='text' class='form-control form-control-sm' id='menergy' value='#{m_energy}' DISABLED>"
		html << "</div>"
		html << '</div>'
	end

	json = JSON.generate( { mod => { "start_date" => start_date, "pal" => pal }} )
	res = db.query( "SELECT module FROM #{$MYSQL_TB_MODJ} WHERE user='#{db.user.name}' AND module='#{mod}';", false )
	if res.first
		db.query( "UPDATE #{$MYSQL_TB_MODJ} SET json='#{json}' WHERE user='#{db.user.name}' AND module='#{mod}';", true )
	else
		db.query( "INSERT INTO #{$MYSQL_TB_MODJ} SET json='#{json}', user='#{db.user.name}', module='#{mod}';", true )
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


def module_js( mod, l )
	js = <<-"JS"
<script type='text/javascript'>

var WeightKeepChartDraw = function(){
//	dl4 = true;
	displayBW();

	var start_date = document.getElementById( "start_date" ).value;
	var pal = document.getElementById( "pal" ).value;
//	$.post( "physique.cgi", { mod:'#{mod}', step:'monitor', start_date:start_date, pal:pal }, function( raw ){ $( "#L4" ).html( raw );});
	$.post( "physique.cgi", { mod:'#{mod}', step:'raw', start_date:start_date, pal:pal }, function( raw ){

		var column = ( String( raw )).split( ':' );
		var x_day = ( String( column[0] )).split(',');
		var y_weight = ( String( column[1] )).split(',');
		var y_bfr = ( String( column[2] )).split(',');

		if( y_weight.length > 1 ){
			var chart = c3.generate({
				bindto: '#physique_#{mod}-chart',

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
						tick: { format: d3.format( ".1f" ) },
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
			var l_weight = ['#{l['data_latest']}'];
			var l_bfr = ['l_bfr'];
			var p_weight = ['#{l['data_past']}'];
			var p_bfr = ['p_bfr'];
			var r_weight = ['#{l['data_recent']}'];
			var r_bfr = ['r_bfr'];
			var f_weight = ['#{l['data_first']}'];
			var	f_bfr = ['f_bfr'];
			var l_flag = true;
			var p_flag = true;

			for( var i = day_size; i >= 1; i-- ){
				if( y_weight[i] != 'NA' && y_bfr[i] != 'NA' && y_weight[i] != null && y_bfr[i] != null ){
					if( l_flag ){
						l_weight.push( y_weight[i] );
						l_bfr.push( y_bfr[i] );
						l_flag = false;
					}else if( p_flag ){
						r_weight.push( y_weight[i] );
						r_bfr.push( y_bfr[i] );
						if( i <= day_size - 23 ){
							p_flag = false;
						}
					}else{
						p_weight.push( y_weight[i] );
						p_bfr.push( y_bfr[i] );
					}
				}
			}
			if( p_weight.length > 1 ){
				f_weight[1] = p_weight.pop();
				f_bfr[1] = p_bfr.pop();
			}else if( r_weight.length > 1 ){
				f_weight[1] = r_weight.pop();
				f_bfr[1] = r_bfr.pop();
			}else{
				f_weight[1] = y_weight[1];
				f_bfr[1] = y_bfr[1];
			}

			var chart_sub = c3.generate({
				bindto: '#physique_#{mod}-chart-sub',

				data: {
					columns: [
						f_weight,
						f_bfr,
						p_weight,
						p_bfr,
						r_weight,
						r_bfr,
						l_weight,
						l_bfr
					],
					xs: { #{l['data_first']}:'f_bfr', #{l['data_past']}:'p_bfr', #{l['data_latest']}:'l_bfr', #{l['data_recent']}:'r_bfr' },
					labels: true,
					type : 'scatter',
					colors: { #{l['data_first']}:'#4b0082', #{l['data_past']}:'#c0c0c0',  #{l['data_recent']}:'#00ff00', #{l['data_latest']}:'#dc143c' }
				},

				axis: {
			    	x: {
						label: { text: '#{l['label_bfr']}', position: 'outer-center' },
						padding: {left: 1, right: 1 },
						tick: { fit: false, format: d3.format( "01D" ) }
					},
					y: {
						label: { text: '#{l['label_weight']}', position: 'outer-middle' },
						padding: {top: 20, bottom: 20 },
						tick: { fit: false, format: d3.format( ".1f" ) }
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
		}else{
			displayVIDEO( 'Non weight data' );
		}
	});

};

var noticeEER = function(){
	var start_date = document.getElementById( "start_date" ).value;
	var pal = document.getElementById( "pal" ).value;
	$.post( "physique.cgi", { mod:'#{mod}', step:'notice', start_date:start_date, pal:pal }, function( data ){
		$( "#L3" ).html( data );
		dl3 = true;
		displayBW();
	});
};


$( document ).ready( function(){
	WeightKeepChartDraw();
	noticeEER();
});


</script>
JS
	puts js
end


def module_lp( language )
	l = Hash.new
	l['jp'] = {
		'mod_name' => "維持チャート",\
		'male' => "男性",\
		'female' => "女性",\
		'chart_name' => "維持チャート",\
		'sex' => "代謝的性別",\
		'age' => "年齢",\
		'height' => "身長（cm）",\
		'weight' => "目標維持体重（kg）",\
		'start_date' => "開始日",\
		'pal' => "身体活動レベル",\
		'menergy' => "目安摂取エネルギー（kcal）",\
		'data_weight' => "体重",\
		'data_bfr' => "体脂肪率",\
		'label_weight' => "体重 (kg)",\
		'label_bfr' => "体脂肪率 (%)",\
		'data_first' => "開始",\
		'data_past' => "過去",\
		'data_recent' => "近頃",\
		'data_latest' => "直近",\
		'error_no-set' => "設定から生体情報を設定してください。"
	}

	return l[language]
end