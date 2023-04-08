#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 japanese intake standard view 0.00b (2023/01/08)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require 'time'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'items' 	=> "個別栄養素表示",\
		'age'		=> "年齢等",\
		'month'		=> "ヶ月",\
		'm'			=> "（月）",\
		'year'		=> "歳",\
		'y'			=> "（歳）",\
		'sex'		=> "代謝的性別",\
		'male'		=> "男性",\
		'sex0'		=> "男性",\
		'female'	=> "女性",\
		'sex1'		=> "女性",\
		'femalem'	=> "女性（月経あり）",\
		'non'		=> "どれでもない",\
		'0'			=> "妊娠初期(0-15w)",\
		'16'		=> "妊娠中期(16-27w)",\
		'28'		=> "妊娠後期(28-w)",\
		'lactation'	=> "授乳期",\
		'mens'		=> "月経あり",\
		'view'		=> "個人摂取基準表示",\
		'ear'		=> "推定平均必要量<br>(EAR)",\
		'rda'		=> "推奨量<br>(RDA)",\
		'ai'		=> "目安量<br>(AI)",\
		'ul'		=> "耐容上限量<br>(UL)",\
		'dg'		=> "目標量<br>(DG)",\
		'unit'		=> "単位",\
		'nutrients'	=> "栄養素",\
		'fcz'		=> "保存値<br>(FCZ)",\
		'ne_na'		=> "（ニコチン酸）",\
		'fe_m'		=> "鉄",\
		'save'		=> "FCZ保存"
	}

	return l[language]
end

####
def menu( user, l )
	age = 18
	sex = 0

	r = mdb( "SELECT bio FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
	if r.first
		if r.first['bio'] != nil && r.first['bio'] != ''
			bio = JSON.parse( r.first['bio'] )
			sex = bio['sex'].to_i
			birth = Time.parse( bio['birth'] )
			age = ( Date.today.strftime( "%Y%m%d" ).to_i - birth.strftime( "%Y%m%d" ).to_i ) / 10000
		end
	end

	options = ''
	r = mdb( "SELECT DISTINCT name FROM #{$MYSQL_TB_REFITS};", false, @debug )
	r.each do |e|
		if e['name'] == 'FE_M'
			options << "<option value=''FE_M'>#{l['fe_m']}</option>"
		elsif e['name'] == 'NE_NA'
			options << "<option value='NE_NA'>#{l['ne_na']}</option>"
		else
			options << "<option value='#{e['name']}'>#{@fct_name[e['name']]}</option>"
		end
	end

	selected_am = ''
	selected_am = 'SELECTED' if age < 1

	checked_m = [ 'CHECKED', '' ]
	checked_f = [ '', 'CHECKED' ]

	html = <<-"MENU"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-6'>
			<div class='input-group input-group-sm'>
			  <select class="form-select" id="rits_item">
			  	#{options}
			  </select>
			  <button type="button" class="btn btn-sm btn-primary" onclick="viewRefIntake();">#{l['items']}</button>
			</div>
		</div>
	</div>
	<hr>

	<div class='row'>
		<div class='col-4'>
			<div class="input-group input-group-sm">
				<span class="input-group-text">#{l['age']}</span>
			  	<input type="number" min=0 class="form-control" id='ritp_age' value='#{age}'>
				<select class="form-select" id="ritp_age_mode">
					<option value='y'>#{l['year']}</option>
					<option value='m' #{selected_am}>#{l['month']}</option>
				</select>
			</div>
		</div>

		<div class='col-8'>
			<label class="form-check-label">#{l['sex']}</label>&nbsp;
			<div class="form-check form-check-inline">
			  <input class="form-check-input" type="radio" name="sex" id="sex_m" onclick="changeRISex( 0 )" #{checked_m[sex]}>
			  <label class="form-check-label">#{l['male']}</label>
			</div>
			<div class="form-check form-check-inline">
			  <input class="form-check-input" type="radio" name="sex" id="sex_f" onclick="changeRISex( 1 )" #{checked_f[sex]}>
			  <label class="form-check-label">#{l['female']}</label>
			</div>
			<div class="form-check form-check-inline">
			  <input class="form-check-input" type="checkbox" id="ff_m" DISABLED>
			  <label class="form-check-label">#{l['mens']}</label>
			</div>
		</div>
	</div>
	<div class='row'>
		<div class='col' align='right'>
			<div class="form-check form-check-inline">
			  <input class="form-check-input" type="radio" name="ff" id="ff_non" CHECKED DISABLED>
			  <label class="form-check-label">#{l['non']}</label>
			</div>
			<div class="form-check form-check-inline">
			  <input class="form-check-input" type="radio" name="ff" id="ff_p1" onclick="changeRIP()" DISABLED>
			  <label class="form-check-label">#{l['0']}</label>
			</div>
			<div class="form-check form-check-inline">
			  <input class="form-check-input" type="radio" name="ff" id="ff_p2" onclick="changeRIP()" DISABLED>
			  <label class="form-check-label">#{l['16']}</label>
			</div>
			<div class="form-check form-check-inline">
			  <input class="form-check-input" type="radio" name="ff" id="ff_p3" onclick="changeRIP()" DISABLED>
			  <label class="form-check-label">#{l['28']}</label>
			</div>
			<div class="form-check form-check-inline">
			  <input class="form-check-input" type="radio" name="ff" id="ff_l" DISABLED>
			  <label class="form-check-label">#{l['lactation']}</label>
			</div>
		</div>
	</div>
	<br>
	<div class='row'>
		<button class="btn btn-sm btn-primary" type="button" onclick="viewRefIntakeP()">#{l['view']}</button>
	</div>

</div>

MENU
	puts html
	exit()
end


###
def f_formula( base, rffi, item )
	v = BigDecimal( '0' )
	v = BigDecimal( base[item] ) if base[item] != ''
	if rffi != nil
		if rffi[item].include?( '+' )
			v += rffi[item].delete( '+' ).to_f
		elsif rffi[item] != ''
			v = BigDecimal( rffi[item] )
		end
	else
		v = 0
	end

	if %w( FAPUN3 VITD TOCPHA THIA RIBF VITB6A THIA2 NACL_EQ FE FE_M CU MN).include?( base['name'] )
		v = v.to_f.round( 1 )
	elsif item == 'UL'
		v = v.to_i
	else
		v = v.to_i
	end
	v = '' if v == 0

	return v
end



#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )

#### Guild member check
if user.status < 8
	puts "Guild member error."
	exit
end


command = @cgi['command']
rits_item = @cgi['rits_item']
ritp_age = @cgi['ritp_age'].to_i
ritp_age_mode = @cgi['ritp_age_mode']
sex = @cgi['sex'].to_i
ff_m = @cgi['ff_m'].to_i
ff_c = @cgi['ff_c'].to_i
fcz_name = @cgi['fcz_name']
if @debug
	puts "command:#{command}<br>\n"
	puts "rits_item:#{rits_item}<br>\n"
	puts "ritp_age:#{ritp_age}<br>\n"
	puts "ritp_age_mode:#{ritp_age_mode}<br>\n"
	puts "sex:#{sex}<br>\n"
	puts "ff_m:#{ff_m}<br>\n"
	puts "ff_c:#{ff_c}<br>\n"

	puts "<hr>\n"
end

case command
when 'view_item'
	puts '[DG]<br>' if @debug
	if rits_item == 'PROTV' || rits_item == 'FATV' || rits_item == 'CHOV' || rits_item == 'FASAT' || rits_item == 'FIB' || rits_item == 'NACL_EQ' || rits_item == 'NA' || rits_item == 'K'
		ref_m = ''
		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='0';", false, @debug )
		unit = r.first['unit']
		dg_unit = ''
		dg_unit = r.first['DG_unit'] if  rits_item == 'PROTV' || rits_item == 'FATV' || rits_item == 'CHOV'
		r.each do |e|
			kara = ''
			kara = '-' if e['DG_min'] != ''
			ref_m << "<tr><td>#{e['periods']}~#{e['periode']}#{l[e['period_class']]}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td><td>#{e['DG_min']}#{kara}#{e['DG_max']}&nbsp;#{dg_unit}</td></tr>"
		end

		ref_f = ''
		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='1' AND ( period_class='m' OR period_class='y' );", false, @debug )
		r.each do |e|
			kara = ''
			kara = '-' if e['DG_min'] != ''
			ref_f << "<tr><td>#{e['periods']}~#{e['periode']}#{l[e['period_class']]}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td><td>#{e['DG_min']}#{kara}#{e['DG_max']}&nbsp;#{dg_unit}</td></tr>"
		end

		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='1' AND period_class='p';", false, @debug )
		r.each do |e| ref_f << "<tr><td>#{l[e['periods']]}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td><td>#{e['DG_min']}-#{e['DG_max']}&nbsp;#{dg_unit}</td></tr>" end

		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='1' AND period_class='l';", false, @debug )
		r.each do |e| ref_f << "<tr><td>#{l['lactation']}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td><td>#{e['DG_min']}-#{e['DG_max']}&nbsp;#{dg_unit}</td></tr>" end

		html = <<-"HTML"
<div class='container-fluid'>
	<h5>#{@fct_name[rits_item]} (#{unit})</h5>
	<div class='row'>
		<div class='col-6'>
			<h6>#{l['male']}</h6>
			<table class='table table-striped table-sm'>
				<thead class='fct_item align_c'>
					<td>#{l['age']}</td>
					<td>#{l['ear']}</td>
					<td>#{l['rda']}</td>
					<td>#{l['ai']}</td>
					<td>#{l['ul']}</td>
					<td>#{l['dg']}</td>
				</thead>
				<tbody class='align_r'>
					#{ref_m}
				</tbody>
			</table>
		</div>

		<div class='col-6'>
			<h6>#{l['female']}</h6>
			<table class='table table-striped table-sm'>
				<thead class='fct_item align_c'>
					<td>#{l['age']}</td>
					<td>#{l['ear']}</td>
					<td>#{l['rda']}</td>
					<td>#{l['ai']}</td>
					<td>#{l['ul']}</td>
					<td>#{l['dg']}</td>
				</thead>
				<tbody class='align_r'>
					#{ref_f}
				</tbody>
			</table>
		</div>
	</div>
</div>
HTML

	elsif rits_item == 'FE'
	puts '[FE]<br>' if @debug
		ref_m = ''
		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='0';", false, @debug )
		unit = r.first['unit']
		r.each do |e| ref_m << "<tr><td>#{e['periods']}~#{e['periode']}#{l[e['period_class']]}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td></tr>" end


		ref_f = ''
		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='1' AND ( period_class='m' OR period_class='y' );", false, @debug )
		r.each do |e| ref_f << "<tr><td>#{e['periods']}~#{e['periode']}#{l[e['period_class']]}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td></tr>" end

		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='1' AND period_class='p';", false, @debug )
		r.each do |e| ref_f << "<tr><td>#{l[e['periods']]}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td></tr>" end

		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='1' AND period_class='l';", false, @debug )
		r.each do |e| ref_f << "<tr><td>#{l['lactation']}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td></tr>" end


		ref_fm = ''
		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='FE_M' AND ( period_class='m' OR period_class='y' );", false, @debug )
		r.each do |e| ref_fm << "<tr><td>#{e['periods']}~#{e['periode']}#{l[e['period_class']]}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td></tr>" end

		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='FE_M' AND period_class='p';", false, @debug )
		r.each do |e| ref_fm << "<tr><td>#{l[e['periods']]}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td></tr>" end

		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='FE_M' AND period_class='l';", false, @debug )
		r.each do |e| ref_fm << "<tr><td>#{l['lactation']}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td></tr>" end

		html = <<-"HTML"
<div class='container-fluid'>
	<h5>#{@fct_name[rits_item]} (#{unit})</h5>
	<div class='row'>
		<div class='col-4'>
			<h6>#{l['male']}</h6>
			<table class='table table-striped table-sm'>
				<thead class='fct_item align_c'>
					<td>#{l['age']}</td>
					<td>#{l['ear']}</td>
					<td>#{l['rda']}</td>
					<td>#{l['ai']}</td>
					<td>#{l['ul']}</td>
				</thead>
				<tbody class='align_r'>
					#{ref_m}
				</tbody>
			</table>
		</div>

		<div class='col-4'>
			<h6>#{l['female']}</h6>
			<table class='table table-striped table-sm'>
				<thead class='fct_item align_c'>
					<td>#{l['age']}</td>
					<td>#{l['ear']}</td>
					<td>#{l['rda']}</td>
					<td>#{l['ai']}</td>
					<td>#{l['ul']}</td>
				</thead>
				<tbody class='align_r'>
					#{ref_f}
				</tbody>
			</table>
		</div>

		<div class='col-4'>
			<h6>#{l['femalem']}</h6>
			<table class='table table-striped table-sm'>
				<thead class='fct_item align_c'>
					<td>#{l['age']}</td>
					<td>#{l['ear']}</td>
					<td>#{l['rda']}</td>
					<td>#{l['ai']}</td>
					<td>#{l['ul']}</td>
				</thead>
				<tbody class='align_r'>
					#{ref_fm}
				</tbody>
			</table>
		</div>
	</div>
</div>
HTML

	else
	puts 'View items<br>' if @debug
		ref_m = ''
		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='0';", false, @debug )
		unit = r.first['unit']
		r.each do |e| ref_m << "<tr><td>#{e['periods']}~#{e['periode']}#{l[e['period_class']]}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td></tr>" end

		ref_f = ''
		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='1' AND ( period_class='m' OR period_class='y' );", false, @debug )
		r.each do |e| ref_f << "<tr><td>#{e['periods']}~#{e['periode']}#{l[e['period_class']]}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td></tr>" end

		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='1' AND period_class='p';", false, @debug )
		r.each do |e| ref_f << "<tr><td>#{l[e['periods']]}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td></tr>" end

		r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE name='#{rits_item}' AND sex='1' AND period_class='l';", false, @debug )
		r.each do |e| ref_f << "<tr><td>#{l['lactation']}</td><td>#{e['EAR']}</td><td>#{e['RDA']}</td><td>#{e['AI']}</td><td>#{e['UL']}</td></tr>" end

		html = <<-"HTML"
<div class='container-fluid'>
	<h5>#{@fct_name[rits_item]} (#{unit})</h5>
	<div class='row'>
		<div class='col-6'>
			<h6>#{l['male']}</h6>
			<table class='table table-striped table-sm'>
				<thead class='fct_item align_c'>
					<td>#{l['age']}</td>
					<td>#{l['ear']}</td>
					<td>#{l['rda']}</td>
					<td>#{l['ai']}</td>
					<td>#{l['ul']}</td>
				</thead>
				<tbody class='align_r'>
					#{ref_m}
				</tbody>
			</table>
		</div>

		<div class='col-6'>
			<h6>#{l['female']}</h6>
			<table class='table table-striped table-sm'>
				<thead class='fct_item align_c'>
					<td>#{l['age']}</td>
					<td>#{l['ear']}</td>
					<td>#{l['rda']}</td>
					<td>#{l['ai']}</td>
					<td>#{l['ul']}</td>
				</thead>
				<tbody class='align_r'>
					#{ref_f}
				</tbody>
			</table>
		</div>
	</div>
</div>
HTML
	end

when 'personal', 'save'
	ref_p = ''
	set_sql = 'SET '

	if sex == 1
		rff = []
		case ff_c
		when 0
			rs= []
		when 1
			rs = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE sex='1' AND period_class='p' AND periods='0';", false, @debug )
		when 2
			rs = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE sex='1' AND period_class='p' AND periods='16';", false, @debug )
		when 3
			rs = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE sex='1' AND period_class='p' AND periods='28';", false, @debug )
		when 4
			rs = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE sex='1' AND period_class='l';", false, @debug )
		end
		rff = []
		rs.each do |e| rff << e end
	end

	r = mdb( "SELECT * FROM #{$MYSQL_TB_REFITS} WHERE sex='#{sex}' AND period_class='#{ritp_age_mode}' AND periods<=#{ritp_age} AND periode>=#{ritp_age};", false, @debug )
	r.each_with_index do |e, i|
		if sex == 0
			@ear = e['EAR']
			@rda = e['RDA']
			@ai = e['AI']
			@ul = e['UL']
			@dg_min = e['DG_min']
			@dg_max = e['DG_max']
			display_flag = true
		else
			unless ( e['name'] == 'FE' && ff_m == 1 ) || ( e['name'] == 'FE_M' && ff_m == 0 )
				@ear = f_formula( e, rff[i], 'EAR' )
				@rda = f_formula( e, rff[i], 'RDA' )
				@ai = f_formula( e, rff[i], 'AI' )
				@ul = f_formula( e, rff[i], 'UL' )
				@dg_min = f_formula( e, rff[i], 'DG_min' )
				@dg_max = f_formula( e, rff[i], 'DG_max' )
				display_flag = true
			else
				display_flag = false
			end
		end

		if display_flag
			nutrients = @fct_name[e['name']]
			sql_name = e['name']
			nutrients = l['ne_na'] if e['name'] == 'NE_NA'
			if e['name'] == 'FE_M'
				nutrients = l['fe_m']
				sql_name = 'FE'
			end
			dg_unit = ''
			dg_unit = r.first['DG_unit'] if  e['name'] == 'PROTV' || e['name'] == 'FATV' || e['name'] == 'CHOV'
			kara = ''
			kara = '-' if @dg_min != 0 && @dg_min != ''

			fcz = @ai
			fcz = @rda if @rda != ''
			fcz = @dg_min if e['name'] == 'FIB'
			fcz = @dg_min if e['name'] == 'K'
			fcz = @dg_max if e['name'] == 'NACL_EQ'
			fcz = @dg_max if e['name'] == 'FASAT'

			ref_p << "<tr><td>#{nutrients}</td><td>#{e['unit']}</td><td>#{@ear}</td><td>#{@rda}</td><td>#{@ai}</td><td>#{@ul}</td><td>#{@dg_min}#{kara}#{@dg_max}&nbsp;#{dg_unit}</td><td>#{fcz}</td></tr>"

			set_sql << "#{sql_name}='#{fcz}'," if e['name'] != 'NE_NA'
		end
	end


	if command == 'save'
		puts '[SAVE]<br>' if @debug
		r = mdb( "SELECT code FROM #{$MYSQL_TB_FCZ} WHERE base='ref_intake' AND user='#{user.name}' AND name='#{fcz_name}';", false, @debug )
		if r.first
			mdb( "UPDATE #{$MYSQL_TB_FCZ} #{set_sql} date='#{@date}' WHERE base='ref_intake' AND user='#{user.name}' AND name='#{fcz_name}';", false, @debug )
		else
			new_code = generate_code( user.name, 'z' )
			mdb( "INSERT INTO #{$MYSQL_TB_FCZ} #{set_sql} code='#{new_code}', origin='#{@datetime}', base='ref_intake', user='#{user.name}', name='#{fcz_name}', date='#{@date}';", false, @debug )
		end
		exit( 0 )
	end

	fct_html = ''
	if user.status >= 2
		fct_html << '<div class="input-group input-group-sm">'
		fct_html << "<input type='text' class='form-control' id='fcz_name' value='#{l["sex#{sex}"]}#{ritp_age}#{l[ritp_age_mode]}#{ff_m}#{ff_c}''>"
		fct_html << "<button class='btn btn-outline-primary' type='button' onclick='saveRefIntake()''>#{l['save']}</button>"
		fct_html << '</div>'
	end

	puts "HTML<br>" if @debug
	html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-8'>
			<h5>#{l["sex#{sex}"]}&nbsp;#{ritp_age}#{l[ritp_age_mode]}</h5>
		</div>
		<div class='col-4'>
			#{fct_html}
		</div>
	</div>
	<br>
	<div class='row'>
		<div class='col'>
			<table class='table table-striped table-sm'>
				<thead class='fct_item align_c'>
					<td>#{l['nutrients']}</td>
					<td>#{l['unit']}</td>
					<td>#{l['ear']}</td>
					<td>#{l['rda']}</td>
					<td>#{l['ai']}</td>
					<td>#{l['ul']}</td>
					<td>#{l['dg']}</td>
					<td>#{l['fcz']}</td>
				</thead>
				<tbody class='align_r'>
					#{ref_p}
				</tbody>
			</table>
		</div>
	</div>
</div>
HTML

else
	menu( user, l )
end

puts html


####
if command == 'init'
	js = <<-"JS"
<script type='text/javascript'>

// Ref instake init
var changeRISex = function( sex ){
	if( sex == 0 ){
		document.getElementById( 'ff_non' ).checked = true;
		document.getElementById( 'ff_m' ).checked = false;
		document.getElementById( 'ff_m' ).disabled = true;
		document.getElementById( 'ff_non' ).disabled = true;
		document.getElementById( 'ff_p1' ).disabled = true;
		document.getElementById( 'ff_p2' ).disabled = true;
		document.getElementById( 'ff_p3' ).disabled = true;
		document.getElementById( 'ff_l' ).disabled = true;
	}else{
		document.getElementById( 'ff_m' ).disabled = false;
		document.getElementById( 'ff_non' ).disabled = false;
		document.getElementById( 'ff_p1' ).disabled = false;
		document.getElementById( 'ff_p2' ).disabled = false;
		document.getElementById( 'ff_p3' ).disabled = false;
		document.getElementById( 'ff_l' ).disabled = false;
	}
};

var changeRIP = function(){
		document.getElementById( 'ff_m' ).checked = false;
};
</script>
JS
	puts js
end