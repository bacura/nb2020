#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser Detective input 0.01b (2022/08/20)

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'detective'
food_max = 10

#==============================================================================
#DEFINITION
#==============================================================================


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
		( food_max - 1 ).times do |c|
			vmax[c + 1] = vmax[c] if vmax[c] < vmax[c + 1]
		end

		food_max.times do |c|
			if food_checks[c] == 1
				vmin[c] = ( food_weights[c].floor ).to_i
				vmax[c] = ( food_weights[c].ceil ).to_i
			else
				vmin[c] = 0
			end
		end
		p vmax, vmin if @debug

		puts "1st reasoning<br>" if @debug
		delta_min = -1
		delta_min_vol = []
		vmin[0].upto( vmax[0] ) do |c0|
			vmin[1].upto( vmax[1] ) do |c1|
				break if c1 > c0
				vmin[2].upto( vmax[2] ) do |c2|
					break if c2 > c1
					vmin[3].upto( vmax[3] ) do |c3|
						break if c3 > c2
						vmin[4].upto( vmax[4] ) do |c4|
							break if c4 > c3
							vmin[5].upto( vmax[5] ) do |c5|
								break if c5 > c4
								vmin[6].upto( vmax[6] ) do |c6|
									break if c6 > c5
									vmin[7].upto( vmax[7] ) do |c7|
										break if c7 > c6
										vmin[8].upto( vmax[8] ) do |c8|
											break if c8 > c7
											vmin[9].upto( vmax[9] ) do |c9|
												break if c9 > c8 || ( c0 + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 ) > volume

												e_ = ( energy - ( dp1[0][0] * c0 ) - ( dp1[1][0] * c1 ) - ( dp1[2][0] * c2 ) - ( dp1[3][0] * c3 ) - ( dp1[4][0] * c4 ) - ( dp1[5][0] * c5 ) - ( dp1[6][0] * c6 ) - ( dp1[7][0] * c7 ) - ( dp1[8][0] * c8 ) - ( dp1[9][0] * c9 )) ** 2
												p_ = ( protein - ( dp1[0][1] * c0 ) - ( dp1[1][1] * c1 ) - (dp1[2][1] * c2 ) - ( dp1[3][1] * c3 ) - ( dp1[4][1] * c4 ) - ( dp1[5][1] * c5 ) - ( dp1[6][1] * c6 ) - ( dp1[7][1] * c7 ) - ( dp1[8][1] * c8 ) - ( dp1[9][1] * c9 )) ** 2
												f_ = ( fat - ( dp1[0][2] * c0 ) - ( dp1[1][2] * c1 ) - ( dp1[2][2] * c2 ) - ( dp1[3][2] * c3 ) - ( dp1[4][2] * c4 ) - ( dp1[5][2] * c5 ) - ( dp1[6][2] * c6 ) - ( dp1[7][2] * c7 ) - ( dp1[8][2] * c8 ) - ( dp1[9][2] * c9 ))  ** 2
												c_ = ( carbo - ( dp1[0][3] * c0 ) - ( dp1[1][3] * c1 ) - ( dp1[2][3] * c2 ) - ( dp1[3][3] * c3 ) - ( dp1[4][3] * c4 ) - ( dp1[5][3] * c5 ) - ( dp1[6][3] * c6 ) - ( dp1[7][3] * c7 ) - ( dp1[8][3] * c8 ) - ( dp1[9][3] * c9 ))  ** 2
												s_ = ( salt - ( dp1[0][4] * c0 ) - ( dp1[1][4] * c1 ) - ( dp1[2][4] * c2 ) - ( dp1[3][4] * c3 ) - ( dp1[4][4] * c4 ) - ( dp1[5][4] * c5 ) - ( dp1[6][4] * c6 ) - ( dp1[7][4] * c7 ) - ( dp1[8][4] * c8 ) - ( dp1[9][4] * c9 ))  ** 2
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
				vmin[c] = ( delta_min_vol[c] - 1 ) * 10
				vmin[c] = 0 if vmin[c] < 0
				vmax[c] = ( delta_min_vol[c] + 1 ) * 10
			end
		end
		p  vmin,vmax if @debug

		puts "2nd reasoning<br>" if @debug
		delta_min = -1
		delta_min_vol = []
		volume10 = volume * 10
		vmin[0].upto( vmax[0] ) do |c0|
			vmin[1].upto( vmax[1] ) do |c1|
				break if c1 > c0
				vmin[2].upto( vmax[2] ) do |c2|
					break if c2 > c1
					vmin[3].upto( vmax[3] ) do |c3|
						break if c3 > c2
						vmin[4].upto( vmax[4] ) do |c4|
							break if c4 > c3
							vmin[5].upto( vmax[5] ) do |c5|
								break if c5 > c4
								vmin[6].upto( vmax[6] ) do |c6|
									break if c6 > c5
									vmin[7].upto( vmax[7] ) do |c7|
										break if c7 > c6
										vmin[8].upto( vmax[8] ) do |c8|
											break if c8 > c7
											vmin[9].upto( vmax[9] ) do |c9|
												break if c9 > c8 || ( c0 + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 ) > volume10

												e_ = ( energy - ( dp2[0][0] * c0 ) - ( dp2[1][0] * c1 ) - ( dp2[2][0] * c2 ) - ( dp2[3][0] * c3 ) - ( dp2[4][0] * c4 ) - ( dp2[5][0] * c5 ) - ( dp2[6][0] * c6 ) - ( dp2[7][0] * c7 ) - ( dp2[8][0] * c8 ) - ( dp2[9][0] * c9 )) ** 2
												p_ = (( protein - ( dp2[0][1] * c0 ) - ( dp2[1][1] * c1 ) - (dp2[2][1] * c2 ) - ( dp2[3][1] * c3 ) - ( dp2[4][1] * c4 ) - ( dp2[5][1] * c5 ) - ( dp2[6][1] * c6 ) - ( dp2[7][1] * c7 ) - ( dp2[8][1] * c8 ) - ( dp2[9][1] * c9 )) * ( energy / protein )) ** 2
												f_ = (( fat - ( dp2[0][2] * c0 ) - ( dp2[1][2] * c1 ) - ( dp2[2][2] * c2 ) - ( dp2[3][2] * c3 ) - ( dp2[4][2] * c4 ) - ( dp2[5][2] * c5 ) - ( dp2[6][2] * c6 ) - ( dp2[7][2] * c7 ) - ( dp2[8][2] * c8 ) - ( dp2[9][2] * c9 )) * ( energy / fat )) ** 2
												c_ = (( carbo - ( dp2[0][3] * c0 ) - ( dp2[1][3] * c1 ) - ( dp2[2][3] * c2 ) - ( dp2[3][3] * c3 ) - ( dp2[4][3] * c4 ) - ( dp2[5][3] * c5 ) - ( dp2[6][3] * c6 ) - ( dp2[7][3] * c7 ) - ( dp2[8][3] * c8 ) - ( dp2[9][3] * c9 )) * ( energy / carbo )) ** 2
												s_ = (( salt - ( dp2[0][4] * c0 ) - ( dp2[1][4] * c1 ) - ( dp2[2][4] * c2 ) - ( dp2[3][4] * c3 ) - ( dp2[4][4] * c4 ) - ( dp2[5][4] * c5 ) - ( dp2[6][4] * c6 ) - ( dp2[7][4] * c7 ) - ( dp2[8][4] * c8 ) - ( dp2[9][4] * c9 )) * ( energy / salt )) ** 2
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

		puts "Calculation FCT<br>" if @debug
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
		fw_ex_set = fw_ex.join( ':' )

		fct_ex_total.map! do |x| x = x.round( 1 ) end

		puts "FCT ratio<br>" if @debug
		fct_ratio = []
		fct_ratio << ( fct_ex_total[0] / energy * 100 ).round( 1 ).to_f
		fct_ratio << ( fct_ex_total[1] / protein * 100 ).round( 1 ).to_f
		fct_ratio << ( fct_ex_total[2] / fat * 100 ).round( 1 ).to_f
		fct_ratio << ( fct_ex_total[3] / carbo * 100 ).round( 1 ).to_f
		fct_ratio << ( fct_ex_total[4] / salt * 100 ).round( 1 ).to_f

		puts "tbody HTML<br>" if @debug
		c = 0
		tbody_html = '<tbody>'
		food_nos.each do |e|
			r = mdb( "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{e}';", false, @debug )
			if r.first
				tbody_html << '<tr>'
				tbody_html << "<td>#{r.first['name']}</td>"
				tbody_html << "<td>#{fw_ex[c]}</td>"
				5.times do |cc|
					tbody_html << "<td>#{fct_ex[c][cc]}</td>"
				end
				tbody_html << '</tr>'
			end
			c += 1
		end
		tbody_html << '<br>'

		tbody_html << '<tr>'
		tbody_html << "<td>#{lp[10]}</td><td></td>"
		5.times do |c| tbody_html << "<td>#{fct_ex_total[c].to_f}</td>" end
		tbody_html << '</tr>'

		tbody_html << '<tr>'
		tbody_html << "<td>#{lp[11]}</td><td></td>"
		tbody_html << "<td>#{energy}</td>"
		tbody_html << "<td>#{protein}</td>"
		tbody_html << "<td>#{fat}</td>"
		tbody_html << "<td>#{carbo}</td>"
		tbody_html << "<td>#{salt}</td>"
		tbody_html << '</tr>'

		tbody_html << '<tr>'
		tbody_html << "<td>#{lp[12]}</td><td></td>"
		5.times do |c| tbody_html << "<td class='text-danger'>#{fct_ratio[c]}%</td>" end
		tbody_html << '</tr>'

		tbody_html << '</tbody>'

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
			#{tbody_html}
		</table>
	</div>
	<br>
	<div class='row'>
		<button type='button' class='btn btn-sm btn-success' onclick="detectiveAdopt( '#{fw_ex_set}' )">#{lp[8]}</button>
	</div>
</div>
HTML

	else
		puts 'ERROR'
	end

when 'adopt'
	puts 'ADOPT<br>' if @debug
	fws = @cgi['fw_set'].split( ':' )

	r = mdb( "SELECT sum FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	if r.first
		sum = r.first['sum']
		foods = sum.split( "\t" )
		c = 0
		new_sums = []
		foods.each do |e|
			if c < food_max
				a = e.split( ':' )
				a[1] = fws[c]
				a[2] = 'g'
				a[3] = fws[c]
				a[7] = fws[c]
				t = a.join( ':' )
				new_sums << t
			else
				new_sums << e
			end
			c += 1
		end
		new_sum = new_sums.join( "\t" )
		mdb( "UPDATE #{$MYSQL_TB_SUM} set sum='#{new_sum}' WHERE user='#{user.name}';", false, @debug )
	end
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
		end
	end

	reasoning_button = ''
	r = mdb( "SELECT sum FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	if r.first
		sum = r.first['sum']
		foods = sum.split( "\t" )
		reasoning_button = "<button type='button' class='btn btn-sm btn-warning' onclick=\"reasoning()\">#{lp[6]}</button>" if foods.size > 0
	end

	html = <<-"HTML"
<div class='container-fluid'>
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

end

puts "<div align='center'>#{lp[13]}</div><br>"

puts html
