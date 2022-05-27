#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 visionnerz 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
script = 'visionnerz'
@debug = false
x_axis = 60 * 24

#koyomi "#{delimiter}#{code}~#{ev}~#{eu}~#{hh_mm}~#{meal_time}"
palette_bit = '00000011001001000000000011000000000001100000000000000000000000000000000011'.split( '' )
palette_bit.map! do |x| x.to_i end
#

#==============================================================================
#DEFINITION
#==============================================================================
class DOFC
	attr_accessor :fc

	def initialize()
		@fc = Hash.new
		@fc['protein'] = 0.0
		@fc['protein_'] = 0.0
		@fc['sugars']= 0.0
		@fc['sugars_'] = 0.0
		@fc['fat'] = 0.0
		@fc['fat_'] = 0.0
		@fc['fiber']= 0.0
		@fc['water'] = 0.0
		@fc['sodium'] = 0.0
		@fc['potassium'] = 0.0
		@fc['alcohol'] = 0.0
	end

	def copy( source )
		source.fc.each do |k, v| @fc[k] = v end
	end

	def plus( source )
		source.fc.each do |k, v| @fc[k] += v end
	end
end


class Oral
	def initialize( debug )
		@stock = DOFC.new
		@post = DOFC.new
		@debug = debug
	end

	def in( fct_slow, fct_fast )
		@stock.fc['protein'] = fct_slow.pickt( 'PROTV' )
		@stock.fc['protein_'] = fct_fast.pickt( 'PROTV' )

		@stock.fc['sugars'] = fct_slow.pickt( 'CHOV' )
		@stock.fc['sugars_'] = fct_fast.pickt( 'CHOV' )

		@stock.fc['fat'] = fct_slow.pickt( 'FATV' )
		@stock.fc['fat_'] = fct_fast.pickt( 'FATV' )

		@stock.fc['fiber'] = fct_slow.pickt( 'FIB' )
		@stock.fc['fiber'] += fct_fast.pickt( 'FIB' )

		@stock.fc['water'] =  fct_slow.pickt( 'WATER' )
		@stock.fc['water'] += fct_fast.pickt( 'WATER' )

		na = fct_slow.pickt( 'NA' )
		na = ( fct_slow.pickt( 'NACL_EQ' ) / 2.54 * 1000 ).round( 0 ) if na == nil
		@stock.fc['sodium'] = na

		na = fct_fast.pickt( 'NA' )
		na = ( fct_fast.pickt( 'NACL_EQ' ) / 2.54 * 1000 ).round( 0 ) if na == nil
		@stock.fc['sodium'] += na

		@stock.fc['potassium'] = fct_slow.pickt( 'K' )
		@stock.fc['potassium'] += fct_fast.pickt( 'K' )

		@stock.fc['alcohol'] = fct_slow.pickt( 'ALC' )
		@stock.fc['alcohol'] += fct_fast.pickt( 'ALC' )
	end

	def function()
		##############################################
		# alpha-amylase
		# feeling
		##############################################
		k = 0.01
		max = 1
		imp = @stock.fc['sugars'] * k
		imp = 1 if imp > max
		@stock.fc['sugars'] -= imp
		@stock.fc['sugars_'] += imp
	end

	def out()
		@post.copy( @stock )

		return @post
	end
end

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
	puts "making meal time table<br>" if @debug

	fct_slow = []
	fct_fast = []
	0.upto( x_axis ) do |c|
		fct_slow[c] = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
		fct_fast[c] = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
		fct_slow[c].load_palette( palette_bit )
		fct_fast[c].load_palette( palette_bit )
	end

	r = mdb( "SELECT koyomi, tdiv FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyymmdd}';", false, @debug )
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


				if /\?/ =~ code
				elsif /\-z\-/ =~ code
					puts 'FIX<br>' if @debug
					fct_tmp = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
					fct_tmp.load_palette( palette_bit )
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
					fct_tmp_slow = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
					fct_tmp_fast = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
					fct_tmp_slow.load_palette( palette_bit )
					fct_tmp_fast.load_palette( palette_bit )

					food_nos_slow = []
					food_nos_fast = []
					food_weights_slow = []
					food_weights_fast = []

					food_nos.size.times do |c|
						fg = food_nos[c].sub( /P|U/, '' ).slice( 0..1 )
						case fg
						when '03', '07', '16', '17'
							food_nos_fast << food_nos[c]
							food_weights_fast << food_weights[c]
						else
							food_nos_slow << food_nos[c]
							food_weights_slow << food_weights[c]
						end
					end

					fct_tmp_slow.set_food( user.name, food_nos_slow, food_weights_slow, false )
					fct_tmp_fast.set_food( user.name, food_nos_fast, food_weights_fast, false )
					fct_tmp_slow.calc
					fct_tmp_fast.calc
					a = fct_tmp_slow.total.map do |x| x / meal_time end
					0.upto( meal_time ) do |c|
						fct_slow[meal_start + c].into_solid( a ) if ( meal_start + c ) <= x_axis
					end
					a = fct_tmp_fast.total.map do |x| x / meal_time end
					0.upto( meal_time ) do |c|
						fct_fast[meal_start + c].into_solid( a ) if ( meal_start + c ) <= x_axis
					end
				end
			end
		end
	end

	puts "Data generating<br>" if @debug
	fc_final = DOFC.new
	oral = Oral.new( @debug )

	hours = []
	protein = []
	protein_ = []
	sugars = []
	sugars_ = []
	fat = []
	fat_ = []
	fiber = []
	sodium = []
	potassium = []
	water = []
	alcohol = []
	0.upto( x_axis ) do |c|
		fct_slow[c].calc
		fct_fast[c].calc
		fct_slow[c].digit
		fct_fast[c].digit

		oral.in( fct_slow[c], fct_fast[c] )
		oral.function
		fc_final.copy( oral.out )

		hours << ( c.to_f / 60 ).round( 4 )
		protein << fc_final.fc['protein']
		protein_ << fc_final.fc['protein_']
		fat << fc_final.fc['fat']
		fat_ << fc_final.fc['fat_']
		sugars << fc_final.fc['sugars']
		sugars_ << fc_final.fc['sugars_']
		sodium << fc_final.fc['sodium']
		potassium << fc_final.fc['potassium']
		fiber << fc_final.fc['fiber']
		water << fc_final.fc['water']
		alcohol << fc_final.fc['alcohol']
	end

	puts "Data binding<br>" if @debug
	raw = []
	raw[0] = hours.unshift( '時間' ).join( ',' )
	raw[1] = protein.unshift( 'たんぱく質' ).join( ',' )
	raw[2] = protein_.unshift( 'たんぱく質_' ).join( ',' )
	raw[3] = fat.unshift( '脂質' ).join( ',' )
	raw[4] = fat_.unshift( '脂質_' ).join( ',' )
	raw[5] = sugars.unshift( '糖質' ).join( ',' )
	raw[6] = sugars_.unshift( '糖質_' ).join( ',' )
	raw[7] = sodium.unshift( 'ナトリウム' ).join( ',' )
	raw[8] = potassium.unshift( 'カリウム' ).join( ',' )
	raw[9] = fiber.unshift( '食物繊維' ).join( ',' )
	raw[10] = water.unshift( '水分' ).join( ',' )
	raw[11] = alcohol.unshift( 'アルコール' ).join( ',' )

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
