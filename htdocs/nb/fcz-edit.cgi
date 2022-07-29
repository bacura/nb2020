#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 fcz editer 0.00b

#==============================================================================
# LIBRARY
#==============================================================================
require './soul'
require './brain'


#==============================================================================
# STATIC
#==============================================================================
script = 'fcz-edit'
@debug = false
reserves = %W( fix freeze recipe )


#==============================================================================
# DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
fct.load_palette( @palette_bit_all )


puts "POST<br>" if @debug
command = @cgi['command']
fcz_code = @cgi['fcz_code']
fcz_name = @cgi['fcz_name']
origin = @cgi['origin']
base = @cgi['base']
puts command, base, fcz_code, fcz_name, origin, '<hr>' if @debug


puts "Loading fcz<br>" if @debug
if command == 'init' && fcz_code != 'new'
	r = mdb( "SELECT origin, name FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='#{base}' AND code='#{fcz_code}';", false, @debug )
	if r.first
		fcz_name = r.first['name']
		origin = r.first['origin']

		fct.load_fcz( user.name, fcz_code, base )
		fct.calc
	end
end


reserve_flag = false
reserves.each do |e|
	reserve_flag = true if e == base
end


if command == 'save'
	puts 'Making fct_sql set<br>' if @debug
	fct.load_cgi( @cgi )
	fct.calc

	if fcz_code == 'new' || fcz_code == ''
		puts 'Generating new Food number:' if @debug
		fcz_code = generate_code( user.name, 'z' )

		mdb( "INSERT INTO #{$MYSQL_TB_FCZ} SET user='#{user.name}', base='#{base}', code='#{fcz_code}', origin='#{origin}', name='#{fcz_name}', #{fct.sql};", false, @debug )
	else
		mdb( "UPDATE #{$MYSQL_TB_FCZ} SET base='#{base}', origin='#{origin}',  name='#{fcz_name}', #{fct.sql} WHERE code='#{fcz_code}' AND user='#{user.name}';", false, @debug )
	end
end


#### disable option
disabled_option = ''
disabled_option = 'disabled' if reserve_flag


puts "FCT_block HTML<Br>" if @debug
fct_block = ['', '', '', '', '', '', '']
@fct_ew.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[0] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='z#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
@fct_pf.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[1] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='z#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
@fct_cho.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[2] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='z#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
@fct_m.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[3] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='z#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
@fct_fsv.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[4] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='z#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
@fct_wsv.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[5] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='z#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
fct_block[5] << "<tr><td><hr></td></tr>"
@fct_as.each do |e|
	t = nil
	t = fct.pickt( e ) if fct.pickt( e ) == nil || fct.pickt( e ) == ''
	fct_block[5] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='z#{e}' value=\"#{fct.pickt(e)}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end


puts "Save button<br>" if @debug
save_button = ''
save_button = "<button class=\"btn btn-outline-primary btn-sm\" type=\"button\" onclick=\"saveFCZedit( '#{fcz_code}' )\">#{lp[4]}</button>" unless reserve_flag


puts "HTML<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col"><h5>#{fcz_code}</h5></div>
		<div align='center' class='col joystic_koyomi' onclick="fczlReturn()">#{lp[5]}</div>
		<div class="col-1" align="right">#{save_button}</div>
	</div>
	<br>

	<div class="row">
		<div class="col-2">
			<div class="input-group input-group-sm">
				<label class="input-group-text">#{lp[1]}</label>
				<input type="text" class="form-control form-control-sm" max='16' id="base" value="#{base}">
			</div>
		</div>
		<div class="col-5">
			<div class="input-group input-group-sm">
				<label class="input-group-text">#{lp[2]}</label>
				<input type="text" class="form-control form-control-sm" max='64' id="fcz_name" value="#{fcz_name}">
			</div>
		</div>
		<div class="col-5">
			<div class="input-group input-group-sm">
				<label class="input-group-text">#{lp[3]}</label>
				<input type="text" class="form-control form-control-sm" max='64' id="origin" value="#{origin}">
			</div>

		</div>
	</div>

	<hr>

	<div class="row">
		<div class="col-4">
			<table class="table-sm table-striped" width="100%">#{fct_block[0]}</table>
		</div>

		<div class="col-4">
			<table class="table-sm table-striped" width="100%">#{fct_block[1]}</table>
		</div>

		<div class="col-4">
			<table class="table-sm table-striped" width="100%">#{fct_block[2]}</table>
		</div>
	</div>

	<hr>

	<div class="row">
		<div class="col-4">
			<table class="table-sm table-striped" width="100%">#{fct_block[3]}</table>
		</div>

		<div class="col-4">
			<table class="table-sm table-striped" width="100%">#{fct_block[4]}</table>
		</div>

		<div class="col-4">
			<table class="table-sm table-striped" width="100%">#{fct_block[5]}</table>
		</div>
	</div>
</div>


HTML

puts html
