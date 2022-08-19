#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser Detective input 0.00b (2022/08/11)

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'detective'
food_max = 5

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
	delta1p = [[],[],[],[],[]]
	delta2p = [[],[],[],[],[]]
	vmax = []
	vmin = []
	food_nos = []

	r = mdb( "SELECT sum FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	if r.first
		sum = r.first['sum']
		foods = sum.split( "\t" )
		food_max.times do |c|
			if foods[c]
				a = foods[c].split( ':' )
				fn = a[0]
				food_nos << fn
				rr = mdb( "SELECT ENERC_KCAL, PROTV, FATV, CHOV, NACL_EQ FROM #{$MYSQL_TB_FCT} WHERE FN='#{fn}';", false, @debug )
				if rr.first
					delta1p[c] << rr.first['ENERC_KCAL'].to_f / 100
					delta1p[c] << rr.first['PROTV'].to_f / 100
					delta1p[c] << rr.first['FATV'].to_f / 100
					delta1p[c] << rr.first['CHOV'].to_f / 100
					delta1p[c] << rr.first['NACL_EQ'].to_f / 100

					delta2p[c] << rr.first['ENERC_KCAL'].to_f / 1000
					delta2p[c] << rr.first['PROTV'].to_f / 1000
					delta2p[c] << rr.first['FATV'].to_f / 1000
					delta2p[c] << rr.first['CHOV'].to_f / 1000
					delta2p[c] << rr.first['NACL_EQ'].to_f / 1000
				end
			else
				delta1p[c] = [0, 0, 0, 0, 0]
				delta2p[c] = [0, 0, 0, 0, 0]
			end
		end

		#
		puts "1st pass<br>" if @debug
		food_max.times do |c|
			limit = [1, 1, 1, 1, 1]
			limit[0] = ( energy / delta1p[c][0] ) if delta1p[c][0] != 0
			limit[1] = ( protein / delta1p[c][1] ) if delta1p[c][1] != 0
			limit[2] = ( fat / delta1p[c][2] ) if delta1p[c][2] != 0
			limit[3] = ( carbo / delta1p[c][3] ) if delta1p[c][3] != 0
			limit[4] = ( salt / delta1p[c][4] ) if delta1p[c][4] != 0
			vmax << limit.max.ceil
		end
		( food_max - 1 ).times do |c|
			vmax[c + 1] = vmax[c] if vmax[c] < vmax[c + 1]
		end
		p vmax if @debug

		puts "1st reasoning<br>" if @debug
		delta_min = -1
		delta_min_vol = []
		0.upto( vmax[0] ) do |c0|
			0.upto( vmax[1] ) do |c1|
				break if c1 > c0
				0.upto( vmax[2] ) do |c2|
					break if c2 > c1
					0.upto( vmax[3] ) do |c3|
						break if c3 > c2
						0.upto( vmax[4] ) do |c4|
							break if c4 > c3 || ( c0 + c1 + c2 + c3 + c4 ) > volume

							e_ = ( energy - ( delta1p[0][0] * c0 ) - ( delta1p[1][0] * c1 ) - ( delta1p[2][0] * c2 ) - ( delta1p[3][0] * c3 ) - ( delta1p[4][0] * c4 )) ** 2
							p_ = ( protein - ( delta1p[0][1] * c0 ) - ( delta1p[1][1] * c1 ) - (delta1p[2][1] * c2 ) - ( delta1p[3][1] * c3 ) - ( delta1p[4][1] * c4 )) ** 2
							f_ = ( fat - ( delta1p[0][2] * c0 ) - ( delta1p[1][2] * c1 ) - ( delta1p[2][2] * c2 ) - ( delta1p[3][2] * c3 ) - ( delta1p[4][2] * c4 ))  ** 2
							c_ = ( carbo - ( delta1p[0][3] * c0 ) - ( delta1p[1][3] * c1 ) - ( delta1p[2][3] * c2 ) - ( delta1p[3][3] * c3 ) - ( delta1p[4][3] * c4 ))  ** 2
							s_ = ( salt - ( delta1p[0][4] * c0 ) - ( delta1p[1][4] * c1 ) - ( delta1p[2][4] * c2 ) - ( delta1p[3][4] * c3 ) - ( delta1p[4][4] * c4 ))  ** 2
							delta = e_ + p_ + f_ + c_ + s_

							if delta_min > delta || delta_min < 0
								delta_min = delta
								delta_min_vol = [c0, c1, c2, c3, c4]
							end
						end
					end
				end
			end
		end
		p delta_min_vol if @debug

		puts "2nd pass<br>" if @debug
		food_max.times do |c|
			if delta2p[c][0] == 0 && delta2p[c][1] == 0 && delta2p[c][2] == 0 && delta2p[c][3] == 0 && delta2p[c][4] == 0
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
							break if c4 > c3 || ( c0 + c1 + c2 + c3 + c4 ) > volume10

							e_ = ( energy - ( delta2p[0][0] * c0 ) - ( delta2p[1][0] * c1 ) - ( delta2p[2][0] * c2 ) - ( delta2p[3][0] * c3 ) - ( delta2p[4][0] * c4 )) ** 2
							p_ = (( protein - ( delta2p[0][1] * c0 ) - ( delta2p[1][1] * c1 ) - (delta2p[2][1] * c2 ) - ( delta2p[3][1] * c3 ) - ( delta2p[4][1] * c4 )) * ( energy / protein )) ** 2
							f_ = (( fat - ( delta2p[0][2] * c0 ) - ( delta2p[1][2] * c1 ) - ( delta2p[2][2] * c2 ) - ( delta2p[3][2] * c3 ) - ( delta2p[4][2] * c4 )) * ( energy / fat ))  ** 2
							c_ = (( carbo - ( delta2p[0][3] * c0 ) - ( delta2p[1][3] * c1 ) - ( delta2p[2][3] * c2 ) - ( delta2p[3][3] * c3 ) - ( delta2p[4][3] * c4 )) * ( energy / carbo )) ** 2
							s_ = (( salt - ( delta2p[0][4] * c0 ) - ( delta2p[1][4] * c1 ) - ( delta2p[2][4] * c2 ) - ( delta2p[3][4] * c3 ) - ( delta2p[4][4] * c4 )) * ( energy / salt )) ** 2
							delta = e_ + p_ + f_ + c_ + s_

							if delta_min > delta || delta_min < 0
								delta_min = delta
								delta_min_vol = [c0, c1, c2, c3, c4]
							end
						end
					end
				end
			end
		end
		p delta_min_vol if @debug

		puts "Calculation FCT<br>" if @debug
		fw_ex = []
		fct_ex = [[],[],[],[],[]]
		fct_ex_total = [0.0, 0.0, 0.0, 0.0, 0.0]
		delta_min_vol.size.times do |c|
			t = ( delta_min_vol[c].to_f / 10 )
			fw_ex << t.round( 1 )
			food_max.times do |cc|
				fct_ex[c] << ( delta1p[c][cc] * t ).round( 1 )
				fct_ex_total[cc] += BigDecimal(( delta1p[c][cc] * t ).to_s )
			end
		end
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
		<button type='button' class='btn btn-sm btn-success' onclick="detectiveAdopt( '#{fw_ex[0]}', '#{fw_ex[1]}', '#{fw_ex[2]}', '#{fw_ex[3]}', '#{fw_ex[4]}' )">#{lp[8]}</button>
	</div>
</div>
HTML

	else
		puts 'ERROR'
	end

when 'adopt'
	puts 'ADOPT<br>' if @debug
	fws = [@cgi['fw1'], @cgi['fw2'], @cgi['fw3'], @cgi['fw4'], @cgi['fw5']]

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
