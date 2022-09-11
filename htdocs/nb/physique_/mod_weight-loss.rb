# Weight loss module for Physique 0.28b (2022/09/11)
#encoding: utf-8

@module = 'weight-loss'
@debug = false
@period = 96

def physique_module( cgi, user )
	l = module_lp( user.language )
	today_p = Time.parse( @datetime )

	puts "LOAD bio config<br>" if @debug
	r = mdb( "SELECT bio FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
	if r.first
		if r.first['bio'] != nil && r.first['bio'] != ''
			bio = JSON.parse( r.first['bio'] )
			sex = bio['sex'].to_i
			birth = Time.parse( bio['birth'] )
			height = bio['height'].to_f * 100
			weight = bio['weight'].to_f
			age = ( Date.today.strftime( "%Y%m%d" ).to_i - birth.strftime( "%Y%m%d" ).to_i ) / 10000
		end
	end

	if height == nil || weight == nil || age == nil
		puts l['error_no-set']
		exit( 0 )
	end

	html = ''
	case cgi['step']
	when 'form'
		module_js( l )
		start_date = $DATE
		pal = 1.50
		eenergy = calc_energy( weight, height, age, sex, pal )

		r = mdb( "SELECT json FROM #{$MYSQL_TB_MODJ} WHERE user='#{user.name}' and module='#{@module}';", false, @debug )
		if r.first
			mod_cfg_h = JSON.parse( r.first['json'] )
			start_date = mod_cfg_h[@module]['start_date']
			pal = mod_cfg_h[@module]['pal'].to_f
			eenergy = mod_cfg_h[@module]['eenergy'].to_i
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
			<input type='date' class='form-control' id='start_date' value='#{start_date}' onchange='drawChart()'>
		</div>
	</div>
	<div class='col-3'>
		<div class="input-group input-group-sm">
			<label class="input-group-text">#{l['pal']}</label>
			<input type='number' min='0.5' max='2.5' step='0.1' class='form-control' id='pal' value='#{pal}' onchange='drawChart()'>
		</div>
	</div>

	<div class='col-3'>
		<div class='input-group input-group-sm'>
			<span class='input-group-text'>#{l['eenergy']}</span>
			<input type='number' class='form-control' id='eenergy' min='0' value='#{eenergy}' onchange='drawChart()'>
		</div>
	</div>
</div>
HTML
########
		####

	when 'raw'
		puts "SET date<br>" if @debug
		start_date = cgi['start_date']
		pal = cgi['pal'].to_f
		eenergy = cgi['eenergy'].to_i

		json = JSON.generate( { @module => { "start_date" => start_date, "pal" => pal, "eenergy" => eenergy }} )
		res = mdb( "SELECT module FROM #{$MYSQL_TB_MODJ} WHERE user='#{user.name}' AND module='#{@module}';", false, @debug )
		if res.first
			mdb( "UPDATE #{$MYSQL_TB_MODJ} SET json='#{json}' WHERE user='#{user.name}' AND module='#{@module}';", false, @debug )
		else
			mdb( "INSERT INTO #{$MYSQL_TB_MODJ} SET json='#{json}', user='#{user.name}', module='#{@module}';", false, @debug )
		end
		start_date_p = Time.parse( start_date )
		end_date = ( start_date_p + ( @period - 1 ) * 86400 ).strftime( "%Y-%m-%d" )
		p start_date, end_date if @debug


		puts "SET X axis<br>" if @debug
		x_day = []
		start_date_p = Time.parse( start_date )
		@period.times do |c|
			x_day[c] = start_date_p.strftime( "%Y-%m-%d" )
			start_date_p += 86400
		end


		puts "SET measured weight & delta energy<br>" if @debug
		measured = []
		denergy = []
		start_date_p = Time.parse( start_date )
		r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND date BETWEEN '#{start_date}' AND '#{end_date}';", false, @debug )
		r.each do |e|
			kexc = JSON.parse( e['cell'] )
			day_pass = (( Time.parse( e['date'].strftime( "%Y-%m-%d" ) ) - start_date_p ) / 86400 ).to_i
			measured[day_pass] = kexc['体重'].to_f if kexc['体重'] != nil
			denergy[day_pass] = kexc['Δエネルギー'].to_f if kexc['Δエネルギー'] != nil
		end

		puts "Day 4 stable weight<br>" if @debug
		d4sw = []
		if measured.size >= 1 and measured[0] != nil
			start_day_p = Time.parse( start_date )
			skip = 0
			@period.times do |c|
				break if start_day_p > today_p
				if measured[c] != nil && measured[c] != '' && measured[c] != 0
					case skip
					when 0
						d4sw[c] = measured[c]
						skip = 1
					when 1
						d4sw[c] = ( measured[c] + ( measured[c-1] / 2 )) / 1.5
						skip = 2
					when 2
						d4sw[c] = ( measured[c] + ( measured[c-1] / 2 ) + ( measured[c-2] / 4 )) / 1.75
						skip = c
					else
						d4sw[c] = ( measured[c] + ( measured[c-1] / 2 ) + ( measured[c-2] / 4 ) + ( measured[c-3] / 8 )) / 1.875
						skip = c
					end
				else
					d4sw[c] = nil
					skip = 0
				end

				start_day_p += 86400
			end
			d4sw.map! do |x|
				if x == nil
					x = 'NA'
				else
					x.round( 2 )
				end
			end
		end

		puts "LOAD Intake enargy 1pass<br>" if @debug
		tdiv_enargy = [[],[],[],[]]
		start_date_p = Time.parse( start_date )
		res_koyomi = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND freeze=1 AND tdiv!=4 AND date BETWEEN '#{start_date}' AND '#{end_date}';", false, @debug )
		res_koyomi.each do |e|
			tdiv = e['tdiv'].to_i
			day_pass = (( Time.parse( e['date'].strftime( "%Y-%m-%d" ) ) - start_date_p ) / 86400 ).to_i
			if /^\?\-\-/ =~ e['koyomi']
				tdiv_enargy[tdiv][day_pass] = '?--'
			elsif /^\?\-/ =~ e['koyomi']
				tdiv_enargy[tdiv][day_pass] = '?-'
			elsif /^\?\=/ =~ e['koyomi']
				tdiv_enargy[tdiv][day_pass] = '?='
			elsif /^\?\+\+/ =~ e['koyomi']
				tdiv_enargy[tdiv][day_pass] = '?++'
			elsif /^\?\+/ =~ e['koyomi']
				tdiv_enargy[tdiv][day_pass] = '?+'
			elsif /^\?0/ =~ e['koyomi']
				tdiv_enargy[tdiv][day_pass] = ''
			else
				res_fcz = mdb( "SELECT ENERC_KCAL FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND code='#{e['fzcode']}';", false, @debug )
				tdiv_enargy[tdiv][day_pass] = res_fcz.first['ENERC_KCAL'].to_i
			end
		end

		puts "SET tdiv energy / pahse<br>" if @debug
		tdiv_p0 = [[], [], [], []]
		tdiv_p1 = [[], [], [], []]
		tdiv_p2 = [[], [], [], []]
		tdiv_p3 = [[], [], [], []]
		tdiv_pset = [tdiv_p0, tdiv_p1, tdiv_p2, tdiv_p3]
		0.upto( 3 ) do |tdiv|
			@period.times do |c|
				if /\d/ =~ tdiv_enargy[tdiv][c].to_s
					phase = ( c / 24 ).to_i
					tdiv_pset[phase][tdiv] << tdiv_enargy[tdiv][c].to_i
				end
			end
		end

		puts "SET tdiv average & SE / phase<br>" if @debug
		phase_energy_ave = [[], [], [], []]
		phase_energy_std = [[], [], [], []]
		0.upto( 3 ) do |phase|
			0.upto( 3 ) do |tdiv|
				if  tdiv_pset[phase][tdiv].size > 0
					phase_energy_ave[phase][tdiv] = BigDecimal(  tdiv_pset[phase][tdiv].sum ) / tdiv_pset[phase][tdiv].size
					a = tdiv_pset[phase][tdiv].map do |x| ( x - phase_energy_ave[phase][tdiv] )**2 end
					phase_energy_std[phase][tdiv] = Math.sqrt( a.sum / a.size )
				else
					phase_energy_ave[phase][tdiv] = 0
					phase_energy_std[phase][tdiv] = 0
				end
			end
		end

		puts "CALC intake enargy 2pass<br>" if @debug
		ienergy = []
		0.upto( 3 ) do |tdiv|
			start_day_p = Time.parse( start_date )
			@period.times do |c|
				break if start_day_p > today_p
				ienergy[c] = 0 if ienergy[c] == nil
				phase = ( c / 24 ).to_i

				tdiv_enargy[tdiv][c] = '' if tdiv_enargy[tdiv][c] == nil && tdiv == 3
				tdiv_enargy[tdiv][c] = '?=' if tdiv_enargy[tdiv][c] == nil

				case tdiv_enargy[tdiv][c].to_s
				when '?--'
					tdiv_enargy[tdiv][c] = phase_energy_ave[phase][tdiv] - phase_energy_std[phase][tdiv]
				when '?-'
					tdiv_enargy[tdiv][c] = phase_energy_ave[phase][tdiv] - phase_energy_std[phase][tdiv] / 2
				when '?='
					tdiv_enargy[tdiv][c] = phase_energy_ave[phase][tdiv]
				when '?+'
					tdiv_enargy[tdiv][c] = phase_energy_ave[phase][tdiv] + phase_energy_std[phase][tdiv] / 2
				when '?++'
					tdiv_enargy[tdiv][c] = phase_energy_ave[phase][tdiv] + phase_energy_std[phase][tdiv]
				when ''
					tdiv_enargy[tdiv][c] = 0
				end
				ienergy[c] += tdiv_enargy[tdiv][c].to_i
				start_day_p += 86400
			end
		end

		puts "CALC actual enargy (intake + delta )<br>" if @debug
		aenergy = []
		acutual_phase_day = [0, 0, 0 ,0]
		acutual_phase_total = [0, 0, 0 ,0]
		start_day_p = Time.parse( start_date )
		@period.times do |c|
			break if start_day_p > today_p
			phase = ( c / 24 ).to_i
			denergy[c] = 0 if denergy[c] == nil
			if ienergy[c] == nil
				aenergy[c] = denergy[c]
			else
				aenergy[c] = ienergy[c] + denergy[c]
			end
			acutual_phase_day[phase] += 1
			acutual_phase_total[phase] += aenergy[c]
			start_day_p += 86400
		end

		puts "CALC actual average / phase<br>" if @debug
		ave_energy = [0, 0, 0 ,0]
		0.upto( 3 ) do |phase|
			ave_energy[phase] = ( acutual_phase_total[phase] / acutual_phase_day[phase] ).to_i if acutual_phase_day[phase] != 0
			ave_energy[phase] = l['empty'] if ave_energy[phase] == 0
		end

		puts "SET Guide weight<br>" if @debug
		guide = []
		guide[0] = measured[0]
		guide[0] = weight if measured[0] == nil
		@period.times do |c|
			cenergy = calc_energy( guide[c-1], height, age, sex, pal )
			guide[c] = ( guide[0] - (( cenergy.to_f - eenergy.to_f ) / 7200 * c ))
		end
		guide.map! do |x| x.round( 2 ) end

		#Theoletical weight
		theoletic = []
		theoletic[0] = measured[0]
		theoletic[0] = weight if measured[0] == nil
		start_day_p = Time.parse( start_date ) + 86400
		1.upto( @period - 1 ) do |c|
			break if start_day_p > today_p
			cenergy = calc_energy( theoletic[c-1], height, age, sex, pal )
			theoletic[c] = ( theoletic[c-1] - (( cenergy.to_f - aenergy[c] ) / 7200 ))
			start_day_p += 86400
		end
		theoletic.map! do |x| x.round( 2 ) end

		raw = []
		raw[0] = x_day.unshift( 'x_day' ).join( ',' )
		raw[1] = guide.unshift( l['data_guide'] ).join( ',' )
		raw[2] = theoletic.unshift( l['data_theoletic'] ).join( ',' )
		raw[3] = d4sw.unshift( l['data_d4sw'] ).join( ',' )
		raw[4] = ienergy.unshift( l['data_ienergy'] ).join( ',' )
		raw[5] = denergy.unshift( l['data_denergy'] ).join( ',' )
		raw[6] = aenergy.unshift( l['data_aenergy'] ).join( ',' )
		raw[7] = ave_energy.join( ',' )
		puts raw.join( ':' )
		exit

	when 'chart'
		html = '<div class="row">'
		html << "<div class='col'><div id='physique_#{@module}-chart' align='center'></div>"
		html << '</div>'

	when 'notice'
		html = "<h5>#{l['bw_name']}</h5>"
		html << '<div class="row">'
		html << '<div class="col-3">'
		html << "<div class='input-group input-group-sm'>"
		html << "  <span class='input-group-text'>1st phase</span>"
		html << "  <input type='text' class='form-control form-control-sm' id='aveep1' value='' DISABLED>"
		html << "</div>"
		html << "</div>"
		html << '<div class="col-3">'
		html << "<div class='input-group input-group-sm'>"
		html << "  <span class='input-group-text'>2nd phase</span>"
		html << "  <input type='text' class='form-control form-control-sm' id='aveep2' value='' DISABLED>"
		html << "</div>"
		html << "</div>"
		html << '<div class="col-3">'
		html << "<div class='input-group input-group-sm'>"
		html << "  <span class='input-group-text'>3rd phase</span>"
		html << "  <input type='text' class='form-control form-control-sm' id='aveep3' value='' DISABLED>"
		html << "</div>"
		html << "</div>"
		html << '<div class="col-3">'
		html << "<div class='input-group input-group-sm'>"
		html << "  <span class='input-group-text'>final phase</span>"
		html << "  <input type='text' class='form-control form-control-sm' id='aveep4' value='' DISABLED>"
		html << "</div>"
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
//	dl4 = true;
	displayBW();

	var start_date = document.getElementById( "start_date" ).value;
	var pal = document.getElementById( "pal" ).value;
	var eenergy = document.getElementById( "eenergy" ).value;

//	$.post( 'physique.cgi', { mod:'#{@module}', step:'raw', start_date:start_date, pal:pal, eenergy:eenergy }, function( data ){ $( '#L4' ).html( data );});
	$.post( "physique.cgi", { mod:'#{@module}', step:'raw', start_date:start_date, pal:pal, eenergy:eenergy }, function( raw ){

		var column = ( String( raw )).split( ':' );
		var chart = c3.generate({
			bindto: '#physique_#{@module}-chart',
//			size: { width: 960, height: 450 },

			data: {
				columns: [
					( String( column[0] )).split(','),	// x_day
					( String( column[1] )).split(','),	// ガイド体重
					( String( column[2] )).split(','),	// 理論体重
					( String( column[3] )).split(','),	// D4安定体重
					( String( column[4] )).split(','),	// 摂取エネルギー
					( String( column[5] )).split(','), 	// Δ消費エネルギー
					( String( column[6] )).split(',') 	// 実エネルギー
				],
				x: 'x_day',
				axes: {
					#{l['data_ienergy']}: 'y2',
					#{l['data_denergy']}: 'y2',
					#{l['data_aenergy']}: 'y2'
				},
				labels: false,
				type : 'line',
				types: { #{l['data_ienergy']}: 'area-step', #{l['data_denergy']}: 'area-step', #{l['data_aenergy']}: 'area-step' },
				colors: {
					#{l['data_guide']}: '#d3d3d3',
					#{l['data_theoletic']}: '#228b22',
					#{l['data_d4sw']}: '#dc143c',
					#{l['data_ienergy']}: '#ffd700',
					#{l['data_denergy']}: '#00ffff',
					#{l['data_aenergy']}: '#d2691e'
				},
				regions: {
					#{l['data_guide']}: { 'start':0, 'style':'dashed' }
				}
			},

			axis: {
		    	x: {
		    		type: 'timeseries'
				},
				y: {
		    		type: 'linear',
					padding: {top: 50, bottom: 100 },
					label: { text: '#{l['label_weight']}', position: 'outer-middle' }
				},
				y2: {
					show: true,
		    		type: 'linear',
					padding: {top: 400, bottom: 0 },
					label: { text: '#{l['label_energy']}', position: 'outer-middle' }
				}
			},

			legend: {
				show: true,
				position: 'bottom'
			},

			line: { connectNull: true, step: { type: 'step' }},
			bar: { width: { ratio: 1.0 }},
			point: { show: true, r: 2 }
		});

		var average_e = ( String( column[7] )).split(',')
		$.post( "physique.cgi", { mod:'#{@module}', step:'notice' }, function( data ){
			$( "#L3" ).html( data );
			document.getElementById( 'aveep1' ).value = average_e[0];
			document.getElementById( 'aveep2' ).value = average_e[1];
			document.getElementById( 'aveep3' ).value = average_e[2];
			document.getElementById( 'aveep4' ).value = average_e[3];
		});
	});

};

drawChart();

</script>
JS
	puts js
end


def module_lp( language )
	l = Hash.new
	l['jp'] = {
		'male' => "男性",\
		'female' => "女性",\
		'chart_name' => "減量チャート",\
		'sex' => "代謝的性別",\
		'age' => "年齢",\
		'height' => "身長（cm）",\
		'weight' => "初期体重（kg）",\
		'start_date' => "開始日",\
		'pal' => "身体活動レベル",\
		'eenergy' => "予定エネルギー（kcal）",\
		'data_ienergy' => "摂取エネルギー",\
		'data_denergy' => "Δ消費エネルギー",\
		'data_aenergy' => "実エネルギー",\
		'data_guide' => "ガイド体重",\
		'data_theoletic' => "理論体重",\
		'data_d4sw' => "D4安定体重",\
		'label_weight' => "体重 (kg)",\
		'label_energy' => "エネルギー (kcal)",\
		'empty' => "ごんぶと",\
		'bw_name' => "平均摂取エネルギー",\
		'error_no-set' => "設定から生体情報を設定してください。"
	}

	return l[language]
end
