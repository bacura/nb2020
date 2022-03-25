#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM unit editor 0.10b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-unit'


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
code.gsub!( '、', ',' )
bunit = @cgi['bunit']
aunit = @cgi['aunit']
if @debug
	puts "command:#{command}<br>\n"
	puts "code:#{code}<br>\n"

end

unith = Hash.new

case command
when 'update'
	0.upto( 9 ) do |c|
		if @cgi["uk#{c}"] != '' && @cgi["uk#{c}"] != nil
			if @cgi["uv#{c}"] != '' && @cgi["uv#{c}"] != nil
				unith[@cgi["uk#{c}"]] = @cgi["uv#{c}"].to_f
			else
				unith[@cgi["uk#{c}"]] = 0.0
			end
		end
	end
	unith['note'] = @cgi['note']

	unit = JSON.generate( unith )
	fn = code.split( ',' )
	fn.each do |e|
		mdb( "UPDATE #{$MYSQL_TB_EXT} SET unit='#{unit}' WHERE FN='#{e}';", false, @debug ) if /\d\d\d\d\d/ =~ e || /P\d\d\d\d\d/ =~ e
	end
when 'exunit'
	res = mdb( "SELECT * FROM recipe;", false, @debug )
	res.each do |r|
		ex_flag = false
		if r['sum'] != '' && r['sum'] != nil
			sum_list = []
			food_list = r['sum'].split( "\t" )
			food_list.each do |e|
				a = e.split( ':' )
				if a[2] == bunit
					a[2] = aunit
					ex_flag = true
				end
				sum_list << a.join( ':' )
			end

			if ex_flag
				sum_new = sum_list.join( "\t" )
				mdb( "UPDATE recipe SET sum='#{sum_new}' WHERE user='#{r['user']}' AND code='#{r['code']}';", false, @debug )
			end
		end
	end

	res = mdb( "SELECT * FROM koyomi;", false, @debug )
	res.each do |r|
		ex_flag = false
		if r['koyomi'] != '' && r['koyomi'] != nil && r['tdiv'] != 4
			koyomi_list = []
			food_list = r['koyomi'].split( "\t" )
			food_list.each do |e|
				a = e.split( '~' )
				if a[2] == bunit
					a[2] = aunit
					ex_flag = true
				end
				koyomi_list << a.join( '~' )
			end

			if ex_flag
				koyomi_new = koyomi_list.join( "\t" )
				mdb( "UPDATE koyomi SET koyomi='#{koyomi_new}' WHERE user='#{r['user']}' AND tdiv='#{r['tdiv']}' AND date='#{r['date']}';", false, @debug )
			end
		end
	end
end

uk_set = []
uv_set = []
note = ''
unless code == ''
	puts 'Loading unit JSON<br>' if @debug
	r = mdb( "SELECT name from #{$MYSQL_TB_TAG} WHERE FN='#{code}';", false, @debug )
	food_name = r.first['name']

	r = mdb( "SELECT unit from #{$MYSQL_TB_EXT} WHERE FN='#{code}';", false, @debug )
	if r.first
		if r.first['unit'] != nil && r.first['unit'] != ''
			unitj = JSON.parse( r.first['unit'] )
			unitj.each do |k, v|
				if k == 'note'
					note = v
				else
					uk_set << k
					uv_set << v
				end
			end
		end
	end
end


puts 'Unit HTML<br>' if @debug
unit_html = ''
0.upto( 4 ) do |c|
	unit_html << "<div class='row'>"
	unit_html << "<div class='col' align='right'><input type='text' class='form-control form-control-sm' id='uk#{c * 2}' value='#{uk_set[c * 2]}'></div>"
	unit_html << "<div class='col' align='right'><input type='number' class='form-control form-control-sm' id='uv#{c * 2}' value='#{uv_set[c * 2]}'></div>"
	unit_html << "<div class='col-1'></div>"
	unit_html << "<div class='col' align='right'><input type='text' class='form-control form-control-sm' id='uk#{c * 2 + 1}' value='#{uk_set[c * 2 + 1]}'></div>"
	unit_html << "<div class='col' align='right'><input type='number' class='form-control form-control-sm' id='uv#{c * 2 + 1}' value='#{uv_set[c * 2 + 1]}'></div>"
	unit_html << "</div>"
	unit_html << "<br>"
end


puts 'HTML<br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: #{food_name}</h5></div>
	</div><br>

	<div class='row'>
		<div class='col-6'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{lp[2]}</label>
  				<input type="text" class="form-control" id="food_no" value="#{code}">
				<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"initUnit()\">#{lp[3]}</button>
			</div>
		</div>
	</div><br>

	<div class='row'>
		<div class='col' align='center'>単位</div>
		<div class='col' align='center'>値</div>
		<div class='col-1'></div>
		<div class='col' align='center'>単位</div>
		<div class='col' align='center'>値</div>
	</div>
	#{unit_html}
	<br>

	<div class='row'>
		<div class='col-1'>#{lp[4]}</div>
	</div>
	<div class='row'>
		<div class='col-10'><input type='text' class='form-control form-control-sm' id='note' value='#{note}'></div>
		<div class='col-1'></div>
		<div class='col' align='center'><button class='btn btn-sm btn-outline-danger' type='button' onclick="updateUint()">#{lp[5]}</button></div>
	</div>
	<br>

</div>
<hr>

<div class='row'>
	<div class='col'>#{lp[7]}</div>
	<div class='col'><input type='text' class='form-control form-control-sm' id='bunit' value='' placeholder='#{lp[8]}'></div>
	<div class='col' align="center">#{lp[10]}</div>
	<div class='col'><input type='text' class='form-control form-control-sm' id='aunit' value='' placeholder='#{lp[9]}'></div>
	<div class='col' align='center'><button class='btn btn-sm btn-outline-danger' type='button' onclick="exUnit( '#{code}' )">#{lp[11]}</button></div>
	</div>

HTML

puts html
