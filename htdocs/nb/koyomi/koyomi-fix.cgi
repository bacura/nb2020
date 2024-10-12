#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi fix fct editer 0.2.1 (2024/08/18)

#==============================================================================
# STATIC
#==============================================================================
@debug = false
script = File.basename( $0, '.cgi' )

#==============================================================================
# LIBRARY
#==============================================================================
require '../soul'
require '../brain'
require '../body'


#==============================================================================
# LANGUAGE PACK
#==============================================================================
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'save' 		=> "保 存",\
		'g100' 		=> "100 g相当",\
		'food_n' 	=> "食品名",\
		'food_g'	=> "食品群",\
		'weight'	=> "重量(g)",\
		'palette'	=> "パレット",\
		'min'		=> "分間",\
		'week'		=> "-- １週間以内 --",\
		'month'		=> "-- １ヶ月以内 --",\
		'volume'	=> "個数",\
		'carry_on'	=> "時間継承",\
		'reference'	=> "参照",\
		'history'	=> "履歴",\
		'signpost'	=> "<img src='bootstrap-dist/icons/signpost-r.svg' style='height:2em; width:2em;'>",\
		'clock'		=> "<img src='bootstrap-dist/icons/clock.svg' style='height:1.5em; width:1.5em;'>"
	}

	return l[language]
end

#==============================================================================
# METHODS
#==============================================================================



#==============================================================================
# MAIN
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
db = Db.new( user, @debug, false )
koyomi = Calendar.new( user.name, 0, 0, 0 )


puts 'POST<br>' if @debug
p @cgi if @debug
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
carry_on = @cgi['carry_on']
carry_on = 1 if @cgi['carry_on'] == ''
carry_on = carry_on.to_i
food_name = @cgi['food_name']
food_number = @cgi['food_number'].to_i
food_number = 1 if food_number == 0
food_weight = @cgi['food_weight']
food_weight = 100 if food_weight == nil || food_weight == ''|| food_weight == '0'
food_weight = BigDecimal( food_weight )


puts 'Getting standard meal start & time<br>' if @debug
start_times = []
meal_tiems = []
r = db.query( "SELECT bio FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false )
if r.first
	if r.first['bio'] != nil && r.first['bio'] != ''
		bio = JSON.parse( r.first['bio'] )
		start_times = [bio['bst'], bio['lst'], bio['dst']]
		meal_tiems = [bio['bti'].to_i, bio['lti'].to_i, bio['dti'].to_i]
	end
end
hh_mm = start_times[tdiv] if hh_mm == '' || hh_mm == nil
hh_mm = @time_now.strftime( "%H:%M" ) if hh_mm == '' || hh_mm == nil
meal_time = meal_tiems[tdiv] if meal_time == 0


puts 'Loading FCT items<br>' if @debug
fix_opt = Hash.new
if command == 'init'
	@fct_min_nr.each do |e| fix_opt[e] = nil end
end


puts 'Updating fcs & koyomi<br>' if @debug
code = nil
if command == 'save'
	puts 'Calculating fct<br>' if @debug
	@fct_min_nr.each do |e|
		if @cgi[e] == '' || @cgi[e] == nil || @cgi[e] == '-'
			fix_opt[e] = 0.0
		else
			fix_opt[e] = ( BigDecimal( @cgi[e] ) / 100 * food_weight * food_number ).round( @fct_frct[e] )
		end
	end

	puts 'stetting SQL set <br>' if @debug
	fix_set = ''
	@fct_min_nr.each do |e| fix_set << "#{e}='#{fix_opt[e]}'," end
	fix_set.chop!

	#### modify
	if  modifyf == 1
		r = db.query( "SELECT koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false )
		if r.first
			a = r.first['koyomi'].split( "\t" )[order]
			code = a.split( "~" )[0]
			db.query( "UPDATE #{$MYSQL_TB_FCZ} SET name='#{food_name}', date='#{yyyy}-#{mm}-#{dd}', #{fix_set} WHERE user='#{user.name}' AND base='fix' AND code='#{code}';", true )
		end
		koyomi_update = ''
		delimiter = "\t"
		r.each do |e|
			a = e['koyomi'].split( delimiter )
			a.size.times do |c|
				if c == order
					koyomi_update << "#{delimiter}#{fix_code}~100~99~#{hh_mm}~#{meal_time}"
				else
					koyomi_update << "#{a[c]}\t"
				end
			end
		end
		koyomi_update.chop!
		db.query( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi_update}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", true )
	else
 		fix_code = generate_code( user.name, 'z' )
		db.query( "INSERT INTO #{$MYSQL_TB_FCZ} SET base='fix', code='#{fix_code}', origin='#{yyyy}-#{mm}-#{dd}-#{tdiv}', date='#{yyyy}-#{mm}-#{dd}', name='#{food_name}',user='#{user.name}', #{fix_set};", true )
		r = db.query( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false )
		if r.first
			koyomi = r.first['koyomi']
			delimiter = ''
			if koyomi != ''
				delimiter = "\t"
				if carry_on == 1
					a = koyomi.split( delimiter )
					aa = a.last.split( '~' )
					hh_mm = aa[3]
					meal_time = aa[4]
				end
			end
			koyomi << "#{delimiter}#{fix_code}~100~99~#{hh_mm}~#{meal_time}"
			db.query( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", true )
		else
			koyomi = "#{fix_code}~100~99~#{hh_mm}~#{meal_time}"
			db.query( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', fzcode='', freeze='0', koyomi='#{koyomi}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}';", true )
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
	r = db.query( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false )
	if r.first
		a = r.first['koyomi'].split( "\t" )[order]
		aa = a.split( "~" )
		code = aa[0]
		hh_mm = aa[3]
		meal_time = aa[4].to_i
		rr = db.query( "SELECT * FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='fix' AND code='#{code}';", false )
		if rr.first
			food_name = rr.first['name']
			@fct_min_nr.each do |e| fix_opt[e] = rr.first[e].to_f end
		end
	end
	modifyf = 1
end


#### history
if command == 'history'
	puts 'HISTORY<br>' if @debug
	fix_his_code = @cgi['fix_his_code']
	r = db.query( "SELECT * FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='fix' AND code='#{fix_his_code}';", false )
	if r.first
		food_name = r.first['name']
		@fct_min_nr.each do |e| fix_opt[e] = r.first[e].to_f end
	end
end


puts 'Setting palette<br>' if @debug
palette = Palette.new( user.name )
palette.set_bit( palette_ )
palette_html = ''
palette_html << "<div class='input-group input-group-sm'>"
palette_html << "<label class='input-group-text'>#{l['palette']}</label>"
palette_html << "<select class='form-select form-select-sm' id='palette' onChange=\"selectKoyomiPalette( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}', #{modifyf} )\">"
palette.sets.each_key do |k|
	s = ''
	s = 'SELECTED' if palette_ == k
	palette_html << "<option value='#{k}' #{s}>#{k}</option>"
end
palette_html << "</select>"
palette_html << "</div>"


puts 'HTML FCT block<br>' if @debug
html_fct_blocks = []
html_fct_blocks[0] = '<table class="table-sm table-striped" width="100%">'
@fct_ew.each do |e|
	po = @fct_item.index( e )
	if palette.bit[po] == 1
		html_fct_blocks[0] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%'><input type='text' class='form-control form-control-sm' id='kf#{e}' value=\"#{fix_opt[e]}\"></td><td>#{@fct_unit[e]}</td></tr>"
	else
		html_fct_blocks[0] << "<input type='hidden' value='0.0' id='kf#{e}'>"
	end
end
html_fct_blocks[0] << '</table>'

html_fct_blocks[1] = '<table class="table-sm table-striped" width="100%">'
@fct_pf.each do |e|
	po = @fct_item.index( e )
	if palette.bit[po] == 1
		html_fct_blocks[1] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%'><input type='text' class='form-control form-control-sm' id='kf#{e}' value='#{fix_opt[e]}'></td><td>#{@fct_unit[e]}</td></tr>"
	else
		html_fct_blocks[1] << "<input type='hidden' value='0.0' id='kf#{e}'>"
	end
end
html_fct_blocks[1] << '</table>'

html_fct_blocks[2] = '<table class="table-sm table-striped" width="100%">'
@fct_cho.each do |e|
	po = @fct_item.index( e )
	if palette.bit[po] == 1
		html_fct_blocks[2] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%'><input type='text' class='form-control form-control-sm' id='kf#{e}' value='#{fix_opt[e]}'></td><td>#{@fct_unit[e]}</td></tr>"
	else
		html_fct_blocks[2] << "<input type='hidden' value='0.0' id='kf#{e}'>"
	end
end
html_fct_blocks[2] << '</table>'

html_fct_blocks[3] = '<table class="table-sm table-striped" width="100%">'
@fct_m.each do |e|
	po = @fct_item.index( e )
	if palette.bit[po] == 1
		html_fct_blocks[3] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%'><input type='text' class='form-control form-control-sm' id='kf#{e}' value='#{fix_opt[e]}'></td><td>#{@fct_unit[e]}</td></tr>"
	else
		html_fct_blocks[3] << "<input type='hidden' value='0.0' id='kf#{e}'>"
	end
end
html_fct_blocks[3] << '</table>'

html_fct_blocks[4] = '<table class="table-sm table-striped" width="100%">'
@fct_fsv.each do |e|
	po = @fct_item.index( e )
	if palette.bit[po] == 1
		html_fct_blocks[4] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%'><input type='text' class='form-control form-control-sm' id='kf#{e}' value='#{fix_opt[e]}'></td><td>#{@fct_unit[e]}</td></tr>"
	else
		html_fct_blocks[4] << "<input type='hidden' value='0.0' id='kf#{e}'>"
	end
end
html_fct_blocks[4] << '</table>'

html_fct_blocks[5] = '<table class="table-sm table-striped" width="100%">'
@fct_wsv.each do |e|
	po = @fct_item.index( e )
	if palette.bit[po] == 1
		html_fct_blocks[5] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%'><input type='text' class='form-control form-control-sm' id='kf#{e}' value='#{fix_opt[e].to_f}'></td><td>#{@fct_unit[e]}</td></tr>"
	else
		html_fct_blocks[5] << "<input type='hidden' value='0.0' id='kf#{e}'>"
	end
end
@fct_as.each do |e|
	po = @fct_item.index( e )
	if palette.bit[po] == 1
		html_fct_blocks[5] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%'><input type='text' class='form-control form-control-sm' id='kf#{e}' value='#{fix_opt[e].to_f}'></td><td>#{@fct_unit[e]}</td></tr>"
	else
		html_fct_blocks[5] << "<input type='hidden' value='0.0' id='kf#{e}'>"
	end
end
html_fct_blocks[5] << '</table>'

puts 'SELECT HH block<br>' if @debug
meal_time_set = [5, 10, 15, 20, 30, 45, 60, 90, 120 ]
eat_time_html = "<div class='input-group input-group-sm'>"
eat_time_html << "<button class='btn btn-info' onclick=\"nowKoyomi( 'hh_mm_fix' )\">#{l['clock']}</button>"
eat_time_html << "<input type='time' step='60' id='hh_mm_fix' value='#{hh_mm}' class='form-control' style='min-width:100px;'>"
eat_time_html << "<select id='meal_time_fix' class='form-select form-select-sm'>"
meal_time_set.each do |e|
	s = ''
	s = 'SELECTED' if meal_time == e
	eat_time_html << "	<option value='#{e}' #{s}>#{e}</option>"
end
eat_time_html << "</select>"
eat_time_html << "<label class='input-group-text'>#{l['min']}</label>"
eat_time_html << "</div>"


#### carry_on_check
carry_on_disabled = ''
if command == 'modify'
	carry_on = 0
	carry_on_disabled = 'DISABLED'
end
carry_on_html = "<input class='form-check-input' type='checkbox' id='carry_on' #{$CHECK[carry_on]} #{carry_on_disabled}>"
carry_on_html << "<label class='form-check-label'>#{l['carry_on']}</label>"


#### fix_his
fix_his_html = ''
his_today = @time_now.strftime( "%Y-%m-%d" )
his_w1 = ( @time_now - ( 60 * 60 * 24 * 7 )).strftime( "%Y-%m-%d" )
his_w1_ = ( @time_now - ( 60 * 60 * 24 * 8 )).strftime( "%Y-%m-%d" )
his_m1 = ( @time_now - ( 60 * 60 * 24 * 30 )).strftime( "%Y-%m-%d" )

r = db.query( "SELECT code, name, origin FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='fix' AND date BETWEEN '#{his_w1}' AND '#{his_today}' GROUP BY name;", false )
rr = db.query( "SELECT code, name, origin FROM #{$MYSQL_TB_FCZ} WHERE user='#{user.name}' AND base='fix' AND date BETWEEN '#{his_m1}' AND '#{his_w1_}' GROUP BY name;", false )
fix_his_html << "<div class='input-group input-group-sm'>"

fix_his_html << "<label class='input-group-text'>#{l['history']}</label>"
fix_his_html << "<select class='form-select form-select-sm' id='fix_his_code' onchange=\"selectKoyomiHis( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}' )\">"
fix_his_html << "<option value='' >#{l['week']}</option>"
r.each do |e| fix_his_html << "<option value='#{e['code']}'>#{e['name']} (#{e['origin']})</option>" end
fix_his_html << "<option value='' >#{l['month']}</option>"
rr.each do |e| fix_his_html << "<option value='#{e['code']}'>#{e['name']} (#{e['origin']})</option>" end
fix_his_html << '</select>'
fix_his_html << "</div>"


fix_ref_html = ''
fix_ref_html << '<div class="form-check form-switch">'
fix_ref_html << "<input class='form-check-input' type='checkbox' id='fix_ref' onChange=\"checkKyomiAsRef()\" #{$CHECK[command == 'history']} #{$DISABLE[command != 'history']}>"
fix_ref_html << "<label class='form-check-label' for='fix_ref'>#{l['reference']}</label>"
fix_ref_html << '</div>'


puts 'HTML<br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			#{fix_his_html}
		</div>
		<div class="col-1">
			#{fix_ref_html}
		</div>
		<div class="col-7">
			<div align='center' class='joystic_koyomi' onclick="returnFix2Edit()">#{l['signpost']}</div>
		</div>
	</div>
	<br>
	<div class="row">
		<div class="col input-group input-group-sm">
			<label class='input-group-text'>#{l['food_n']}</label>
			<input type="text" class="form-control form-control-sm" id="food_name" value="#{food_name}">
		</div>
		<div class="col">#{eat_time_html}</div>
		<div class="col">#{carry_on_html}</div>
	</div>
	<br>

	<div class="row">
		<div class="col">#{palette_html}</div>
		<div class="col"></div>
		<div class="col input-group input-group-sm">
			<div class="form-check">
				<input type="checkbox" class="form-check-input" id="g100_check" onChange="checkKyomiXOR100g()">
				<label class="form-check-label">#{l['g100']}</label>
				</div>
				&nbsp;&nbsp;&nbsp;
			<label class="input-group-text">#{l['weight']}</label>
			<input type="text" class="form-control form-control-sm" id="kffood_weight" placeholder="100" value="#{food_weight.to_f}" disabled>
		</div>
		<div class="col input-group input-group-sm">
			<label class="input-group-text">#{l['volume']}</label>
			<input type="number" min='1' class="form-control form-control-sm" id="food_number" placeholder="1">
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
	<br>

	<div class="row">
		<button class='btn btn-success btn-sm' type='button' onclick="saveKoyomiFix( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}', '#{modifyf}', '#{order}' )">#{l['save']}</button>
	</div>

</div>
HTML

puts html

#==============================================================================
#FRONT SCRIPT
#==============================================================================
if command = 'init'
	js = <<-"JS"
<script type='text/javascript'>

// Koyomi fix save
var saveKoyomiFix = function( yyyy, mm, dd, tdiv, modifyf, order ){
	const food_name = $( "#food_name" ).val();
	const hh_mm = $( "#hh_mm_fix" ).val();
	const meal_time = $( "#meal_time_fix" ).val();
	const food_number = $( "#food_number" ).val();
	let carry_on = 0;
	if( $( "#carry_on" ).is( ":checked" )){ carry_on = 1; }

	if( food_name != '' ){
		let food_weight = 100;
		if( $( "#g100_check" ).is( ":checked" )){ food_weight = $( "#kffood_weight" ).val(); }
		const ENERC = $( "#kfENERC" ).val();
		const ENERC_KCAL = $( "#kfENERC_KCAL" ).val();
		const WATER = $( "#kfWATER" ).val();

		const PROTCAA = $( "#kfPROTCAA" ).val();
		const PROT = $( "#kfPROT" ).val();
		const PROTV = $( "#kfPROTV" ).val();
		const FATNLEA = $( "#kfFATNLEA" ).val();
		const CHOLE = $( "#kfCHOLE" ).val();
		const FAT = $( "#kfFAT" ).val();
		const FATV = $( "#kfFATV" ).val();
		const CHOAVLM = $( "#kfCHOAVLM" ).val();
		const CHOAVL = $( "#kfCHOAVL" ).val();
		const CHOAVLDF = $( "#kfCHOAVLDF" ).val();
		const CHOV = $( "#kfCHOV" ).val();
		const FIB = $( "#kfFIB" ).val();
		const POLYL = $( "#kfPOLYL" ).val();
		const CHOCDF = $( "#kfCHOCDF" ).val();
		const OA = $( "#kfOA" ).val();

		const ASH = $( "#kfASH" ).val();
		const NA = $( "#kfNA" ).val();
		const K = $( "#kfK" ).val();
		const CA = $( "#kfCA" ).val();
		const MG = $( "#kfMG" ).val();
		const P = $( "#kfP" ).val();
		const FE = $( "#kfFE" ).val();
		const ZN = $( "#kfZN" ).val();
		const CU = $( "#kfCU" ).val();
		const MN = $( "#kfMN" ).val();
		const ID = $( "#kfID" ).val();
		const SE = $( "#kfSE" ).val();
		const CR = $( "#kfCR" ).val();
		const MO = $( "#kfMO" ).val();

		const RETOL = $( "#kfRETOL" ).val();
		const CARTA = $( "#kfCARTA" ).val();
		const CARTB = $( "#kfCARTB" ).val();
		const CRYPXB = $( "#kfCRYPXB" ).val();
		const CARTBEQ = $( "#kfCARTBEQ" ).val();
		const VITA_RAE = $( "#kfVITA_RAE" ).val();
		const VITD = $( "#kfVITD" ).val();
		const TOCPHA = $( "#kfTOCPHA" ).val();
		const TOCPHB = $( "#kfTOCPHB" ).val();
		const TOCPHG = $( "#kfTOCPHG" ).val();
		const TOCPHD = $( "#kfTOCPHD" ).val();
		const VITK = $( "#kfVITK" ).val();

		const THIA = $( "#kfTHIA" ).val();
		const RIBF = $( "#kfRIBF" ).val();
		const NIA = $( "#kfNIA" ).val();
		const NE = $( "#kfNE" ).val();
		const VITB6A = $( "#kfVITB6A" ).val();
		const VITB12 = $( "#kfVITB12" ).val();
		const FOL = $( "#kfFOL" ).val();
		const PANTAC = $( "#kfPANTAC" ).val();
		const BIOT = $( "#kfBIOT" ).val();
		const VITC = $( "#kfVITC" ).val();

		const ALC = $( "#kfALC" ).val();
		const NACL_EQ = $( "#kfNACL_EQ" ).val();

		const FASAT = $( "#kfFASAT" ).val();
		const FAMS = $( "#kfFAMS" ).val();
		const FAPU = $( "#kfFAPU" ).val();
		const FAPUN3 = $( "#kfFAPUN3" ).val();
		const FAPUN6 = $( "#kfFAPUN6" ).val();

		const FIBTG = $( "#kfFIBTG" ).val();
		const FIBSOL = $( "#kfFIBSOL" ).val();
		const FIBINS = $( "#kfFIBINS" ).val();
		const FIBTDF = $( "#kfFIBTDF" ).val();
		const FIBSDFS = $( "#kfFIBSDFS" ).val();
		const FIBSDFP = $( "#kfFIBSDFP" ).val();
		const FIBIDF = $( "#kfFIBIDF" ).val();
		const STARES = $( "#kfSTARES" ).val();

		$.post( kp + "koyomi-fix.cgi", {
			command:'save', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh_mm:hh_mm, meal_time,meal_time,
			food_name:food_name, food_weight:food_weight, food_number:food_number, modifyf:modifyf, carry_on:carry_on, order:order,
			ENERC:ENERC, ENERC_KCAL:ENERC_KCAL, WATER:WATER,
			PROTCAA:PROTCAA, PROT:PROT, PROTV:PROTV, FATNLEA:FATNLEA, CHOLE:CHOLE, FAT:FAT, FATV:FATV, CHOAVLM:CHOAVLM, CHOAVL:CHOAVL, CHOAVLDF:CHOAVLDF, CHOV:CHOV, FIB:FIB, POLYL:POLYL, CHOCDF:CHOCDF, OA:OA,
			ASH:ASH, NA:NA, K:K, CA:CA, MG:MG, P:P, FE:FE, ZN:ZN, CU:CU, MN:MN, ID:ID, SE:SE, CR:CR, MO:MO,
			RETOL:RETOL, CARTA:CARTA, CARTB:CARTB, CRYPXB:CRYPXB, CARTBEQ:CARTBEQ, VITA_RAE:VITA_RAE, VITD:VITD, TOCPHA:TOCPHA, TOCPHB:TOCPHB, TOCPHG:TOCPHG, TOCPHD:TOCPHD, VITK:VITK,
			THIA:THIA, RIBF:RIBF, NIA:NIA, NE:NE, VITB6A:VITB6A, VITB12:VITB12, FOL:FOL, PANTAC:PANTAC, BIOT:BIOT, VITC:VITC,
			ALC:ALC, NACL_EQ:NACL_EQ,
			FASAT:FASAT, FAMS:FAMS, FAPU:FAPU, FAPUN3:FAPUN3, FAPUN6:FAPUN6,
			FIBTG:FIBTG, FIBSOL:FIBSOL, FIBINS:FIBINS, FIBTDF:FIBTDF, FIBSDFS:FIBSDFS, FIBSDFP:FIBSDFP, FIBIDF:FIBIDF, STARES:STARES
		}, function( data ){
//			$( "#L3" ).html( data );

			const yyyy_mm_dd = yyyy + '-' + mm + '-' + dd;
			$.post( kp + "koyomi-edit.cgi", { yyyy_mm_dd:yyyy_mm_dd }, function( data ){
				$( "#L2" ).html( data );

				dl2 = true;
				dl3 = false;
				displayBW();
				displayREC();
			});

		});
	} else{
		displayVIDEO( 'Food name! (>_<)' );
	}
};


var selectKoyomiPalette = function( yyyy, mm, dd, tdiv, modifyf ){
	displayVIDEO( modifyf );
	const palette = $( "#palette" ).val();
	$.post( kp + "koyomi-fix.cgi", { command:'palette', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, palette:palette, modifyf:modifyf }, function( data ){ $( "#L3" ).html( data );});
};


var selectKoyomiHis = function( yyyy, mm, dd, tdiv ){
	 fix_his_code = $( "#fix_his_code" ).val();
	if( fix_his_code != '' ){
		$.post( kp + "koyomi-fix.cgi", { command:"history", yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, fix_his_code:fix_his_code }, function( data ){
			$( "#L3" ).html( data );
		});
	}
};


var checkKyomiAsRef = function(){
	if( $( "#fix_ref" ).is( ":checked" )){
		$( "#kffood_weight" ).prop("disabled", false );
	}else{
		$( "#kffood_weight" ).prop("disabled", true );
	}
};


var checkKyomiXOR100g = function(){
	if( $( "#g100_check" ).is( ":checked" )){
		$( "#kffood_weight" ).prop("disabled", false );
	}else{
		$( "#kffood_weight" ).prop("disabled", true );
	}
};

var returnFix2Edit = function(){
	dl2 = true;
	dl3 = false;
	displayBW();
};

</script>
JS

	puts js
end