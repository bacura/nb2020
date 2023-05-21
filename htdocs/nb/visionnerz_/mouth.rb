#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 visionnerz mouth 0.00b


#==============================================================================
#LIBRARY
#==============================================================================


#==============================================================================
#STATIC
#==============================================================================
script = 'visionnerz'
@debug = false
x_axis = 60 * 24

#koyomi "#{delimiter}#{code}~#{ev}~#{eu}~#{hh_mm}~#{meal_time}"


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
#user.debug if @debug
lp = user.load_lp( script )


# POST
command = @cgi['command']
yyyymmdd = @cgi['yyyymmdd']
regist_s = @cgi['regist_s']
puts command, yyyymmdd, regist_s, '<hr>' if @debug


mybio = Bio.new( user )
mybio.kex_ow
mybio.debug if @debug

case command
when 'raw'
	puts "Palette setting<br>" if @debug
	palette = Palette.new( user.name )
	palette.set_bit( nil )

	fct_slow = []
	0.upto( x_axis ) do |c|
		fct_slow[c] = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
		fct_medium[c] = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
		fct_fast[c] = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
		fct_slow[c].load_palette( palette.bit )
		fct_medium[c].load_palette( palette.bit )
		fct_fast[c].load_palette( palette.bit )
	end


	r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyymmdd}';", false, @debug )
	memo = ''
	r.each do |e|
		if e['tdiv'].to_i == 4
			memo = e['koyomi']
		else
			puts 'Raw<br>' if @debug
			a = []
			a = e['koyomi'].split( "\t" ) if e['koyomi']
			a.each do |ee|
				( code, rate_, unit, hhmm, meal_time ) = ee.split( '~' )
				a = hhmm.split( ':' )
				meal_start = a[0].to_i * 60 + a[1].to_i
				meal_time = meal_time.to_i
				z, rate = food_weight_check( rate_ )

				fct_tmp = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
				fct_tmp.load_palette( palette.bit )

				if /\?/ =~ code
				elsif /\-z\-/ =~ code
					puts 'FIX<br>' if @debug
					fct_tmp.load_fcz( user.name, code, 'fix' )
					fct_tmp.calc
					a = fct_tmp.total.map do |x| x / meal_time end
					0.upto( meal_time ) do |c|
						fct_slow[meal_start + c].into_solid( a ) if ( meal_start + c ) <= x_axis
					end
				else
					puts 'Recipe<br>' if @debug
					recipe_codes = []
					if /\-m\-/ =~ code
						recipe_codes = menu2rc( user.name, code )
					else
						recipe_codes << code
					end

					food_nos = []
					food_weights = []
					recipe_codes.each do |e|
						if /\-r\-/ =~ e || /\w+\-\h{4}\-\h{4}/ =~ e
							fns, fws, z = recipe2fns( user.name, e, rate, unit )
							food_nos.concat( fns )
							food_weights.concat( fws )
						else
							food_nos << code
							food_weights << unit_weight( rate, unit, code )
						end
					end

					puts 'Foods<br>' if @debug
					fct_tmp.set_food( user.name, food_nos, food_weights, false )
					fct_tmp.calc
					a = fct_tmp.total.map do |x| x / meal_time end
					0.upto( meal_time ) do |c|
						fct_slow[meal_start + c].into_solid( a ) if ( meal_start + c ) <= x_axis
					end
				end
			end
		end
	end

	puts "Data generating<br>" if @debug
	hours = []
	energy = []
	protein = []
	fat = []
	carbohydrate = []
	fiber = []
	sodium = []



	0.upto( x_axis ) do |c|
		fct_slow[c].into_solid( fct_slow[c - 1].total ) unless c == 0
		fct_slow[c].calc
		fct_slow[c].digit

		hours << ( c.to_f / 60 ).round( 4 )
		energy << fct_slow[c].pickt( 'ENERC_KCAL' )
		protein << fct_slow[c].pickt( 'PROTV' )
		fat << fct_slow[c].pickt( 'FATV' )
		carbohydrate << fct_slow[c].pickt( 'CHOV' )
		fib = fct_slow[c].pickt( 'fiber' )
		fib = 0 if fib == nil
		fiber << fib
		na = fct_slow[c].pickt( 'NA' )
		na = ( fct_slow[c].pickt( 'NACL_EQ' ) / 2.54 * 1000 ).round( 0 ) if na == nil
		sodium << na
	end

	raw = []
	raw[0] = hours.unshift( lp[4] ).join( ',' )
	raw[1] = energy.unshift( lp[5] ).join( ',' )
	raw[2] = protein.unshift( lp[6] ).join( ',' )
	raw[3] = fat.unshift( lp[7] ).join( ',' )
	raw[4] = carbohydrate.unshift( lp[8] ).join( ',' )
	raw[5] = fiber.unshift( lp[9] ).join( ',' )
	raw[6] = sodium.unshift( lp[10] ).join( ',' )

	puts raw.join( ':' )
	exit( 0 )
else
	html = <<-"HTML"
<div class="row">
<h6>#{yyyymmdd}</h6>
</div>

<hr>
<div class="row">
#{lp[1]}<br>
<div id='visionnerz-digestion' align='center'></div>
</div>

<div class="row">
<div class='col-1'>#{lp[2]}</div>
<div class='col'><div id='visionnerz-blood' align='center'></div></div>
</div>
<div class="row">
<div class='col-1'>#{lp[3]}</div>
<div class='col'><div id='visionnerz-tissue' align='center'></div></div>
</div>
HTML

	puts html
end

#### 検索設定の保存
#recipe_ = JSON.generate( { "range" => range, "type" => type, "role" => role, "tech" => tech, "time" => time, "cost" => cost, "xitem" => xitem, "yitem" => yitem, "zitem" => zitem, "zml" => zml, "zrange" => zrange } )
#mdb( "UPDATE #{$MYSQL_TB_CFG} SET recipe3ds='#{recipe_}' WHERE user='#{user.name}';", false, true )
