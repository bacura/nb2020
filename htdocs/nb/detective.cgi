#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser Detective input 0.04b (2022/10/14)

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
@dummy = false
script = 'detective'
food_max = 10

#==============================================================================
#DEFINITION
#==============================================================================

def html_form_hints( user, lp, volume, energy, protein, fat, carbo, salt )
	reasoning_button = ''
	r = mdb( "SELECT sum FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	if r.first
		sum = r.first['sum']
		foods = sum.split( "\t" )
		reasoning_button = "<button type='button' class='btn btn-sm btn-warning' onclick=\"reasoning()\">#{lp[6]}</button>" if foods.size > 0
	end

	token_button = ''
	r = mdbr( "SELECT token FROM detective WHERE user='#{user.name}';", false, @debug )
	token_button = "<span class='badge text-light bg-dark' onclick=\"loadDetectiveResult()\">#{lp[14]}</span>" if r.first

html = <<-"HTML"
<div class='container-fluid'>
	<div align="right">#{token_button}</div><br>
	<div class='row'>
		<div class='col-2'>
			#{lp[7]}<br>
			<input type='text' id='volume' value='#{volume}'>
		</div>
		<div class='col-2'>
			#{lp[1]}<br>
			<input type='text' id='energy' value='#{energy}'>
		</div>
		<div class='col-2'>
			#{lp[2]}<br>
			<input type='text' id='protein' value='#{protein}'>
		</div>
		<div class='col-2'>
			#{lp[3]}<br>
			<input type='text' id='fat' value='#{fat}'>
		</div>
		<div class='col-2'>
			#{lp[4]}<br>
			<input type='text' id='carbo' value='#{carbo}'>
		</div>
		<div class='col-2'>
			#{lp[5]}<br>
			<input type='text' id='salt' value='#{salt}'>
		</div>
	</div>
	<br>
	<div class='row'>
		#{reasoning_button}
	</div>
</div>
HTML

	return html
end


def html_table_result( user, lp,volume, energy, protein, fat, carbo, salt, food_nos, fw_ex, fct_ex, fct_ex_total, fct_ratio )
	c = 0
	tbody = '<tbody>'
	food_nos.each do |e|
		r = mdb( "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{e}';", false, @debug )
		if r.first
			tbody << '<tr>'
			tbody << "<td>#{r.first['name']}</td>"
			tbody << "<td>#{fw_ex[c]}</td>"
			5.times do |cc| tbody << "<td>#{fct_ex[c][cc]}</td>" end
			tbody << '</tr>'
		end
		c += 1
	end

	fct_ratio_ = ''
	5.times do |c| fct_ratio_ << "<td class='text-danger'>#{fct_ratio[c]}%</td>" end

	fct_ex_total_ = ''
	5.times do |c| fct_ex_total_ << "<td>#{fct_ex_total[c].to_f}</td>" end

	fw_ex_solid = fw_ex.join( ':' )
	food_nos_solid = food_nos.join( ':' )


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<table class='table table-sm'>
			<thead>
				<tr>
					<td class='cb_header'>#{lp[9]}</td>
					<td class='cb_header'>#{lp[7]}</td>
					<td class='cb_header'>#{lp[1]}</td>
					<td class='cb_header'>#{lp[2]}</td>
					<td class='cb_header'>#{lp[3]}</td>
					<td class='cb_header'>#{lp[4]}</td>
					<td class='cb_header'>#{lp[5]}</td>
				</td>
			<thead>

			<tbody>
			#{tbody}

			<br>

			<tr>
			<td>#{lp[10]}</td><td></td>
			#{fct_ex_total_}
			</tr>

			<tr>
			<td>#{lp[11]}</td><td></td>
			<td>#{energy}</td>
			<td>#{protein}</td>
			<td>#{fat}</td>
			<td>#{carbo}</td>
			<td>#{salt}</td>
			</tr>

			<tr>
			<td>#{lp[12]}</td><td></td>
				#{fct_ratio_}
			</tr>

			</tbody>
		</table>
	</div>
	<br>
	<div class='row'>
		<button type='button' class='btn btn-sm btn-success' onclick="detectiveAdopt( '#{food_nos_solid}', '#{fw_ex_solid}' )">#{lp[8]}</button>
	</div>
</div>
HTML

	return html
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


puts "POST<br>" if @debug
command = @cgi['command']
code = @cgi['code']
volume = @cgi['volume'].to_i
energy = @cgi['energy'].to_f
protein = @cgi['protein'].to_f
fat = @cgi['fat'].to_f
carbo = @cgi['carbo'].to_f
salt = @cgi['salt'].to_f
if @dummy
	command = 'reasoning'
	user.name = 'gm'
	volume = 100
	energy = 231
	protein = 1.8
	fat = 20.7
	carbo = 9.3
	salt = 3.0
end
if @debug
	puts "command:#{command}<br>"
	puts "code:#{code}<br>"
	puts "volume:#{volume}<br>"
	puts "energy:#{energy}<br>"
	puts "protein:#{protein}<br>"
	puts "fat:#{fat}<br>"
	puts "carbo:#{carbo}<br>"
	puts "salt:#{salt}<br>"
	puts "<hr>"
end


####
html = ''
message = ''
case command
when 'reasoning'
	puts 'REASONING<br>' if @debug
	dp1 = [[],[],[],[],[],[],[],[],[],[]]
	dp2 = [[],[],[],[],[],[],[],[],[],[]]
	vmax = []
	vmin = []
	food_nos = []
	food_weights = []
	food_checks = []

	if volume > 100
		volume = 100
		energy = energy / volume * 100
		protein = protein / volume * 100
		fat = fat / volume * 100
		carbo = carbo / volume * 100
		salt = salt / volume * 100
	end

	r = mdb( "SELECT sum FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	if r.first
		sum = r.first['sum']
		foods = sum.split( "\t" )
		food_max.times do |c|
			if foods[c]
				a = foods[c].split( ':' )
				food_nos << a[0]
				food_weights << a[1].to_f
				food_checks << a[4].to_i

				query = ''
				if /P/ =~ a[0]
          			query  = "SELECT ENERC_KCAL, PROTV, FATV, CHOV, NACL_EQ FROM #{$MYSQL_TB_FCTP} WHERE FN='#{a[0]}';"
				elsif /U/ =~ a[0]
          			query  = "SELECT ENERC_KCAL, PROTV, FATV, CHOV, NACL_EQ FROM #{$MYSQL_TB_FCTP} WHERE FN='#{a[0]}' AND user='#{user.name}';"
				else
          			query  = "SELECT ENERC_KCAL, PROTV, FATV, CHOV, NACL_EQ FROM #{$MYSQL_TB_FCT} WHERE FN='#{a[0]}';"
				end
				rr = mdb( query, false, @debug )
				if rr.first
					dp1[c] << rr.first['ENERC_KCAL'].to_f / 100
					dp1[c] << rr.first['PROTV'].to_f / 100
					dp1[c] << rr.first['FATV'].to_f / 100
					dp1[c] << rr.first['CHOV'].to_f / 100
					dp1[c] << rr.first['NACL_EQ'].to_f / 100

					dp2[c] << rr.first['ENERC_KCAL'].to_f / 1000
					dp2[c] << rr.first['PROTV'].to_f / 1000
					dp2[c] << rr.first['FATV'].to_f / 1000
					dp2[c] << rr.first['CHOV'].to_f / 1000
					dp2[c] << rr.first['NACL_EQ'].to_f / 1000
				end
			else
				dp1[c] = [0, 0, 0, 0, 0]
				dp2[c] = [0, 0, 0, 0, 0]
			end
		end

		#
		puts "1st pass<br>" if @debug
		food_max.times do |c|
			limit = [1, 1, 1, 1, 1]
			limit[0] = ( energy / dp1[c][0] ) if dp1[c][0] != 0
			limit[1] = ( protein / dp1[c][1] ) if dp1[c][1] != 0
			limit[2] = ( fat / dp1[c][2] ) if dp1[c][2] != 0
			limit[3] = ( carbo / dp1[c][3] ) if dp1[c][3] != 0
			limit[4] = ( salt / dp1[c][4] ) if dp1[c][4] != 0
			vmax << limit.max.ceil
		end

		food_max.times do |c|
			if food_checks[c] == 1
				vmin[c] = ( food_weights[c].floor ).to_i
				vmax[c] = ( food_weights[c].ceil ).to_i
			else
				vmin[c] = 0
				vmax[c] = volume if vmax[c] > volume
			end
		end

		( food_max - 1 ).times do |c|
			vmax[c + 1] = vmax[c] if vmax[c] < vmax[c + 1]
		end
		p vmin, vmax if @debug

		puts "1st reasoning<br>" if @debug
		delta_min = -1
		delta_min_vol = []
		dpm = [[],[],[],[],[],[],[],[],[],[]]
		10.times do |i|
			10.times do |j|
				dpm[i][j] = 0
			end
		end

		vmin[0].upto( vmax[0] ) do |c0|
			5.times do |c| dpm[0][c] = dp1[0][c] * c0 end
			vmin[1].upto( vmax[1] ) do |c1|
				break if c1 > c0 || ( c0 + c1 ) > volume
				5.times do |c| dpm[1][c] = dp1[1][c] * c1 end
				vmin[2].upto( vmax[2] ) do |c2|
					break if c2 > c1 || ( c0 + c1 + c2 ) > volume
					5.times do |c| dpm[2][c] = dp1[2][c] * c2 end
					vmin[3].upto( vmax[3] ) do |c3|
						break if c3 > c2 || ( c0 + c1 + c2 + c3 ) > volume
						5.times do |c| dpm[3][c] = dp1[3][c] * c3 end
						vmin[4].upto( vmax[4] ) do |c4|
							break if c4 > c3 || ( c0 + c1 + c2 + c3 + c4 ) > volume
							5.times do |c| dpm[4][c] = dp1[4][c] * c4 end
							vmin[5].upto( vmax[5] ) do |c5|
								break if c5 > c4 || ( c0 + c1 + c2 + c3 + c4 + c5 ) > volume
								5.times do |c| dpm[5][c] = dp1[5][c] * c5 end
								vmin[6].upto( vmax[6] ) do |c6|
									break if c6 > c5 || ( c0 + c1 + c2 + c3 + c4 + c5 + c6 ) > volume
									5.times do |c| dpm[6][c] = dp1[6][c] * c6 end
									vmin[7].upto( vmax[7] ) do |c7|
										break if c7 > c6 || ( c0 + c1 + c2 + c3 + c4 + c5 + c6 + c7 ) > volume
										5.times do |c| dpm[7][c] = dp1[7][c] * c7 end
										vmin[8].upto( vmax[8] ) do |c8|
											break if c8 > c7 || ( c0 + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 ) > volume
											5.times do |c| dpm[8][c] = dp1[8][c] * c8 end
											vmin[9].upto( vmax[9] ) do |c9|
												break if c9 > c8 || ( c0 + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 ) > volume
												5.times do |c| dpm[9][c] = dp1[9][c] * c9 end

												e_ = ( energy - dpm[0][0] - dpm[1][0] - dpm[2][0] - dpm[3][0] - dpm[4][0] - dpm[5][0] - dpm[6][0] - dpm[7][0] - dpm[8][0] - dpm[9][0] ) ** 2
												p_ = ( protein - dpm[0][1] - dpm[1][1] - dpm[2][1] - dpm[3][1] - dpm[4][1] - dpm[5][1] - dpm[6][1] - dpm[7][1] - dpm[8][1] - dpm[9][1] ) ** 2
												f_ = ( fat - dpm[0][2] - dpm[1][2] - dpm[2][2] - dpm[3][2] - dpm[4][2] - dpm[5][2] - dpm[6][2] - dpm[7][2] - dpm[8][2] - dpm[9][2] )  ** 2
												c_ = ( carbo - dpm[0][3] - dpm[1][3] - dpm[2][3] - dpm[3][3] - dpm[4][3] - dpm[5][3] - dpm[6][3] - dpm[7][3] - dpm[8][3] - dpm[9][3] )  ** 2
												s_ = ( salt - dpm[0][4] - dpm[1][4] - dpm[2][4] - dpm[3][4] - dpm[4][4] - dpm[5][4] - dpm[6][4] - dpm[7][4] - dpm[8][4] - dpm[9][4] )  ** 2
												delta = e_ + p_ + f_ + c_ + s_

												if delta_min > delta || delta_min < 0
													delta_min = delta
													delta_min_vol = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9]
												end
											end
										end
									end
								end
							end
						end
					end
				end
			end
		end
		p delta_min_vol if @debug

		puts "2nd pass<br>" if @debug
		food_max.times do |c|
			if food_checks[c] == 1
				vmin[c] = ( food_weights[c] * 10 ).floor.to_i
				vmax[c] = ( food_weights[c] * 10 ).ceil.to_i
			elsif dp2[c][0] == 0 && dp2[c][1] == 0 && dp2[c][2] == 0 && dp2[c][3] == 0 && dp2[c][4] == 0
				vmin[c] = 0
				vmax[c] = 1
			else
				vmin[c] = (( delta_min_vol[c] - 1 ) * 10 ).to_i
				vmin[c] = 0 if vmin[c] < 0
				vmax[c] = (( delta_min_vol[c] + 1 ) * 10 ).to_i
			end
		end
		p  vmin,vmax if @debug

		puts "2nd reasoning<br>" if @debug
		delta_min = -1
		delta_min_vol = []

		10.times do |i|
			10.times do |j|
				dpm[i][j] = 0
			end
		end

		volume12 = volume * 12
		vmin[0].upto( vmax[0] ) do |c0|
			5.times do |c| dpm[0][c] = dp2[0][c] * c0 end
			vmin[1].upto( vmax[1] ) do |c1|
				break if c1 > c0 || ( c0 + c1 ) > volume12
				5.times do |c| dpm[1][c] = dp2[1][c] * c1 end
				vmin[2].upto( vmax[2] ) do |c2|
					break if c2 > c1 || ( c0 + c1 + c2 ) > volume12
					5.times do |c| dpm[2][c] = dp2[2][c] * c2 end
					vmin[3].upto( vmax[3] ) do |c3|
						break if c3 > c2 || ( c0 + c1 + c2 + c3 ) > volume12
						5.times do |c| dpm[3][c] = dp2[3][c] * c3 end
						vmin[4].upto( vmax[4] ) do |c4|
							break if c4 > c3 || ( c0 + c1 + c2 + c3 + c4 ) > volume12
							5.times do |c| dpm[4][c] = dp2[4][c] * c4 end
							vmin[5].upto( vmax[5] ) do |c5|
								break if c5 > c4 || ( c0 + c1 + c2 + c3 + c4 + c5 ) > volume12
								5.times do |c| dpm[5][c] = dp2[5][c] * c5 end
								vmin[6].upto( vmax[6] ) do |c6|
									break if c6 > c5 || ( c0 + c1 + c2 + c3 + c4 + c5 + c6 ) > volume12
									5.times do |c| dpm[6][c] = dp2[6][c] * c6 end
									vmin[7].upto( vmax[7] ) do |c7|
										break if c7 > c6 || ( c0 + c1 + c2 + c3 + c4 + c5 + c6 + c7 ) > volume12
										5.times do |c| dpm[7][c] = dp2[7][c] * c7 end
										vmin[8].upto( vmax[8] ) do |c8|
											break if c8 > c7 || ( c0 + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 ) > volume12
											5.times do |c| dpm[8][c] = dp2[8][c] * c8 end
											vmin[9].upto( vmax[9] ) do |c9|
												break if c9 > c8 || ( c0 + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 ) > volume12
												5.times do |c| dpm[9][c] = dp2[9][c] * c9 end

												e_ = ( energy - dpm[0][0] - dpm[1][0] - dpm[2][0] - dpm[3][0] - dpm[4][0] - dpm[5][0] - dpm[6][0] - dpm[7][0] - dpm[8][0] - dpm[9][0] ) ** 2
												p_ = (( protein - dpm[0][1] - dpm[1][1] - dpm[2][1] - dpm[3][1] - dpm[4][1] - dpm[5][1] - dpm[6][1] - dpm[7][1] - dpm[8][1] - dpm[9][1] ) ) ** 2
												f_ = (( fat - dpm[0][2] - dpm[1][2] - dpm[2][2] - dpm[3][2] - dpm[4][2] - dpm[5][2] - dpm[6][2] - dpm[7][2] - dpm[8][2] - dpm[9][2] ) ) ** 2
												c_ = (( carbo - dpm[0][3] - dpm[1][3] - dpm[2][3] - dpm[3][3] - dpm[4][3] - dpm[5][3] - dpm[6][3] - dpm[7][3] - dpm[8][3] - dpm[9][3] )  ) ** 2
												s_ = (( salt - dpm[0][4] - dpm[1][4] - dpm[2][4] - dpm[3][4] - dpm[4][4] - dpm[5][4] - dpm[6][4] - dpm[7][4] - dpm[8][4] - dpm[9][4] ) ) ** 2
												delta = e_ + p_ + f_ + c_ + s_

												if delta_min > delta || delta_min < 0
													delta_min = delta
													delta_min_vol = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9]
												end
											end
										end
									end
								end
							end
						end
					end
				end
			end
		end
		p delta_min_vol if @debug

		puts "CALC FCT<br>" if @debug
		fw_ex = []
		fct_ex = [[],[],[],[],[],[],[],[],[],[]]
		fct_ex_total = [0.0, 0.0, 0.0, 0.0, 0.0]
		delta_min_vol.size.times do |c|
			t = ( delta_min_vol[c].to_f / 10 )
			fw_ex << t.round( 1 )
			food_max.times do |cc|
				if dp1[c][cc] != nil
					fct_ex[c] << ( dp1[c][cc] * t ).round( 1 )
					fct_ex_total[cc] += BigDecimal(( dp1[c][cc] * t ).to_s )
				end
			end
		end

		fct_ex_total.map! do |x| x = x.round( 1 ) end

		puts "CALC FCT ratio<br>" if @debug
		fct_ratio = []
		fct_ratio << ( fct_ex_total[0] / energy * 100 ).round( 1 ).to_f
		fct_ratio << ( fct_ex_total[1] / protein * 100 ).round( 1 ).to_f
		fct_ratio << ( fct_ex_total[2] / fat * 100 ).round( 1 ).to_f
		fct_ratio << ( fct_ex_total[3] / carbo * 100 ).round( 1 ).to_f
		fct_ratio << ( fct_ex_total[4] / salt * 100 ).round( 1 ).to_f
		fct_ratio.map! do |x|
			if x.nan?
				x = 0.0
			else
				x = x
			end
		end

		puts "CHECK detective table in DBR<br>" if @debug
		r = mdbr( "SHOW TABLES LIKE '#{script}';", false, @debug )
		mdbr( "CREATE TABLE #{script} ( token VARCHAR(24) NOT NULL PRIMARY KEY, user VARCHAR(32), result TEXT );", false, @debug ) unless r.first
		token = issue_token()
		hints = { 'volume' => volume, 'energy' => energy, 'protein' => protein, 'fat' => fat, 'carbo' => carbo, 'salt' => salt }
		ptime = Time.at( Time.now - @time_now ) - 60 * 60 * 9
		result_ = JSON.generate( { 'food_nos' => food_nos, 'hints' => hints, 'fw_ex' => fw_ex, 'fct_ex' => fct_ex, 'fct_ex_total' => fct_ex_total, 'fct_ratio' => fct_ratio, 'ptime' => ptime } )
		mdbr( "DELETE FROM #{script} WHERE user='#{user.name}';", false, @debug )
		mdbr( "INSERT INTO #{script} SET token='#{token}', user='#{user.name}', result='#{result_}';", false, @debug )

		html =  html_table_result( user, lp, volume, energy, protein, fat, carbo, salt, food_nos, fw_ex, fct_ex, fct_ex_total, fct_ratio )
		message = "#{lp[15]} #{ptime.hour}:#{ptime.min}:#{ptime.sec}"
	else
		puts 'ERROR'
	end

when 'load_result'
	puts 'load_result<br>' if @debug
	r = mdbr( "SELECT * FROM #{script} WHERE user='#{user.name}';", false, @debug )
	if r.first
		result = JSON.parse( r.first['result'] )
		ptime = Time.parse( result['ptime'] )
		hints = result['hints']
		food_nos = result['food_nos']
		fw_ex = result['fw_ex']
		fct_ex = result['fct_ex']
		fct_ex_total = result['fct_ex_total']
		fct_ratio = result['fct_ratio']

		volume = hints['volume']
		energy = hints['energy']
		protein = hints['protein']
		fat = hints['fat']
		carbo = hints['carbo']
		salt = hints['salt']

		html =  html_table_result( user, lp, volume, energy, protein, fat, carbo, salt, food_nos, fw_ex, fct_ex, fct_ex_total, fct_ratio )
		message = "#{lp[15]} #{ptime.hour}:#{ptime.min}:#{ptime.sec}"
	else
		message = "ERROR"
	end

when 'adopt'
	puts 'ADOPT<br>' if @debug
	food_nos = @cgi['food_nos_solid'].split( ':' )
	fw_ex = @cgi['fw_ex_solid'].split( ':' )
	r = mdb( "SELECT sum FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	new_sum = ''
	sum = r.first['sum']
	if sum != ''
		foods = sum.split( "\t" )
		c = 0
		new_sums = []
		foods.each do |e|
			if c < food_max
				a = e.split( ':' )
				a[1] = fw_ex[c]
				a[2] = 'g'
				a[3] = fw_ex[c]
				a[7] = fw_ex[c]
				t = a.join( ':' )
				new_sums << t
			else
				new_sums << e
			end
			c += 1
		end
		new_sum = new_sums.join( "\t" )
	else
		food_nos.size.times do |c|
			new_sum << "#{food_nos[c]}:#{fw_ex[c]}:g:#{fw_ex[c]}:::1.0:#{fw_ex[c]}\t"
		end
		new_sum.chop!
	end
	mdb( "UPDATE #{$MYSQL_TB_SUM} set sum='#{new_sum}' WHERE user='#{user.name}';", false, @debug )

when 'wait'
	html = '<div class="spinner-border" role="status" align="center"><span class="visually-hidden">Loading...</span></div>'
	message = lp[16]
else
	if code != ''
		puts "FCZ import<br>" if @debug
		r = mdb( "SELECT origin, ENERC_KCAL, PROTV, FATV, CHOV, NACL_EQ FROM #{$MYSQL_TB_FCZ} WHERE code='#{code}' AND user='#{user.name}';", false, @debug )
		if r.first
			volume = r.first['origin'].to_i
			energy = r.first['ENERC_KCAL'].to_f
			protein = r.first['PROTV'].to_f
			fat = r.first['FATV'].to_f
			carbo = r.first['CHOV'].to_f
			salt = r.first['NACL_EQ'].to_f
		else
			r = mdbr( "SELECT * FROM #{script} WHERE user='#{user.name}';", false, @debug )
			if r.first
				result = JSON.parse( r.first['result'] )
				volume = hints['volume']
				energy = hints['energy']
				protein = hints['protein']
				fat = hints['fat']
				carbo = hints['carbo']
				salt = hints['salt']
			end
		end
	end

	html = html_form_hints( user, lp, volume, energy, protein, fat, carbo, salt )
end


message = `uptime` if message == ''
puts "<div align='center'>#{lp[13]}&nbsp;&nbsp;#{message}</div><br>"

puts html
