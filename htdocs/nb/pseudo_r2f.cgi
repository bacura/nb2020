#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser recipe to pseudo food 0.2.2.AI (2024/10/19)

#==============================================================================
# STATIC
#==============================================================================
@debug = false
myself = File.basename( __FILE__ )

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
		:save 		=> "保存",\
		:food_name	=> "食品名",\
		:food_group => "食品群"
	}

	return l[language]
end

def generate_code( db, status, food_group, code_prefix, user_condition )
	puts 'generate_code<br>' if @debug
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

puts 'POST data<br>' if @debug
command = @cgi['command']
recipe_code = @cgi['code']
food_name = @cgi['food_name']
food_group = @cgi['food_group']
class1 = @cgi['class1']
class2 = @cgi['class2']
class3 = @cgi['class3']
tag1 = @cgi['tag1']
tag2 = @cgi['tag2']
tag3 = @cgi['tag3']
tag4 = @cgi['tag4']
tag5 = @cgi['tag5']
if @debug
	puts "command: #{command}<br>\n"
	puts "recipe_code: #{recipe_code}<br>\n"
	puts "<hr>\n"
	puts "food_name: #{food_name}<br>\n"
	puts "food_group: #{food_group}<br>\n"
	puts "class1: #{class1}<br>\n"
	puts "class2: #{class2}<br>\n"
	puts "class3: #{class3}<br>\n"
	puts "tag1: #{tag1}<br>\n"
	puts "tag2: #{tag2}<br>\n"
	puts "tag3: #{tag3}<br>\n"
	puts "tag4: #{tag4}<br>\n"
	puts "tag5: #{tag5}<br>\n"
end


puts 'Extracting SUM<br>' if @debug
r = db.query(  "SELECT code, name, sum, dish from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false )
food_name = r.first['name'] if food_name == ''
recipe_code = r.first['code']
dish_num = r.first['dish'].to_i
food_no, food_weight = extract_sum( r.first['sum'], dish_num, 0 )[0..1]


if command == 'init'
	puts 'Generate form HTML<br>' if @debug
	food_group_option = ''
	19.times do |c| food_group_option << "<option value='#{@fg[c]}'>#{c}.#{@category[c]}</option>" end

	html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_name">#{l[:food_name]}</label>
				<input type="text" class="form-control form-control-sm" id="r2ffood_name" value="#{food_name}">
			</div>
		</div>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_group">#{l[:food_group]}</label>
				<select class="form-select form-select-sm" id="r2ffood_group">
					#{food_group_option}
				</select>
			</div>
		</div>
		<div class="col-3"></div>
		<div class="col-1">
			<button class="btn btn-outline-primary btn-sm" type="button" onclick="savePseudo_R2F( '#{recipe_code}' )">#{l[:save]}</button>
		</div>
	</div>

	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="r2fclass1" placeholder="class1" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="r2fclass2" placeholder="class2" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="r2fclass3" placeholder="class3" value=""></div>
	</div>
	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="r2ftag1" placeholder="tag1" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="r2ftag2" placeholder="tag2" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="r2ftag3" placeholder="tag3" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="r2ftag4" placeholder="tag4" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="r2ftag5" placeholder="tag5" value=""></div>
		<div class="col-1"></div>
	</div>
</div>

HTML
end


if command == 'save'
	puts 'FCT Calc<br>' if @debug
	fct.set_food( user.name, food_no, food_weight, false )
	fct.calc
	fct.gramt( 100 )
	fct.digit

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
		code = generate_code( db, status, food_group, 'P', '' )
	elsif user.status >= 8 && $NBURL != $MYURL
		status = 3
		code = generate_code( db, status, food_group, 'C', '' )
	else
		status = 1
		user_condition = "AND user='#{user.name}'"
		code = generate_code( db, status, food_group, 'U', user_condition )
	end

	puts 'Generate units<br>' if @debug
	unith = Hash.new
	unith['g'] = 1
	unith['kcal'] = fct.pickt( 'ENERC_KCAL' ).to_f / 100 if fct.pickt( 'ENERC_KCAL' ) != 0
	unith_ = unith.sort.to_h
	unit = JSON.generate( unith_ )

	fct_set = "REFUSE='0', #{fct.sql}, Notice='#{recipe_code}'"

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
end

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

// 食品化フォームの保存ボタンを押して保存してL3を消す。
var savePseudo_R2F = ( code ) => {
	const food_name = $( "#r2ffood_name" ).val();
	if( food_name != '' ){

		const food_group = $( "#r2ffood_group" ).val();
		const class1 = $( "#r2fclass1" ).val();
		const class2 = $( "#r2fclass2" ).val();
		const class3 = $( "#r2fclass3" ).val();
		const tag1 = $( "#r2ftag1" ).val();
		const tag2 = $( "#r2ftag2" ).val();
		const tag3 = $( "#r2ftag3" ).val();
		const tag4 = $( "#r2ftag4" ).val();
		const tag5 = $( "#r2ftag5" ).val();

		postReq( "save", { code, food_name, food_group, class1, class2, class3, tag1, tag2, tag3, tag4, tag5 }, (data) => {

//			$( "#L2" ).html( data );
			displayVIDEO( 'Foodized' );

			dl2 = false;
			displayBW();
		});
	}else{
		displayVIDEO( 'Food name! (>_<)' );
	}
};

</script>

JS
	puts js
end
