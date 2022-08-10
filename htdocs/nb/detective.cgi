#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser Detective input 0.02b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require 'matrix'


#==============================================================================
#STATIC
#==============================================================================
@debug = true
script = 'detective'


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

puts "POST<br>" if @debug
command = 'reasoning'
code = ''
volume = 65
energy = 112
protein = 1.7
fat = 0.3
carbo = 25.6
salt = 0.1
user.name = 'gm'

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
	fct_delta = [[],[],[],[],[]]
	food_max = 5

	r = mdb( "SELECT sum FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	if r.first
		sum = r.first['sum']
		foods = sum.split( "\t" )
		5.times do |c|
			if foods[c]
				a = foods[c].split( ':' )
				fn = a[0]
				rr = mdb( "SELECT ENERC_KCAL, PROTV, FATV, CHOV, NACL_EQ FROM #{$MYSQL_TB_FCT} WHERE FN='#{fn}';", false, @debug )
				if rr.first
					fct_delta[c] << rr.first['ENERC_KCAL'].to_f / 1000
					fct_delta[c] << rr.first['PROTV'].to_f / 1000
					fct_delta[c] << rr.first['FATV'].to_f / 1000
					fct_delta[c] << rr.first['CHOV'].to_f / 1000
					fct_delta[c] << rr.first['NACL_EQ'].to_f / 1000
				end
			else
				food_max = c
				break
			end
		end

		#
		volume_limit = []
		( food_max ).times do |c|
			limit = [0, 0, 0, 0, 0]
			limit[0] = ( energy / fct_delta[c][0] ) / 10 if fct_delta[c][0] != 0
			limit[1] = ( protein / fct_delta[c][1] ) / 10 if fct_delta[c][1] != 0
			limit[2] = ( fat / fct_delta[c][2] ) / 10 if fct_delta[c][2] != 0
			limit[3] = ( carbo / fct_delta[c][3] ) / 10 if fct_delta[c][3] != 0
			limit[4] = ( salt / fct_delta[c][4] ) / 10 if fct_delta[c][4] != 0
			volume_limit << limit.max.ceil
		end
		volume_limit[1] = volume_limit[0] if volume_limit[0] < volume_limit[1]
		volume_limit[2] = volume_limit[1] if volume_limit[1] < volume_limit[2]
		volume_limit[3] = volume_limit[2] if volume_limit[2] < volume_limit[3]
		volume_limit[4] = volume_limit[3] if volume_limit[3] < volume_limit[4]

p volume_limit

		#1st pass
		delta_min = -1
		delta_min_vol = []
		dd = 0
		0.upto( volume_limit[0] * 10 ) do |c0|
			0.upto( volume_limit[1] * 10 ) do |c1|
				next if c1 > c0
				0.upto( volume_limit[2] * 10 ) do |c2|
					next if c2 > c1
					0.upto( volume_limit[3] * 10) do |c3|
						next if c3 > c2
						0.upto( volume_limit[4] * 10 ) do |c4|
							next if c4 > c3 || ( c0 + c1 + c2 + c3 + c4 ) > volume

							e_ = ( energy - ( fct_delta[0][0] * c0 ) - ( fct_delta[1][0] * c1 ) - ( fct_delta[2][0] * c2 ) - ( fct_delta[3][0] * c3 ) - ( fct_delta[4][0] * c4 )) ** 2
							p_ = (( protein - ( fct_delta[0][1] * c0 ) - ( fct_delta[1][1] * c1 ) - (fct_delta[2][1] * c2 ) - ( fct_delta[3][1] * c3 ) - ( fct_delta[4][1] * c4 )) * ( energy / protein )) ** 2
							f_ = (( fat - ( fct_delta[0][2] * c0 ) - ( fct_delta[1][2] * c1 ) - ( fct_delta[2][2] * c2 ) - ( fct_delta[3][2] * c3 ) - ( fct_delta[4][2] * c4 )) * ( energy / fat ))  ** 2
							c_ = (( carbo - ( fct_delta[0][3] * c0 ) - ( fct_delta[1][3] * c1 ) - ( fct_delta[2][3] * c2 ) - ( fct_delta[3][3] * c3 ) - ( fct_delta[4][3] * c4 )) * ( energy / carbo )) ** 2
							s_ = (( salt - ( fct_delta[0][4] * c0 ) - ( fct_delta[1][4] * c1 ) - ( fct_delta[2][4] * c2 ) - ( fct_delta[3][4] * c3 ) - ( fct_delta[4][4] * c4 )) * ( energy / salt )) ** 2
							delta = e_ + p_ + f_ + c_ + s_
p delta
							if delta_min > delta || delta_min < 0
								delta_min = delta
								delta_min_vol = [c0, c1, c2, c3, c4]
								dd = ( delta / 5 ) ** 0.5
p delta_min_vol, dd
							end
						end
					end
				end
			end
		end
p delta_min
p delta_min_vol
p dd



	end

when 'cb'


else

	if code != ''
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
		<button type='button' class='btn btn-sm btn-success' onclick="reasoning()">#{lp[6]}</button>
	</div>
</div>
HTML

end

puts html