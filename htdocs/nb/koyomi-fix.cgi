#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi fix fct editer 0.04b

#==============================================================================
# LIBRARY
#==============================================================================
require './probe'
require './brain'


#==============================================================================
# STATIC
#==============================================================================
script = 'koyomi-fix'
@debug = false


#==============================================================================
# DEFINITION
#==============================================================================

def block_maker(  fix_opt, palette_bit, s, e )
	html  = '<table class="table-sm table-striped" width="100%">'
	s.upto( e ) do |i|
		t = $FCT['I'][i]
		if palette_bit[i] == 1
			html << "<tr><td>#{$FCT['N'][t]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{t}' value=\"#{fix_opt[t].to_f}\"></td><td>#{$FCT['U'][t]}</td></tr>"
		else
			html << "<input type='hidden' value='#{fix_opt[t].to_f}' id='k#{t}'>"
		end
	end
	html << '</table>'

	return html
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


koyomi = Calendar.new( user.name, 0, 0, 0 )
fix_opt = Hash.new


#### POSTデータの取得
command = @cgi['command']
yyyy = @cgi['yyyy']
mm = @cgi['mm']
dd = @cgi['dd']
tdiv = @cgi['tdiv'].to_i
hh_mm = @cgi['hh_mm']
meal_time = @cgi['meal_time'].to_i
order = @cgi['order'].to_i
palette_ = @cgi['palette']
modifyf = @cgi['modifyf'].to_i
food_name = @cgi['food_name']
food_number = @cgi['food_number'].to_i
food_number = 1 if food_number == 0
food_weight = @cgi['food_weight']
food_weight = 100 if food_weight == nil || food_weight == ''|| food_weight == '0'
food_weight = BigDecimal( food_weight )
if @debug
	puts "command: #{command}<br>\n"
	puts "food_name: #{food_name}<br>\n"
	puts "food_weight: #{food_weight}<br>\n"
	puts "food_number: #{food_number}<br>\n"
	puts "yyyy: #{yyyy}<br>\n"
	puts "hh_mm: #{hh_mm}<br>\n"
	puts "meal_time: #{meal_time}<br>\n"
	puts "dd: #{dd}<br>\n"
	puts "tdiv: #{tdiv}<br>\n"
	puts "order: #{order}<br>\n"
	puts "palette_: #{palette_}<br>\n"
	puts "modifyf: #{modifyf}<br>\n"
	puts "<hr>\n"
end


puts 'Getting standard meal start & time<br>' if @debug
start_times = []
meal_tiems = []
r = mdb( "SELECT bio FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, false )
if r.first
	if r.first['bio'] != nil && r.first['bio'] != ''
		bio = JSON.parse( r.first['bio'] )
		start_times = [bio['bst'], bio['lst'], bio['dst']]
		meal_tiems = [bio['bti'].to_i, bio['lti'].to_i, bio['dti'].to_i]
	end
end
hh_mm = start_times[tdiv] if hh_mm == '' || hh_mm == nil
meal_time = meal_tiems[tdiv] if meal_time == 0


puts 'Loading FCT items<br>' if @debug
if command == 'init'
	@fct_start.upto( @fct_end ) do |i| fix_opt[@fct_item[i]] = 0.0 end
end


puts 'Updating fcs & koyomi<br>' if @debug
code = nil
if command == 'save'
	puts 'Calculating fct<br>' if @debug
	@fct_start.upto( @fct_end ) do |i|
		if @cgi[@fct_item[i]] == '' || @cgi[@fct_item[i]] == nil || @cgi[@fct_item[i]] == '-'
			fix_opt[@fct_item[i]] = '-'
		else
			fix_opt[@fct_item[i]] = ( BigDecimal( @cgi[@fct_item[i]] ) / 100 * food_weight * food_number ).round( @fct_frct[@fct_item[i]] )
		end
	end

	puts 'stetting SQL set <br>' if @debug
	fix_set = ''
	@fct_start.upto( @fct_end ) do |i| fix_set << "#{@fct_item[i]}='#{fix_opt[@fct_item[i]]}'," end
	fix_set.chop!

	#### modify
	if  modifyf == 1
		r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
		if r.first
			a = r.first['koyomi'].split( "\t" )[order]
			code = a.split( "~" )[0]
			mdb( "UPDATE #{$MYSQL_TB_FCZ} SET name='#{food_name}', #{fix_set} WHERE user='#{user.name}' AND base='fix' AND code='#{code}';", false, @debug )
		end
		koyomi_update = ''
		r.each do |e|
			a = e['koyomi'].split( "\t" )
			a.size.times do |c|
				if c == order
					aa = a[c].split( "~" )
					koyomi_update << "#{aa[0]}~#{aa[1]}~#{aa[2]}~#{hh_mm}~#{meal_time}\t"
				else
					koyomi_update << "#{t[c]}\t"
				end
			end
		end
		koyomi_update.chop!
		mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi_update}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug)
	else
 		fix_code = generate_code( user.name, 'z' )
		mdb( "INSERT INTO #{$MYSQL_TB_FCZ} SET base='fix', code='#{fix_code}', origin='#{yyyy}-#{mm}-#{dd}-#{tdiv}', name='#{food_name}',user='#{user.name}', #{fix_set};", false, @debug )
		r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )

		if r.first
			koyomi = r.first['koyomi']
			koyomi << "\t#{fix_code}~100~99~#{hh_mm}~#{meal_time}"
			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
		else
			koyomi = "#{fix_code}~100~99~#{hh_mm}~#{meal_time}"
			mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', fzcode='', freeze='0', koyomi='#{koyomi}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}';", false, @debug )
		end
	end
end
if @debug
	puts "fix_opt: #{fix_opt}<br>\n"
	puts "<hr>\n"
end


#### modify
if command == 'modify' || modifyf == 1
	puts 'modify process<br>' if @debug
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
	if r.first
		t = r.first['koyomi'].split( "\t" )[order]
		code = t.split( "~" )[0]

		rr = mdb( "SELECT * FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='fix' AND code='#{code}';", false, @debug )
		if rr.first
			food_name = rr.first['name']
			@fct_start.upto( @fct_end ) do |i| fix_opt[@fct_item[i]] = rr.first[@fct_item[i]].to_f end
		end
	end
	modifyf = 1
end


puts 'Setting palette<br>' if @debug
palette = Palette.new( user.name )
palette.set_bit( palette_ )
palette_html = ''
palette_html << "<div class='input-group input-group-sm'>"
palette_html << "<label class='input-group-text'>#{lp[6]}</label>"
palette_html << "<select class='form-select form-select-sm' id='palette' onChange=\"paletteKoyomi( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}', #{modifyf} )\">"
palette.sets.each_key do |k|
	s = ''
	s = 'SELECTED' if palette_ == k
	palette_html << "<option value='#{k}' #{s}>#{k}</option>"
end
palette_html << "</select>"
palette_html << "</div>"


puts 'HTML FCT block<br>' if @debug
html_fct_blocks = []
fct_start = [ 5, 8, 20, 34, 46, 56 ]
fct_end = [ 7, 19, 33, 45, 55, 57 ]
6.times do |i| html_fct_blocks[i] = block_maker( fix_opt, palette.bit, fct_start[i], fct_end[i] ) end


puts 'SELECT HH block<br>' if @debug
meal_time_set = [5, 10, 15, 20, 30, 45, 60, 90, 120 ]
eat_time_html = "<div class='input-group input-group-sm'>"
eat_time_html << "<label class='input-group-text btn-info' onclick=\"nowKoyomi( 'hh_mm_fix' )\">#{lp[8]}</label>"
eat_time_html << "<input type='time' step='60' id='hh_mm_fix' value='#{hh_mm}' class='form-control' style='min-width:100px;'>"
eat_time_html << "<select id='meal_time_fix' class='form-select form-select-sm'>"
meal_time_set.each do |e|
	s = ''
	s = 'SELECTED' if meal_time == e
	eat_time_html << "	<option value='#{e}' #{s}>#{e}</option>"
end
eat_time_html << "</select>"
eat_time_html << "<label class='input-group-text'>#{lp[9]}</label>"
eat_time_html << "</div>"


puts 'HTML<br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div align='center' class='joystic_koyomi' onclick="koyomiFixR()">#{lp[7]}</div>
	</div>
	<br>
	<div class="row">
		<div class="col-4">
			<input type="text" class="form-control form-control-sm" id="food_name" placeholder="#{lp[3]}" value="#{food_name}">
		</div>
		<div class="col-3">#{eat_time_html}</div>
		<div class="col-3"></div>
		<div class="col-2" align="right">
			<button class='btn btn-success btn-sm' type='button' onclick="koyomiSaveFix( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}', '#{modifyf}', '#{order}' )">#{lp[1]}</button>
		</div>
	</div>
	<br>

	<div class="row">
		<div class="col-3">#{palette_html}</div>
		<div class="col-1"></div>
		<div class="col-3">
			<div class="input-group input-group-sm">
				<div class="form-check">
    				<input type="checkbox" class="form-check-input" id="g100_check" onChange="koyomiG100check()">
    				<label class="form-check-label">#{lp[2]}</label>
  				</div>
  				&nbsp;&nbsp;&nbsp;
				<label class="input-group-text">#{lp[5]}</label>
				<input type="text" class="form-control form-control-sm" id="kffood_weight" placeholder="100" value="#{food_weight.to_f}" disabled>
			</div>
		</div>
		<div class="col-2">
			<div class="input-group input-group-sm">
				<label class="input-group-text">#{lp[12]}</label>
				<input type="number" min='1' class="form-control form-control-sm" id="food_number" placeholder="1">
			</div>
		</div>
	</div>
	<br>

	<div class="row">
		<div class="col-4">#{html_fct_blocks[0]}</div>
		<div class="col-4">#{html_fct_blocks[1]}</div>
		<div class="col-4">#{html_fct_blocks[2]}</div>
	</div>
	<hr>
	<div class="row">
		<div class="col-4">#{html_fct_blocks[3]}</div>
		<div class="col-4">#{html_fct_blocks[4]}</div>
		<div class="col-4">#{html_fct_blocks[5]}</div>
	</div>

	<hr>
</div>
HTML

puts html
