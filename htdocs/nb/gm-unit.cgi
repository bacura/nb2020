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
if @debug
	puts "command:#{command}<br>\n"
	puts "code:#{code}<br>\n"

end

unith = Hash.new

case command
when 'update'
	0.upto( 6 ) do |c|
		if @cgi["uk#{c}"] != '' && @cgi["uk#{c}"] != nil
			if @cgi["uv#{c}"] != '' && @cgi["uv#{c}"] != nil
				unith[@cgi["uv#{c}"]] = @cgi["uv#{c}"].to_f
			else
				unith[@cgi["uv#{c}"]] = 0.0
			end
		end
	end
	unith['note'] = @cgi['note']

	unit = JSON.generate( unith )
	fn = code.split( ',' )
	fn.each do |e|
		mdb( "UPDATE #{$MYSQL_TB_EXT} SET unit='#{unit}' WHERE FN='#{e}';", false, @debug ) if /\d\d\d\d\d/ =~ e || /P\d\d\d\d\d/ =~ e
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
0.upto( 6 ) do |c|
	unit_html << "<div class='row'>"
	unit_html << "<div class='col-2' align='right'><input type='text' class='form-control form-control-sm' id='uk#{c}' value='#{uk_set[c]}'></div>"
	unit_html << "<div class='col-2' align='right'><input type='number' class='form-control form-control-sm' id='uv#{c}' value='#{uv_set[c]}'></div>"
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
		<div class='col'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{lp[2]}</label>
  				<input type="text" class="form-control" id="food_no" value="#{code}">
				<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"initUnit()\">#{lp[3]}</button>
			</div>
		</div>
	</div><br>

	<div class='row'>
		<div class='col-2' align='center'>単位</div>
		<div class='col-2' align='center'>値</div>
	</div>
	#{unit_html}
	<br>

	<div class='row'>
		<div class='col-1'>#{lp[4]}</div>
	</div>
	<div class='row'>
		<div class='col'><input type='text' class='form-control form-control-sm' id='note' value='#{note}'></div>
	</div><br>

	<div class='row'>
		<div class='col' align='center'><button class='btn btn-outline-danger' type='button' onclick=\"updateUint()\">#{lp[5]}</button></div>
	</div>
</div>
<hr>
#{lp[7]}<br>
#{lp[8]}<br>
#{lp[9]}<br>
HTML

puts html
