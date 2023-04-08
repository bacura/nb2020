#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser recipe to pseudo food 0.21b (20023/01/14)

#==============================================================================
# STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

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
		'food_name'	=> "食品名",\
		'food_group'=> "食品群"
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


#### POSTデータの取得
command = @cgi['command']
code = @cgi['code']
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
	puts "code: #{code}<br>\n"
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


fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
fct.load_palette( @palette_bit_all )


puts 'Extracting SUM<br>' if @debug
r = mdb( "SELECT code, name, sum, dish from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
food_name = r.first['name'] if food_name == ''
code = r.first['code']
dish_num = r.first['dish'].to_i
food_no, food_weight = extract_sum( r.first['sum'], dish_num, 0 )[0..1]


if command == 'form'
	# 食品群オプション html
	food_group_option = ''
	19.times do |c|
		cc = c
		cc = "0#{c}" if c < 10
		food_group_option << "<option value='#{cc}'>#{c}.#{@category[c]}</option>"
	end

	html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_name">#{l['food_name']}</label>
				<input type="text" class="form-control form-control-sm" id="r2ffood_name" value="#{food_name}">
			</div>
		</div>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="food_group">#{l['food_group']}</label>
				<select class="form-select form-select-sm" id="r2ffood_group">
					#{food_group_option}
				</select>
			</div>
		</div>
		<div class="col-3"></div>
		<div class="col-1">
			<button class="btn btn-outline-primary btn-sm" type="button" onclick="savePseudo_R2F( '#{code}' )">#{l['save']}</button>
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
	fct_set = "REFUSE='0',"
	fct_set << fct.sql
	fct_set << ",Notice='#{code}'"

	puts 'Generating new Food number:' if @debug
	if user.status >= 8 && $NBURL == $MYURL
		puts 'Public' if @debug
		public_bit = 1
		r = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND FN='#{code}' AND public=1;", false, @debug )
		unless r.first
			rr = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND public='3' AND FN LIKE 'P%';", false, @debug )
			if rr.first
				code = rr.first['FN']
				puts "Recycle:#{code}>" if @debug
			else
				code = "P#{food_group}001"
				rrr = mdb( "select * from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND public=1 AND FN LIKE 'P%');", false, @debug )
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
		r = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND FN='#{code}' AND public=1;", false, @debug )
		unless r.first
			rr = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND public='3' AND FN LIKE 'C%';", false, @debug )
			if rr.first
				code = rr.first['FN']
				puts "Recycle:#{code}>" if @debug
			else
				code = "C#{food_group}001"
				rrr = mdb( "select * from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND public=1 AND FN LIKE 'C%');", false, @debug )
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
		r = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND FN='#{code}' AND public=0 AND user='#{user.name}';", false, @debug )
		unless r.first
			rr = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND user='#{user.name}' AND public='2';", false, @debug )
			if rr.first
				code = rr.first['FN']
				puts "Recycle:#{code}>" if @debug
			else
				code = "U#{food_group}001"
				rrr = mdb( "select * from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND user='#{user.name}' AND public=0 AND FN LIKE 'U%');", false, @debug )
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
	unith['kcal'] = fct.pickt( 'ENERC_KCAL' ).to_f / 100 if fct.pickt( 'ENERC_KCAL' ) != 0
	unith_ = unith.sort.to_h
	unit = JSON.generate( unith_ )

	puts 'Checking Food number<br>' if @debug
	r = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE user='#{user.name}' AND FN='#{code}';", false, @debug )
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_FCTP} SET FG='#{food_group}',Tagnames='#{tagnames_new}',#{fct_set} WHERE FN='#{code}' AND user='#{user.name}';", false, @debug )
		mdb( "UPDATE #{$MYSQL_TB_TAG} SET FG='#{food_group}',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',public='#{public_bit}' WHERE FN='#{code}' AND user='#{user.name}';", false, @debug )
		mdb( "UPDATE #{$MYSQL_TB_EXT} SET user='#{user.name}',color1='0', color2='0', color1h='0', color2h='0', unit='#{unit}' WHERE FN='#{code}' AND user='#{user.name}';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_FCTP} SET FG='#{food_group}',FN='#{code}',user='#{user.name}',Tagnames='#{tagnames_new}',#{fct_set};", false, @debug )
		mdb( "INSERT INTO #{$MYSQL_TB_TAG} SET FG='#{food_group}',FN='#{code}',SID='',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',user='#{user.name}',public='#{public_bit}';", false, @debug )
		mdb( "INSERT INTO #{$MYSQL_TB_EXT} SET FN='#{code}', user='#{user.name}',color1='0', color2='0', color1h='0', color2h='0', unit='#{unit}';", false, @debug )
	end
end

puts html

puts '\(^q^)/' if @debug
