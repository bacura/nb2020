#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser print page selector 0.05b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


#==============================================================================
#STATIC
#==============================================================================
script = 'print'
@debug = false


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


puts 'Getting POST<br>' if @debug
command = @cgi['command']
code = @cgi['code']
if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "<hr>"
end


puts 'Checking recipe code<br>' if @debug
r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}';", false, @debug )
unless r.first
	puts "#{lp[1]}(#{code})#{lp[2]}"
	exit( 9 )
end
recipe_name = r.first['name']
recipe_dish = r.first['dish']


puts 'Generating palette HTML<br>' if @debug
palette_html = ''
#### Setting palette
palette_sets = []
palette_name = []
r = mdb( "SELECT * from #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}';", false, @debug )
r.each do |e| palette_name << e['name'] end
palette_name.size.times do |c| palette_html << "<option value='#{palette_name[c]}'>#{palette_name[c]}</option>" end


puts 'Cooking school HTML<br>' if @debug
csc = ''
cs_disabled = ''
if user.status == 5 ||  user.status >= 8
	r = mdb( "SELECT enable FROM #{$MYSQL_TB_SCHOOLC} WHERE user='#{user.name}';", false, @dubug )
	if r.first
		enable = r.first['enable']
		cs_disabled = 'DISABLED' if enable != 1
	else
		cs_disabled = 'DISABLED'
	end
else
	cs_disabled = 'DISABLED'
end

puts 'HTML<br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-6'><h4>#{recipe_name}</h4></div>
		<div align="center" class='col-6 joystic_koyomi' onclick="print_templateReturen()">#{lp[3]}</div>
	</div>
	<br>

	<div class='row'>
		<div class='col-3'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="palette">#{lp[5]}</label>
				<select class="form-select" id="palette">
					#{palette_html}
				</select>
			</div>
		</div>
		<div class='col-3' align='center'>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="frct_accu">#{lp[6]}
			</div>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="ew_mode">#{lp[7]}
			</div>
		</div>
		<div class='col-2'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="frct_mode">#{lp[8]}</label>
				<select class="form-select" id="frct_mode">
					<option value="1">#{lp[9]}</option>
					<option value="2">#{lp[10]}</option>
					<option value="3">#{lp[11]}</option>
				</select>
			</div>
		</div>
		<div class='col-1'></div>
		<div class='col-2'>
			<div class="form-check form-switch">
  				<input class="form-check-input" type="checkbox" id="csc" value='#{csc}' #{cs_disabled}>
  				<label class="form-check-label">#{lp[4]} (#{csc})</label>
			</div>
		</div>
	</div>
	<br>

	<div class='row'>
		<div class='col print_card'>
			<div class="card" style="width: 14rem;" onclick="openPrint( '#{user.name}', '#{code}', '0', '#{recipe_dish}' )">
  				<img class="card-img-top" src="photo_/pvt_sample_2.png" alt="Card image cap">
  				<div class="card-body">
    				<h6 class="card-title">#{lp[13]}</h6>
  				</div>
			</div>
		</div>
		<div class='col print_card'>
			<div class="card" style="width: 14rem;" onclick="openPrint( '#{user.name}', '#{code}', '1', '#{recipe_dish}' )">
  				<img class="card-img-top" src="photo_/pvt_sample_4.png" alt="Card image cap">
  				<div class="card-body">
    				<h6 class="card-title">#{lp[14]}</h6>
  				</div>
			</div>
		</div>
		<div class='col print_card'>
			<div class="card" style="width: 14rem;" onclick="openPrint( '#{user.name}', '#{code}', '2', '#{recipe_dish}' )">
  				<img class="card-img-top" src="photo_/pvt_sample_6.png" alt="Card image cap">
  				<div class="card-body">
    				<h6 class="card-title">#{lp[15]}</h6>
  				</div>
			</div>
		</div>
		<div class='col print_card'>
			<div class="card" style="width: 14rem;" onclick="openPrint( '#{user.name}', '#{code}', '3', '#{recipe_dish}' )">
  				<img class="card-img-top" src="photo_/pvt_sample_8.png" alt="Card image cap">
  				<div class="card-body">
    				<h6 class="card-title">#{lp[16]}</h6>
  				</div>
			</div>
		</div>
	</div>
</div>

HTML

puts html
