#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 pseudo food editer 0.2.2.AI (2024/10/19)

#==============================================================================
# STATIC
#==============================================================================
@debug = false
myself = File.basename( __FILE__ )

#status = {1=>'user',-1=>'user_del',2=>'public',-2=>'public_del',3=>'community',-3=>'community_del',9=>'original', }

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
		:save       => "保存",
		:delete     => "削除",
		:food_name  => "食品名",
		:food_group => "食品群",
		:notice 	=> "備考：",
		:weight     => "重量"
	}

	return l[language]
end

#
def add_fct_row( fct_collection, fct, disabled_option )
	fct_block = ''
	fct_collection.each do |e|
		picked_value = fct.pickt( e )
		t = picked_value.nil? || picked_value == '' ? 0.to_f : picked_value.to_f
		fct_block << "<tr><td>#{@fct_name[e]}</td><td align='right' width='20%'><input type='text' class='form-control form-control-sm' id='p#{e}' value=\"#{t}\" #{disabled_option}></td><td>#{@fct_unit[e]}</td></tr>"
	end

	return fct_block
end

#
def generate_code( db, code, status, food_group, code_prefix, user_condition )
	puts 'generate_code<br>' if @debug
	r = db.query( "SELECT FN FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND FN='#{code}' AND status='#{status}' #{user_condition};", false )
	unless r.first
		rr = db.query( "SELECT FN FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND status='-#{status}' AND FN LIKE '#{code_prefix}%';", false )
		if rr.first
			code = rr.first['FN']
		else
			code = "#{code_prefix}#{food_group}001"
			rrr = db.query( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND status='#{status}' AND FN LIKE '#{code_prefix}%' );", false)
			if rrr.first
				last_code = rrr.first['FN'][-3, 3].to_i
				code = "#{code_prefix}#{food_group}%#03d" % ( last_code + 1 )
			end
		end
	end

	return code
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
code = @cgi['code'] || ''
code = '' unless /P|U|C\d{5}/ =~ code
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

food_weight_zero = food_weight == '0' ? true : false
food_weight = food_weight == nil || food_weight == ''|| food_weight == '0' ? 100 : BigDecimal( food_weight )


# food_key処理
unless food_key.empty?
	fg_key, class1_key, class2_key, class3_key, food_name_key = food_key.split( ':' )
	food_group = fg_key
	class1 = class1_key
	class2 = class2_key
	class3 = class3_key
	food_name = food_name_key
end

if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "food_key: #{food_key}<br>"
	puts "food_name: #{food_name}<br>"
	puts "food_group: #{food_group}<br>"
	puts "food_weight: #{food_weight}<br>"
	puts "class1: #{class1}<br>"
	puts "class2: #{class2}<br>"
	puts "class3: #{class3}<br>"
	puts "tag1: #{tag1}<br>"
	puts "tag2: #{tag2}<br>"
	puts "tag3: #{tag3}<br>"
	puts "tag4: #{tag4}<br>"
	puts "tag5: #{tag5}<br>"
	puts "<hr>"
end


puts "Loading fctp<br>" if @debug
if command == 'init' && code != ''
	refuse, notice = fct.load_fctp( user.name, code )
	fct.calc
end


puts "Loading tag<br>" if @debug
tag_user = nil
status = 0
if command == 'init' && code != ''
	r = db.query( "select * from #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND ( user='#{user.name}' OR user='#{$GM}' );", false )
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
		status = r.first['status'].to_i
	end

elsif command == 'save' && code != ''
	r = db.query(  "select * from #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND user='#{user.name}';", false )
	tag_user = r.first['user'] if r.first

elsif command == 'delete' && code != ''
	r = db.query(  "select * from #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND user='#{user.name}';", false )
	status = r.first['status'].to_i
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

	class1_new = class1.empty? ? '' : "＜#{class1}＞"
	class2_new = class2.empty? ? '' : "＜#{class2}＞"
	class3_new = class2.empty? ? '' : "＜#{class2}＞"
	tag1_new = tag1.empty? ? '' : "　#{tag1}"
	tag2_new = tag2.empty? ? '' : "　#{tag2}"
	tag3_new = tag3.empty? ? '' : "　#{tag3}"
	tag4_new = tag4.empty? ? '' : "　#{tag4}"
	tag5_new = tag5.empty? ? '' : "　#{tag5}"
	tagnames_new = "#{class1_new}#{class2_new}#{class3_new}#{food_name}#{tag1_new}#{tag2_new}#{tag3_new}#{tag4_new}#{tag5_new}"

	puts 'Generate code<br>' if @debug
	if user.status >= 8 && $NBURL == $MYURL
		status = 2
		code = generate_code( db, code, status, food_group, 'P', '' )
	elsif user.status >= 8 && $NBURL != $MYURL
		status = 3
		code = generate_code( db, code, status, food_group, 'C', '' )
	else
		status = 1
		user_condition = "AND user='#{user.name}'"
		code = generate_code( db, code, status, food_group, 'U', user_condition )
	end

	puts 'Generate units<br>' if @debug
	unith = Hash.new
	unith['g'] = 1
	unith['kcal'] = ( fct.pickt( 'ENERC_KCAL' ) / 100 ).to_i if fct.pickt( 'ENERC_KCAL' ) != 0
	unith['g処理前'] = (( 100 - refuse ) / 100 ).to_i if refuse != 0
	unit = JSON.generate( unith.sort.to_h )

	fct_set = "REFUSE='#{refuse}', #{fct.sql}, Notice='#{notice}'"

	puts 'Checking Food number<br>' if @debug
	r = db.query(  "select FN from #{$MYSQL_TB_FCTP} WHERE user='#{user.name}' AND FN='#{code}';", false )
	if r.first
		db.query(  "UPDATE #{$MYSQL_TB_FCTP} SET FG='#{food_group}',Tagnames='#{tagnames_new}',#{fct_set} WHERE FN='#{code}' AND user='#{user.name}';", true )
	else
		db.query(  "INSERT INTO #{$MYSQL_TB_FCTP} SET FG='#{food_group}',FN='#{code}',user='#{user.name}',Tagnames='#{tagnames_new}',#{fct_set};", true )
	end

	r = db.query(  "select FN from #{$MYSQL_TB_TAG} WHERE user='#{user.name}' AND FN='#{code}';", false )
	if r.first
		db.query(  "UPDATE #{$MYSQL_TB_TAG} SET FG='#{food_group}',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',status='#{status}' WHERE FN='#{code}' AND user='#{user.name}';", true )
	else
		db.query(  "INSERT INTO #{$MYSQL_TB_TAG} SET FG='#{food_group}',FN='#{code}',SID='',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',user='#{user.name}',status='#{status}';", true )
	end

	r = db.query(  "select FN from #{$MYSQL_TB_EXT} WHERE user='#{user.name}' AND FN='#{code}';", false )
	if r.first
		db.query(  "UPDATE #{$MYSQL_TB_EXT} SET user='#{user.name}',color1='0', color2='0', color1h='0', color2h='0', unit='#{unit}' WHERE FN='#{code}' AND user='#{user.name}';", true )
	else
		db.query(  "INSERT INTO #{$MYSQL_TB_EXT} SET FN='#{code}', user='#{user.name}',color1='0', color2='0', color1h='0', color2h='0', unit='#{unit}';", true )
	end

	food_weight = 100
	tag_user = user.name
end


if command == 'delete'
	puts "DELETE<br>" if @debug
	status = -1 if status == 1
	status = -2 if status == 2
	status = -3 if status == 3
	db.query(  "UPDATE #{$MYSQL_TB_TAG} SET status='#{status}' WHERE user='#{user.name}' AND FN='#{code}';", true )
	code = ''
end


puts "FCT block html<br>" if @debug
food_group_option = ''
19.times do |c| food_group_option << "<option value='#{@fg[c]}' #{$SELECT[food_group.to_i == c]}>#{c}.#{@category[c]}</option>" end
disabled_option = tag_user != user.name && tag_user != nil && user.status != 9 ? 'disabled' : ''

fct_block = Array.new( 6, '' )
fct_block[0] = add_fct_row( @fct_rew, fct, disabled_option )
fct_block[1] = add_fct_row( @fct_pf, fct, disabled_option )
fct_block[2] = add_fct_row( @fct_cho, fct, disabled_option )
fct_block[3] = add_fct_row( @fct_m, fct, disabled_option )
fct_block[4] = add_fct_row( @fct_fsv, fct, disabled_option )
fct_block[5] = add_fct_row( @fct_wsv, fct, disabled_option )
fct_block[5] << "<tr><td><hr></td></tr>"
fct_block[5] << add_fct_row( @fct_as, fct, disabled_option )


puts "ports html<br>" if @debug
save_button = tag_user == user.name || code == '' ? "<button class=\"btn btn-outline-primary btn-sm\" type=\"button\" onclick=\"pseudoSave( '#{code}' )\">#{l[:save]}</button>" : ''
delete_button = code != '' && tag_user == user.name ? "<button class='btn btn-outline-danger btn-sm' type='button' onclick=\"pseudoDelete( '#{code}' )\">#{l[:delete]}</button>" : ''
fg_disabled = code != '' ? "DISABLED" : ''


puts "HTML<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			<input type="text" class="form-control form-control-sm" id="pfood_name" placeholder="#{l[:food_name]}" value="#{food_name}">
		</div>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_group">#{l[:food_group]}</label>
				<select class="form-select" id="pfood_group" #{fg_disabled}>
					#{food_group_option}
				</select>
			</div>
		</div>
		<div class="col-2">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_weight">#{l[:weight]}</label>
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
				#{l[:notice]}<br>
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


#==============================================================================
# FRONT SCRIPT START
#==============================================================================

if command == 'init'
	js = <<-"JS"
<script type='text/javascript'>

var postReq = ( command, data, successCallback ) => {
	$.post( '#{myself}', { command, ...data })
		.done( successCallback )
		.fail(( jqXHR, textStatus, errorThrown ) => {
			console.error( "Request failed: ", textStatus, errorThrown );
			alert( "An error occurred. Please try again." );
		});
};

//Get from DOM values
var getValue = ( id ) => document.getElementById( id ).value;

// Get all fields
var getFields = () => {
	const fields = [
		"food_name", "food_group", "food_weight", "class1", "class2", "class3",
		"tag1", "tag2", "tag3", "tag4", "tag5", "REFUSE", "ENERC", "ENERC_KCAL", "WATER",
		"PROTCAA", "PROT", "PROTV", "FATNLEA", "CHOLE", "FAT", "FATV", "CHOAVLM", "CHOAVL", 
		"CHOAVLDF", "CHOV", "FIB", "POLYL", "CHOCDF", "OA", "ASH", "NA", "K", "CA", "MG", 
		"P", "FE", "ZN", "CU", "MN", "ID", "SE", "CR", "MO", "RETOL", "CARTA", "CARTB", 
		"CRYPXB", "CARTBEQ", "VITA_RAE", "VITD", "TOCPHA", "TOCPHB", "TOCPHG", "TOCPHD", 
		"VITK", "THIA", "RIBF", "NIA", "NE", "VITB6A", "VITB12", "FOL", "PANTAC", "BIOT", 
		"VITC", "ALC", "NACL_EQ", "Notice", "FASAT", "FAMS", "FAPU", "FAPUN3", "FAPUN6", 
		"FIBTG", "FIBSOL", "FIBINS", "FIBTDF", "FIBSDFS", "FIBSDFP", "FIBIDF", "STARES"
	];

	let data = {};
	fields.forEach( field => { data[field] = getValue( "p" + field );});
	return data;
};

//Save pseudo food
var pseudoSave = function( code ) {
	const food_name = getValue( "pfood_name" );

	if ( food_name !== '' ) {
		let data = getFields();
		data.command = 'save';
		data.code = code;

		$.post( "#{myself}", data, function(response) {
			$( "#LF" ).html( response );
			displayVIDEO(food_name + ' saved');
		});
	} else {
		displayVIDEO('Food name! (>_<)');
	}
};

//Delete  pseudo food
var pseudoDelete = ( code ) => {
	postReq( "delete", { code }, data => {
		$( "#LF" ).html( data );

		dlf = false;
		displayBW();
		displayVIDEO( code + ' deleted' );
	});
};

</script>

JS
	puts js
end
