# Weight loss module for Physique 0.27b
#encoding: utf-8

@module = 'weight-loss'
@debug = false

def physique_module( cgi, user )
	l = module_lp( user.language )
	persed_today = Time.parse( @datetime )

	#importing from config
	r = mdb( "SELECT bio FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
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
	when 'raw'
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

		# X axis
		x_day = []
		persed_date = Time.parse( start_date )
		0.upto( 95 ) do |c|
			target_date = persed_date.strftime( "%Y-%m-%d" )
			x_day[c] = target_date
			persed_date += 86400
		end

		#Koyomiex config
		puts "Loading config<br>" if @debug
		weight_kex = -1
		denergy_kex = -1
		r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
		if r.first
			koyomi = JSON.parse( r.first['koyomi'] )
			kex_select = koyomi['kex_select']
			0.upto( 9 ) do |c|
 				weight_kex = c if kex_select[c.to_s] == 'WEIGHT'
				denergy_kex = c if kex_select[c.to_s] == 'dENERGY'
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
				denergy[c] = ( r.first["item#{denergy_kex}"].to_i ) * -1 if denergy_kex >= 0
				denergy[c] = 0 if denergy[c] == nil
			else
				measured[c] = nil
				denergy[c] = 0
			end
			persed_date += 86400
		end

		#Day 4 stable weight
		d4sw = []
		if measured.size >= 1 and measured[0] != nil
			persed_date = Time.parse( start_date )
			skip = 0
			0.upto( 95 ) do |c|
				break if persed_date > persed_today
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

				persed_date += 86400
			end
			d4sw.map! do |x|
				if x == nil
					x = 'NA'
				else
					x.round( 2 )
				end
			end
		end

		#Intake enargy 1pass
		tdiv_enargy = [[],[],[],[]]
		persed_date = Time.parse( start_date )
		0.upto( 95 ) do |c|
			break if persed_date > persed_today
			target_date = persed_date.strftime( "%Y-%m-%d" )
			res_koyomi = mdb( "SELECT fzcode, koyomi, tdiv FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND freeze=1 AND tdiv!=4 AND date='#{target_date}';", false, @debug )
			res_koyomi.each do |e|
				tdiv = e['tdiv'].to_i
				if /^\?\-\-/ =~ e['koyomi']
					tdiv_enargy[tdiv][c] = '?--'
				elsif /^\?\-/ =~ e['koyomi']
					tdiv_enargy[tdiv][c] = '?-'
				elsif /^\?\=/ =~ e['koyomi']
					tdiv_enargy[tdiv][c] = '?='
				elsif /^\?\+\+/ =~ e['koyomi']
					tdiv_enargy[tdiv][c] = '?++'
				elsif /^\?\+/ =~ e['koyomi']
					tdiv_enargy[tdiv][c] = '?+'
				elsif /^\?0/ =~ e['koyomi']
					tdiv_enargy[tdiv][c] = ''
				else
					res_fcz = mdb( "SELECT ENERC_KCAL FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND code='#{e['fzcode']}';", false, @debug )
					tdiv_enargy[tdiv][c] = res_fcz.first['ENERC_KCAL'].to_i
				end
			end
			persed_date += 86400
		end

		#tdiv energy / period
		tdiv_p0 = [[], [], [], []]
		tdiv_p1 = [[], [], [], []]
		tdiv_p2 = [[], [], [], []]
		tdiv_p3 = [[], [], [], []]
		tdiv_pset = [tdiv_p0, tdiv_p1, tdiv_p2, tdiv_p3]
		0.upto( 3 ) do |tdiv|
			0.upto( 95 ) do |c|
				if /\d/ =~ tdiv_enargy[tdiv][c].to_s
					period = ( c / 24 ).to_i
					tdiv_pset[period][tdiv] << tdiv_enargy[tdiv][c].to_i
				end
			end
		end

		#tdiv average & SE / period
		period_energy_ave = [[], [], [], []]
		period_energy_std = [[], [], [], []]
		0.upto( 3 ) do |period|
			0.upto( 3 ) do |tdiv|
				if  tdiv_pset[period][tdiv].size > 0
					period_energy_ave[period][tdiv] = BigDecimal(  tdiv_pset[period][tdiv].sum ) / tdiv_pset[period][tdiv].size
					a = tdiv_pset[period][tdiv].map do |x| ( x - period_energy_ave[period][tdiv] )**2 end
					period_energy_std[period][tdiv] = Math.sqrt( a.sum / a.size )
				else
					period_energy_ave[period][tdiv] = 0
					period_energy_std[period][tdiv] = 0
				end
			end
		end

		#Intake enargy 2pass
		ienergy = []
		0.upto( 3 ) do |tdiv|
			persed_date = Time.parse( start_date )
			0.upto( 95 ) do |c|
				break if persed_date > persed_today
				ienergy[c] = 0 if ienergy[c] == nil
				period = ( c / 24 ).to_i

				tdiv_enargy[tdiv][c] = '' if tdiv_enargy[tdiv][c] == nil && tdiv == 3
				tdiv_enargy[tdiv][c] = '?=' if tdiv_enargy[tdiv][c] == nil

				case tdiv_enargy[tdiv][c].to_s
				when '?--'
					tdiv_enargy[tdiv][c] = period_energy_ave[period][tdiv] - period_energy_std[period][tdiv]
				when '?-'
					tdiv_enargy[tdiv][c] = period_energy_ave[period][tdiv] - period_energy_std[period][tdiv] / 2
				when '?='
					tdiv_enargy[tdiv][c] = period_energy_ave[period][tdiv]
				when '?+'
					tdiv_enargy[tdiv][c] = period_energy_ave[period][tdiv] + period_energy_std[period][tdiv] / 2
				when '?++'
					tdiv_enargy[tdiv][c] = period_energy_ave[period][tdiv] + period_energy_std[period][tdiv]
				when ''
					tdiv_enargy[tdiv][c] = 0
				end
				ienergy[c] += tdiv_enargy[tdiv][c].to_i
				persed_date += 86400
			end
		end

		#Actual enargy (intake + delta )
		aenergy = []
		acutual_period_day = [0, 0, 0 ,0]
		acutual_period_total = [0, 0, 0 ,0]
		persed_date = Time.parse( start_date )
		0.upto( 95 ) do |c|
			break if persed_date > persed_today
			period = ( c / 24 ).to_i
			if ienergy[c] == nil
				aenergy[c] = denergy[c]
			else
				aenergy[c] = ienergy[c] + denergy[c]
			end
			acutual_period_day[period] += 1
			acutual_period_total[period] += aenergy[c]
			persed_date += 86400
		end

		#Actual average / period
		ave_energy = [0, 0, 0 ,0]
		0.upto( 3 ) do |period|
			ave_energy[period] = ( acutual_period_total[period] / acutual_period_day[period] ).to_i if acutual_period_day[period] != 0
			ave_energy[period] = l['empty'] if ave_energy[period] == 0
		end

		#Guide weight
		guide = []
		guide[0] = measured[0]
		guide[0] = weight if measured[0] == nil
		1.upto( 95 ) do |c|
			cenergy = calc_energy( guide[c-1], height, age, sex, pal )
			guide[c] = ( guide[0] - (( cenergy.to_f - eenergy.to_f ) / 7200 * c ))
		end
		guide.map! do |x| x.round( 2 ) end

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
		html << "  <span class='input-group-text'>1st period</span>"
		html << "  <input type='text' class='form-control form-control-sm' id='aveep1' value='' DISABLED>"
		html << "</div>"
		html << "</div>"
		html << '<div class="col-3">'
		html << "<div class='input-group input-group-sm'>"
		html << "  <span class='input-group-text'>2nd period</span>"
		html << "  <input type='text' class='form-control form-control-sm' id='aveep2' value='' DISABLED>"
		html << "</div>"
		html << "</div>"
		html << '<div class="col-3">'
		html << "<div class='input-group input-group-sm'>"
		html << "  <span class='input-group-text'>3rd period</span>"
		html << "  <input type='text' class='form-control form-control-sm' id='aveep3' value='' DISABLED>"
		html << "</div>"
		html << "</div>"
		html << '<div class="col-3">'
		html << "<div class='input-group input-group-sm'>"
		html << "  <span class='input-group-text'>final period</span>"
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
