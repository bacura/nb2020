#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 pseudo food editer 0.22b (2024/04/30)

#==============================================================================
# STATIC
#==============================================================================
#script = File.basename( $0, '.cgi' )
@debug = false

#==============================================================================
# LIBRARY
#==============================================================================
require './soul'
require './brain'

#==============================================================================
# DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'save' 		=> "保存",\
		'delete'	=> "削除",\
		'food_name'	=> "食品名",\
		'food_group'=> "食品群",\
		'weight'	=> "重量"
	}

	return l[language]
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
db = Db.new( user, @debug, false )


fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
fct.load_palette( @palette_bit_all )


#### POSTデータの取得
command = @cgi['command']
food_key = @cgi['food_key']
code = @cgi['code']
food_name = @cgi['food_name']
food_group = @cgi['food_group']
food_weight = @cgi['food_weight']
class1 = @cgi['class1']
class2 = @cgi['class2']
class3 = @cgi['class3']
tag1 = @cgi['tag1']
tag2 = @cgi['tag2']
tag3 = @cgi['tag3']
tag4 = @cgi['tag4']
tag5 = @cgi['tag5']
refuse = @cgi['REFUSE'].to_i
notice = @cgi['Notice']


food_weight_zero = false
food_weight_zero = true if food_weight == '0'
food_weight = 100 if food_weight == nil || food_weight == ''|| food_weight == '0'
food_weight = BigDecimal( food_weight )

code = '' if code == nil
code = '' unless /P|U|C\d{5}/ =~ code

fg_key, class1_key, class2_key, class3_key, food_name_key = food_key.split( ':' ) if food_key unless nil
food_group = fg_key unless fg_key == nil
food_group_i = food_group.to_i
class1 = class1_key unless class1_key == nil
class2 = class2_key unless class2_key == nil
class3 = class3_key unless class3_key == nil
food_name = food_name_key unless food_name_key == nil
if @debug
	puts "command: #{command}<br>\n"
	puts "code: #{code}<br>\n"
	puts "food_key: #{food_key}<br>\n"
	puts "food_name: #{food_name}<br>\n"
	puts "food_group: #{food_group}<br>\n"
	puts "food_weight: #{food_weight}<br>\n"
	puts "class1: #{class1}<br>\n"
	puts "class2: #{class2}<br>\n"
	puts "class3: #{class3}<br>\n"
	puts "tag1: #{tag1}<br>\n"
	puts "tag2: #{tag2}<br>\n"
	puts "tag3: #{tag3}<br>\n"
	puts "tag4: #{tag4}<br>\n"
	puts "tag5: #{tag5}<br>\n"
	puts "<hr>\n"
end


puts "Loading fctp<br>" if @debug
if command == 'init' && code != ''
	refuse, notice = fct.load_fctp( user.name, code )
	fct.calc
end


puts "Loading tag<br>" if @debug
tag_user = nil
public_bit = 0
if command == 'init' && code != ''
	r = db.query(  "select * from #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND ( user='#{user.name}' OR user='#{$GM}' );", false )
	if r.first
		tag_user = r.first['user']
		class1 = r.first['class1']
		class2 = r.first['class2']
		class3 = r.first['class3']
		tag1 = r.first['tag1']
		tag2 = r.first['tag2']
		tag3 = r.first['tag3']
		tag4 = r.first['tag4']
		tag5 = r.first['tag5']
		public_bit = r.first['public']
	end
elsif command == 'save' && code != ''
	r = db.query(  "select * from #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND user='#{user.name}';", false )
	tag_user = r.first['user'] if r.first
elsif command == 'delete' && code != ''
	r = db.query(  "select * from #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND user='#{user.name}';", false )
	public_bit = r.first['public']
end


if command == 'save'
	puts "SAVE:" if @debug
	fct.load_cgi( @cgi )

	if  @cgi['ENERC_KCAL'].to_f != 0 && @cgi['ENERC'].to_f == 0
		puts "Energy>" if @debug
		fct.put_solid( 'ENERC', 0, (( @cgi['ENERC_KCAL'].to_f * 4184 ) / 1000 ).to_i )
	end
	if  @cgi['NACL_EQ'].to_f != 0 && @cgi['NA'].to_f == 0
		puts "Na>" if @debug
		fct.put_solid( 'NA', 0, ( @cgi['NACL_EQ'].to_f / 2.54 ).round( 1 ))
	end

	fct.singlet
	fct.gramt( 100 )
	fct.digit

	# ゼロ重量戻し
	food_weight = 0 if food_weight_zero

	class1_new = ''
	class2_new = ''
	class3_new = ''
	tag1_new = ''
	tag2_new = ''
	tag3_new = ''
	tag4_new = ''
	tag5_new = ''
	class1_new = "＜#{class1}＞" unless class1 == ''
	class2_new = "（#{class2}）" unless class2 == ''
	class3_new = "［#{class3}］" unless class3 == ''
	tag1_new = "　#{tag1}" unless tag1 == ''
	tag2_new = "　#{tag2}" unless tag2 == ''
	tag3_new = "　#{tag3}" unless tag3 == ''
	tag4_new = "　#{tag4}" unless tag4 == ''
	tag5_new = "　#{tag5}" unless tag5 == ''
	tagnames_new = "#{class1_new}#{class2_new}#{class3_new}#{food_name}#{tag1_new}#{tag2_new}#{tag3_new}#{tag4_new}#{tag5_new}"

	puts 'Making fct_sql set<br>' if @debug
	fct_set = "REFUSE='#{refuse}',"
	fct_set << fct.sql
	fct_set << ",Notice='#{notice}'"

	puts 'Generating new Food number:' if @debug
	if user.status >= 8 && $NBURL == $MYURL
		puts 'Public>' if @debug
		public_bit = 1
		r = db.query(  "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND FN='#{code}' AND public=1;", false )
		unless r.first
			rr = db.query(  "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND public='3' AND FN LIKE 'P%';", false )
			if rr.first
				code = rr.first['FN']
				puts "Recycle:#{code}>" if @debug
			else
				code = "P#{food_group}001"
				rrr = db.query(  "select * from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND public=1 AND FN LIKE 'P%');", false )
				if rrr.first
					puts "Detect:#{rrr.first['FN']}>" if @debug
					last_code = rrr.first['FN'][-3,3].to_i
					code = "P#{food_group}%#03d" % ( last_code + 1 )
				end
				puts "New:#{code}>" if @debug
			end
		end
	elsif user.status >= 8 && $NBURL != $MYURL
		puts 'Community' if @debug
		public_bit = 1
		r = db.query(  "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND FN='#{code}' AND public=1;", false )
		unless r.first
			rr = db.query(  "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND public='3' AND FN LIKE 'C%';", false )
			if rr.first
				code = rr.first['FN']
				puts "Recycle:#{code}>" if @debug
			else
				code = "C#{food_group}001"
				rrr = db.query(  "select * from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND public=1 AND FN LIKE 'C%');", false )
				if rrr.first
					puts "Detect:#{rrr.first['FN']}>" if @debug
					last_code = rrr.first['FN'][-3,3].to_i
					code = "C#{food_group}%#03d" % ( last_code + 1 )
				end
				puts "New:#{code}>" if @debug
			end
		end
	else
		puts 'Private>' if @debug
		r = db.query(  "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND FN='#{code}' AND public=0 AND user='#{user.name}' ;", false )
		unless r.first
			rr = db.query(  "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND user='#{user.name}' AND public='2' AND FN LIKE 'U%';", false )
			if rr.first
				code = rr.first['FN']
				puts "Recycle:#{code}>" if @debug
			else
				code = "U#{food_group}001"
				rrr = db.query(  "select * from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND user='#{user.name}' AND public=0 AND FN LIKE 'U%');", false )
				if rrr.first
					puts "Detect:#{rrr.first['FN']}>" if @debug
					last_code = rrr.first['FN'][-3,3].to_i
					code = "U#{food_group}%#03d" % ( last_code + 1 )
				end
				puts "New:#{code}>" if @debug
			end
		end
	end

	puts 'Generating units<br>' if @debug
	unith = Hash.new
	unith['g'] = 1
	unith['kcal'] = ( fct.pickt( 'ENERC_KCAL' ) / 100 ).to_i if fct.pickt( 'ENERC_KCAL' ) != 0
	unith['g処理前'] = (( 100 - refuse ) / 100 ).to_i if refuse != 0
	unith_ = unith.sort.to_h
	unit = JSON.generate( unith_ )

	puts 'Checking Food number<br>' if @debug
	r = db.query(  "select FN from #{$MYSQL_TB_TAG} WHERE user='#{user.name}' AND FN='#{code}';", false )
	if r.first
		# 擬似食品テーブルの更新
		db.query(  "UPDATE #{$MYSQL_TB_FCTP} SET FG='#{food_group}',Tagnames='#{tagnames_new}',#{fct_set} WHERE FN='#{code}' AND user='#{user.name}';", true )
		db.query(  "UPDATE #{$MYSQL_TB_TAG} SET FG='#{food_group}',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',public='#{public_bit}' WHERE FN='#{code}' AND user='#{user.name}';", true )
		db.query(  "UPDATE #{$MYSQL_TB_EXT} SET user='#{user.name}',color1='0', color2='0', color1h='0', color2h='0', unit='#{unit}' WHERE FN='#{code}' AND user='#{user.name}';", true )
	else
		db.query(  "INSERT INTO #{$MYSQL_TB_FCTP} SET FG='#{food_group}',FN='#{code}',user='#{user.name}',Tagnames='#{tagnames_new}',#{fct_set};", true )
		db.query(  "INSERT INTO #{$MYSQL_TB_TAG} SET FG='#{food_group}',FN='#{code}',SID='',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',user='#{user.name}',public='#{public_bit}';", true )
		db.query(  "INSERT INTO #{$MYSQL_TB_EXT} SET FN='#{code}', user='#{user.name}',color1='0', color2='0', color1h='0', color2h='0', unit='#{unit}';", true )
	end

	food_weight = 100
	tag_user = user.name
end


if command == 'delete'
	puts "DELETE<br>" if @debug
	public_bit = 2 if public_bit == 0
	public_bit = 3 if public_bit == 1
	db.query(  "UPDATE #{$MYSQL_TB_TAG} SET public='#{public_bit}' WHERE user='#{user.name}' AND FN='#{code}';", true )
	code = ''
end


#### food group html
food_group_option = ''
19.times do |c|
	cc = c
	cc = "0#{c}" if c < 10
	if food_group_i == c
		food_group_option << "<option value='#{cc}' SELECTED>#{c}.#{@category[c]}</option>"
	else
		food_group_option << "<option value='#{cc}'>#{c}.#{@category[c]}</option>"
	end
end


#### disable option
disabled_option = ''
disabled_option = 'disabled' if tag_user != user.name && tag_user != nil && user.status != 9


#### html_fct_block
fct_block = ['', '', '', '', '', '', '']
@fct_rew.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[0] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='p#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
@fct_pf.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[1] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='p#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
@fct_cho.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[2] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='p#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
@fct_m.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[3] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='p#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
@fct_fsv.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[4] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='p#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
@fct_wsv.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil && fct.pickt( e ) != ''
	fct_block[5] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='p#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end
fct_block[5] << "<tr><td><hr></td></tr>"
@fct_as.each do |e|
	t = nil
	t = fct.pickt( e ).to_f if fct.pickt( e ) != nil || fct.pickt( e ) != ''
	fct_block[5] << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='p#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
end


#### save button
save_button = ''
save_button = "<button class=\"btn btn-outline-primary btn-sm\" type=\"button\" onclick=\"pseudoSave( '#{code}' )\">#{l['save']}</button>" if tag_user == user.name || code == ''


#### delete button
delete_button = ''
delete_button = "<button class='btn btn-outline-danger btn-sm' type='button' onclick=\"pseudoDelete( '#{code}' )\">#{l['delete']}</button>" if code != '' && tag_user == user.name


#### FG select disable option
fg_disabled = ''
fg_disabled = "DISABLED" if code != ''


#### html part
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			<input type="text" class="form-control form-control-sm" id="pfood_name" placeholder="#{l['food_name']}" value="#{food_name}">
		</div>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_group">#{l['food_group']}</label>
				<select class="form-select" id="pfood_group" #{fg_disabled}>
					#{food_group_option}
				</select>
			</div>
		</div>
		<div class="col-2">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_weight">#{l['weight']}</label>
				<input type="text" class="form-control form-control-sm" id="pfood_weight" placeholder="100" value="#{food_weight.to_f}">&nbsp;g
			</div>

		</div>

		<div class="col-1"></div>

		<div class="col-1">
			#{save_button}
		</div>
	</div>

	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="pclass1" placeholder="class1" value="#{class1}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="pclass2" placeholder="class2" value="#{class2}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="pclass3" placeholder="class3" value="#{class3}"></div>
	</div>
	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="ptag1" placeholder="tag1" value="#{tag1}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="ptag2" placeholder="tag2" value="#{tag2}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="ptag3" placeholder="tag3" value="#{tag3}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="ptag4" placeholder="tag4" value="#{tag4}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="ptag5" placeholder="tag5" value="#{tag5}"></div>
		<div class="col-1"></div>
		<div class="col-1">#{delete_button}</div>
	</div>
	<hr>
	<div class="row">
		<div class="col-4">
			<table class="table-sm table-striped" width="100%">#{fct_block[0]}</table>

			<div style='border: solid gray 1px; margin: 0.5em; padding: 0.5em;'>
				備考：<br>
				<textarea rows="6" cols="32" id="pNotice" #{disabled_option}>#{notice}</textarea>
			</div>
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
	<div class='code'>#{code}</div>
</div>


HTML

puts html
