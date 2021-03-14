#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM unit editor 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-unitc'


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


#### GM check
if user.status < 8
	puts "GM error."
	exit
end


#### Getting POST
command = @cgi['command']
code = @cgi['code']
code = '' if code == nil
code.gsub!( /\s/, ',' )
code.gsub!( '　', ',' )
if @debug
	puts "command:#{command}<br>\n"
	puts "code:#{code}<br>\n"

end

unitc2 = 0.0
unitc3 = 0.0
unitc4 = 0.0
unitc5 = 0.0
unitc6 = 0.0
unitc7 = 0.0
unitc8 = 0.0
unitc9 = 0.0
unitc10 = 0.0
unitc11 = 0.0
unitc12 = 0.0
unitc13 = 0.0
unitc14 = 0.0
unitc16 = 0.0
unitc17 = 0.0
notice = ''


case command
when 'update'
	unitc2 = @cgi['unitc2'].gsub( ':', '' ).to_f
	unitc3 = @cgi['unitc3'].gsub( ':', '' ).to_f
	unitc4 = @cgi['unitc4'].gsub( ':', '' ).to_f
	unitc5 = @cgi['unitc5'].gsub( ':', '' ).to_f
	unitc6 = @cgi['unitc6'].gsub( ':', '' ).to_f
	unitc7 = @cgi['unitc7'].gsub( ':', '' ).to_f
	unitc8 = @cgi['unitc8'].gsub( ':', '' ).to_f
	unitc9 = @cgi['unitc9'].gsub( ':', '' ).to_f
	unitc10 = @cgi['unitc10'].gsub( ':', '' ).to_f
	unitc11 = @cgi['unitc11'].gsub( ':', '' ).to_f
	unitc12 = @cgi['unitc12'].gsub( ':', '' ).to_f
	unitc13 = @cgi['unitc13'].gsub( ':', '' ).to_f
	unitc14 = @cgi['unitc14'].gsub( ':', '' ).to_f
	unitc16 = @cgi['unitc16'].gsub( ':', '' ).to_f
	unitc17 = @cgi['unitc17'].gsub( ':', '' ).to_f
	notice = @cgi['notice']

	unitc = "-:-:#{unitc2}:#{unitc3}:#{unitc4}:#{unitc5}:#{unitc6}:#{unitc7}:#{unitc8}:#{unitc9}:#{unitc10}:#{unitc11}:#{unitc12}:#{unitc13}:#{unitc14}:-:#{unitc16}:#{unitc17}:"
	fn = code.split( ',' )
	fn.each do |e|
		mdb( "UPDATE #{$MYSQL_TB_EXT} SET unitc='#{unitc}', unitn='#{notice}' WHERE FN='#{e}';", false, @debug ) if /\d\d\d\d\d/ =~ e
	end
end


unless code == ''
	r = mdb( "SELECT name from #{$MYSQL_TB_TAG} WHERE FN='#{code}';", false, @debug )
	food_name = r.first['name']

	r = mdb( "SELECT * from #{$MYSQL_TB_EXT} WHERE FN='#{code}';", false, @debug )
	if r.first
		t = r.first['unitc']
		t = '-:-:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:0.0:-:0.0:0.0:' if t == nil || t == ''
		unitc = t.split( ':' )
		unitc2 = unitc[2]
		unitc3 = unitc[3]
		unitc4 = unitc[4]
		unitc5 = unitc[5]
		unitc6 = unitc[6]
		unitc7 = unitc[7]
		unitc8 = unitc[8]
		unitc9 = unitc[9]
		unitc10 = unitc[10]
		unitc11 = unitc[11]
		unitc12 = unitc[12]
		unitc13 = unitc[13]
		unitc14 = unitc[14]
		unitc16 = unitc[16]
		unitc17 = unitc[17]
		notice = r.first['unitn']
	end
end

html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: #{food_name}</h5></div>
	</div><br>

	<div class='row'>
		<div class='col-12'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{lp[2]}</label>
  				<input type="text" class="form-control" id="food_no" value="#{code}">
				<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"initUnitc()\">#{lp[3]}</button>
			</div>
		</div>
	</div><br>

	<div class='row'>
		<div class='col-1' align='right'>#{@unit[2]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc2' value='#{unitc2}'></div>
		<div class='col-1' align='right'>#{@unit[3]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc3' value='#{unitc3}'></div>
		<div class='col-1' align='right'>#{@unit[4]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc4' value='#{unitc4}'></div>
		<div class='col-1' align='right'>#{@unit[5]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc5' value='#{unitc5}'></div>
		<div class='col-1' align='right'>#{@unit[6]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc6' value='#{unitc6}'></div>
	</div><br>

	<div class='row'>
		<div class='col-1' align='right'>#{@unit[7]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc7' value='#{unitc7}'></div>
		<div class='col-1' align='right'>#{@unit[8]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc8' value='#{unitc8}'></div>
		<div class='col-1' align='right'>#{@unit[9]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc9' value='#{unitc9}'></div>
	</div><br>

	<div class='row'>
		<div class='col-1' align='right'>#{@unit[10]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc10' value='#{unitc10}'></div>
		<div class='col-1' align='right'>#{@unit[11]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc11' value='#{unitc11}'></div>
		<div class='col-1' align='right'>#{@unit[12]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc12' value='#{unitc12}'></div>
	</div><br>

	<div class='row'>
		<div class='col-1' align='right'>#{@unit[13]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc13' value='#{unitc13}'></div>
		<div class='col-1' align='right'>#{@unit[14]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc14' value='#{unitc14}'></div>
		<div class='col-1' align='right'>#{@unit[16]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc16' value='#{unitc16}'></div>
		<div class='col-1' align='right'>#{@unit[17]}</div>
		<div class='col-1'><input type='text' class='form-control form-control-sm' id='unitc17' value='#{unitc17}'></div>
	</div><br>

	<div class='row'>
		<div class='col-1' align='right'>#{lp[4]}</div>
		<div class='col-11'><input type='text' class='form-control form-control-sm' id='notice' value='#{notice}'></div>
	</div><br>
</div>
<hr>
#{lp[7]}<br>
#{lp[8]}<br>
#{lp[9]}<br>
HTML

puts html
