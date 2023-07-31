#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 recipe editor 0.15b (2023/04/15)

#==============================================================================
#COMMON LIBRARY
#==============================================================================
require './soul'
require './brain'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )
#$UDIC = '/usr/local/share/mecab/dic/ipadic/sys.dic'


#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'type'	 	=> "料理スタイル",\
		'role' 		=> "献立区分",\
		'tech'	 	=> "調理区分",\
		'time' 		=> "目安時間(分)",\
		'cost'	 	=> "目安費用(円)",\
		'name' 		=> "レシピ名",\
		'save' 		=> "保存",\
		'protocol' 	=> "調理手順",\
		'special' 	=> "【行頭特殊記号】　<b>!</b>[文字]:強調、<b>@</b>[文字]:ただし書き（薄カッコ表示）、<b>#</b>[文字]:コメント（非表示）、<b>&</b>[レシピコード]:参照レシピ",\
		'root' 		=> "母",\
		'branch' 	=> "娘",\
		'favorite' 	=> "<img src='bootstrap-dist/icons/star-fill-y.svg' style='height:1.0em; width:1.0em;'>お気に入り",\
		'draft' 	=> "<img src='bootstrap-dist/icons/cone-striped.svg' style='height:1.0em; width:1.0em;'>仮組",\
		'public' 	=> "<img src='bootstrap-dist/icons/globe.svg' style='height:1.0em; width:1.0em;'>公開",\
		'protect' 	=> "<img src='bootstrap-dist/icons/lock-fill.svg' style='height:1.0em; width:1.0em;'>保護",\
		'camera'	=> "<img src='bootstrap-dist/icons/camera.svg' style='height:1.2em; width:1.2em;'>",\
		'link'		=> "<img src='bootstrap-dist/icons/paperclip.svg' style='height:2.4em; width:2.4em;'>",\
		'division'	=> "<img src='bootstrap-dist/icons/virus-p.svg' style='height:1.2em; width:1.2em;'>",\
		'mdm'		=> "<img src='bootstrap-dist/icons/diagram-3.svg' style='height:2.4em; width:2.4em;'>",\
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


#### POST
command = @cgi['command']
code = @cgi['code']
root = @cgi['root']
if @debug
	puts "commnad:#{command}<br>"
	puts "code:#{code}<br>"
	puts "root:#{code}<br>"
end

recipe = Recipe.new( user )
recipe.debug if @debug

case command
when 'view'
	# Loading recipe from DB
	recipe.load_db( code, true ) if code != ''

when 'protocol'
	recipe.load_db( code, true ) if code != ''
	recipe.protocol = @cgi['protocol']
	recipe.date = @datetime
	recipe.update_db
	exit

when 'save', 'division'
	require 'fileutils'
	recipe.load_cgi( @cgi )

	# Avoiding loop
	 recipe.root = '' if recipe.root == recipe.code

	# excepting for tags
	recipe.protocol = wash( recipe.protocol )

	r = mdb( "SELECT sum, name, dish from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	if r.first['name'] == ''
		puts 'Inserting new recipe<br>' if @debug
		recipe.code = generate_code( user.name, 'r' )
		recipe.sum = r.first['sum']
		recipe.dish = r.first['dish'].to_i
  		recipe.insert_db

	else
		puts 'Updating recipe<br>' if @debug
		pre_recipe = Recipe.new( user )
		pre_recipe.code = recipe.code
		pre_recipe.load_db( code, true )
		recipe.sum = r.first['sum']
		recipe.dish = r.first['dish'].to_i

		copy_flag = false
		original_user = nil

		if user.name != pre_recipe.user.name
			puts 'Import mode<br>' if @debug
			copy_flag = true
			original_user = pre_recipe.user.name
			recipe.favorite = 0
			recipe.draft = 1
			recipe.user = user
			recipe.sum = r.first['sum']
			recipe.dish = r.first['dish'].to_i
		end

		puts 'Canceling public mode of recipe using puseudo user foods<br>' if @debug
		a = recipe.sum.split( "\t" )
		a.each do |e|
			sum_items = e.split( ':' )
			recipe.public = 0 if /^U/ =~ sum_items[0]
		end

		if recipe.draft == 1
			puts 'Draft mode<br>' if @debug
			recipe.protect = 0
			recipe.public = 0

			recipe.update_db

			copy_flag = true if command == 'division'

		elsif recipe.draft == 0 && recipe.protect == 0
			puts 'Normal mode<br>' if @debug
			if recipe.name == pre_recipe.name
				recipe.update_db
			else
				recipe.protect = 1 if recipe.public == 1
				copy_flag = true
			end

		else
			puts 'Protect mode<br>' if @debug
			recipe.protect = 1 if recipe.public == 1
			if pre_recipe.protect == 0 && recipe.name == pre_recipe.name
				recipe.update_db
			else
				copy_flag = true
			end
		end

		if copy_flag
			puts "Copying recipe<br>" if @debug
			recipe.code = generate_code( user.name, 'r' )

			# Copying name
			if recipe.name == pre_recipe.name && user.name == pre_recipe.user.name && command != 'division'
				t = pre_recipe.name.match( /\((\d+)\)$/ )
				sn = 1
				sn = t[1].to_i + 1 if t != nil
				pre_recipe.name.sub!( /\((\d+)\)$/, '' )
				recipe.name = "#{pre_recipe.name}(#{sn})"
			end

			puts "checking media<br>" if @debug
			rr = ''
			if original_user == nil
				rr = mdb( "SELECT mcode FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' and code='#{code}';", false, @debug )
			else
				rr = mdb( "SELECT mcode FROM #{$MYSQL_TB_MEDIA} WHERE user='#{original_user}' and code='#{code}';", false, @debug )
			end

			if rr.first
				puts "Copying photo<br>" if @debug
				rr.each do |e|
					new_media_code = generate_code( user.name, 'p' )

					FileUtils.cp( "#{$PHOTO_PATH}/#{e['mcode']}-tns.jpg", "#{$PHOTO_PATH}/#{new_media_code}-tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{e['mcode']}-tns.jpg" )
					FileUtils.cp( "#{$PHOTO_PATH}/#{e['mcode']}-tn.jpg", "#{$PHOTO_PATH}/#{new_media_code}-tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{e['mcode']}-tn.jpg" )
					FileUtils.cp( "#{$PHOTO_PATH}/#{e['mcode']}.jpg", "#{$PHOTO_PATH}/#{new_media_code}.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{e['mcode']}.jpg" )

					puts "Inserting into DB<br>" if @debug
					mdb( "INSERT INTO #{$MYSQL_TB_MEDIA} SET user='#{user.name}', code='#{recipe.code}', mcode='#{new_media_code}', origin='#{e['origin']}', date='#{@datetime}';", false, @debug )
				end
			end

			recipe.insert_db
		end
	end

	mdb( "UPDATE #{$MYSQL_TB_SUM} SET name='#{recipe.name}', code='#{recipe.code}', protect='#{recipe.protect}' WHERE user='#{user.name}';", false, @debug )
end


puts "HTML SELECT Recipe attribute<br>" if @debug
check_favorite = checked( recipe.favorite )
check_public = checked( recipe.public )
check_protect = checked( recipe.protect )
check_draft =  checked( recipe.draft )
file_disabled = false
if user.name != recipe.user
	check_favorite = 'DISABLED'
	check_public = 'DISABLED'
	check_protect = 'DISABLED'
	check_draft = 'CHECKED DISABLED'
	file_disabled = true
end


puts "HTML SELECT Recipe type<br>" if @debug
html_type = l['type']
html_type << '<select class="form-select form-select-sm" id="type">'
s = selected( 0, @recipe_type.size - 1, recipe.type )
@recipe_type.size.times do |i| html_type << "<option value='#{i}' #{s[i]}>#{@recipe_type[i]}</option>" end
html_type << '</select>'


puts "HTML SELECT Recipe role<br>" if @debug
html_role = l['role']
html_role << '<select class="form-select form-select-sm" id="role">'
s = selected( 0, @recipe_role.size - 1, recipe.role )
@recipe_role.size.times do |i| html_role << "<option value='#{i}' #{s[i]}>#{@recipe_role[i]}</option>" end
if recipe.role == 100
	html_role << "<option value='100' SELECTED>[ 調味％ ]</option>"
else
	html_role << "<option value='100'>[ 調味％ ]</option>"
end
html_role << '</select>'


puts "HTML SELECT Cooking technique<br>" if @debug
html_tech = l['tech']
html_tech << '<select class="form-select form-select-sm" id="tech">'
s = selected( 0, @recipe_tech.size - 1, recipe.tech )
@recipe_tech.size.times do |i| html_tech << "<option value='#{i}' #{s[i]}>#{@recipe_tech[i]}</option>" end
html_tech << '</select>'


puts "HTML SELECT Cooking time<br>" if @debug
html_time = l['time']
html_time << '<select class="form-select form-select-sm" id="time">'
s = selected( 0, @recipe_time.size - 1, recipe.time )
@recipe_time.size.times do |i| html_time << "<option value='#{i}' #{s[i]}>#{@recipe_time[i]}</option>" end
html_time << '</select>'


puts "HTML SELECT Cooking cost<br>" if @debug
html_cost = l['cost']
html_cost << '<select class="form-select form-select-sm" id="cost">'
s = selected( 0, @recipe_cost.size - 1, recipe.cost )
@recipe_cost.size.times do |i| html_cost << "<option value='#{i}' #{s[i]}>#{@recipe_cost[i]}</option>" end
html_cost << '</select>'


puts "HTML Photo upload form<br>" if @debug
form_photo = ''
form_photo = "<form method='post' enctype='multipart/form-data' id='photo_form'>"
form_photo << '<div class="input-group input-group-sm">'
form_photo << "<label class='input-group-text'>#{l['camera']}</label>"
if recipe.code == nil || file_disabled
	form_photo << "<input type='file' class='form-control' DISABLED>"
else
	form_photo << "<input type='file' class='form-control' name='photo' onchange=\"photoSave( '#{recipe.code}', '#photo_form', 'recipe' )\">"
end
form_photo << '</form></div>'

division = ''
division = "<span onclick=\"recipeSave( 'division', '#{recipe.code}' )\">#{l['division']}</span>" if recipe.draft == 1


puts "branche parts<br>" if @debug
branche = "<div class='col' id='tree' style='display:none;'>"
r = mdb( "SELECT name, code FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}' AND root='#{recipe.code}';", false, @debug )
if r.first && recipe.code != nil
    branche	<< '<ul class="list-group">'
	r.each do |e|
		branche << "<li class='list-group-item list-group-item-action' onclick='initCB( \"load\", \"#{e['code']}\", \"#{user.name}\" )'>#{e['name']}&nbsp;(#{e['code']})</li>"
	end
    branche	<< '</ul>'
    branche	<< "<input type='hidden' class='form-control' id='root' value='' >"
else
	branche	<< '<div class="input-group input-group-sm">'
	root_recipe_id = ''
	root_recipe_name = ''
	root_button = "<button class='btn btn-sm btn-secondary' onclick='words2Root()'>#{l['root']}</button>"

	if recipe.root != ""
		rr = mdb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}' AND root='#{recipe.root}';", false, @debug )
		if rr.first
			root_button = "<button class='btn btn-sm btn-info' onclick='initCB( \"load\", \"#{recipe.root}\", \"#{user.name}\" )'>#{l['root']}</button>"
			root_recipe_id = recipe.root
			root_recipe_name = rr.first['name']
		end
	end

	branche << root_button
    branche	<< "<input type='text' class='form-control' id='root' value='#{root_recipe_id}' >"
    branche	<< "<input type='text' class='form-control' id='root_name' value='#{root_recipe_name}' DISABLED>"
    branche	<< "&nbsp;&nbsp;#{division}"
    branche	<< '</div>'
end
branche << '</div>'


puts "HTML FORM recipe<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
  		<div class="col-5">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="recipe_name">#{l['name']}</label>
      			<input type="text" class="form-control" id="recipe_name" value="#{recipe.name}" required>
    		</div>
    	</div>
		<div class="col-1">
    	</div>
		<div class="col">
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="favorite" #{check_favorite}> #{l['favorite']}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="public" #{check_public} onchange="recipeBit_public()"> #{l['public']}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="protect" #{check_protect} onchange="recipeBit_protect()"> #{l['protect']}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="draft" #{check_draft} onchange="recipeBit_draft()"> #{l['draft']}
  				</label>
			</div>
		</div>
		<div class="col-1">
			<button class="btn btn-sm btn-outline-primary" type="button" onclick="recipeSave( 'save', '#{recipe.code}' )">#{l['save']}</button>
    	</div>
    </div>
    <br>
	<div class='row'>
		<div class='col'>#{html_type}</div>
		<div class='col'>#{html_role}</div>
		<div class='col'>#{html_tech}</div>
		<div class='col'>#{html_time}</div>
		<div class='col'>#{html_cost}</div>
	</div>
	<br>
	<div class='row'>
		<div class="col-2">#{l['protocol']}</div>
		<div class="col-10" align='right'>#{l['special']}</div>
	</div>
	<div class='row'>
		<textarea class="form-control" id="protocol" rows="10" onchange="recipeProtocol( '#{recipe.code}' )">#{recipe.protocol}</textarea>
	</div>
	<br>

	<div class='row'>
		<div class='col-4'>
			#{form_photo}
		</div>
		<div class='col-1'>
			<span onclick="words2Protocol()" >#{l['link']}</span>
		</div>
		<div class='col-1'>
			<span onclick="open_tree()" >#{l['mdm']}</span>
		</div>
		#{branche}
	</div>

	<div class='row'>
		<div align='right' class='col code'>#{recipe.code}</div>
	</div>

</div>
HTML

puts html

#==============================================================================
#POST PROCESS
#==============================================================================

if command == 'save'
	puts "Save fcz<br>" if @debug
	food_no, food_weight, total_weight = extract_sum( recipe.sum, recipe.dish, 0 )

	fct = FCT.new( @fct_item, @fct_name, @fct_unit, @fct_frct, 1, 1 )
	fct.load_palette( @palette_bit_all )
	fct.set_food( user.name, food_no, food_weight, false )
	fct.calc
	fct.digit

	fct.save_fcz( user.name, recipe.name, 'recipe', recipe.code )
end

if command == 'save'
	require 'natto'
	mecab = Natto::MeCab.new()

	puts "Makeing alias dictionary<br>" if @debug
	dic = Hash.new
	r = mdb( "SELECT org_name, alias FROM #{$MYSQL_TB_DIC};", false, @debug )
	r.each do |e| dic[e['alias']] = e['org_name'] end

	target = []

	puts "Marking recipe name<br>" if @debug
	r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPEI} WHERE code='#{recipe.code}' AND word='#{recipe.name}' AND user='#{user.name}';", false, @debug )
	mdb( "INSERT INTO #{$MYSQL_TB_RECIPEI}  SET public='#{recipe.public}', user='#{user.name}', code='#{recipe.code}', word='#{recipe.name}';", false, @debug ) unless r.first
	recipe.name.gsub!( '　', "\t" )
	recipe.name.gsub!( '・', "\t" )
	recipe.name.gsub!( '／', "\t" )
	recipe.name.gsub!( '(', "\t" )
	recipe.name.gsub!( ')', "\t" )
	recipe.name.gsub!( '（', "\t" )
	recipe.name.gsub!( '）', "\t" )
	recipe.name.gsub!( /\t+/, "\s" )
	target << recipe.name

	a = recipe.protocol.split( "\n" )

	puts "Marking tag line<br>" if @debug
	if a[0] != nil && /^\#.+/ =~ a[0]
		a[0].gsub!( '#', '' )
		if a[0] != ''
			a[0].gsub!( "　", "\s" )
			tags = a[0].split( "\s" )
			tags.each do |e|
				if e != ''
					target << e
					r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPEI} WHERE code='#{recipe.code}' AND word='#{e}' AND user='#{user.name}';", false, @debug )
					mdb( "INSERT INTO #{$MYSQL_TB_RECIPEI}  SET public='#{recipe.public}', user='#{user.name}', code='#{recipe.code}', word='#{e}';", false, @debug ) unless r.first
				end
			end
		end
	end

	puts "Marking comment line<br>" if @debug
	if a[1] != nil && /^\#.+/ =~ a[1]
		a[1].gsub!( '#', '' )
		target << a[1] if a[1] != ''
	end

	target.each do |e|
		true_word = e
		true_word = dic[e] if dic[e] != nil
		mecab.parse( true_word ) do |n|
			a = n.feature.force_encoding( 'utf-8' ).split( ',' )
		 	if a[0] == '名詞' && ( a[1] == '一般' || a[1] == '普通名詞' || a[1] == '固有名詞' || a[1] == '人名' )
				r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPEI} WHERE user='#{user.name}' AND code='#{recipe.code}' AND word='#{n.surface}';", false, @debug )
				mdb( "INSERT INTO #{$MYSQL_TB_RECIPEI}  SET public='#{recipe.public}', user='#{user.name}', code='#{recipe.code}', word='#{n.surface}';", false, @debug ) unless r.first
		 	end
		end
	end

	puts "Marking SUM<br>" if @debug
	a = recipe.sum.split( "\t" )
	sum_code = []
	target_food = []
	a.each do |e| sum_code << e.split( ':' ).first end
	sum_code.each do |e|
		r = mdb( "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{e}';", false, @debug )
		target_food << r.first['name'] if r.first
	end

	target_food.each do |e|
		r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPEI} WHERE user='#{user.name}' AND code='#{recipe.code}' AND word='#{e}';", false, @debug )
		mdb( "INSERT INTO #{$MYSQL_TB_RECIPEI}  SET public='#{recipe.public}', user='#{user.name}', code='#{recipe.code}', word='#{e}';", false, @debug ) unless r.first
	end
end


#==============================================================================
#FRONT SCRIPT
#==============================================================================

if command == 'view'
	js = <<-"JS"
<script type='text/javascript'>

// Public button
var recipeBit_public = function(){
	if( document.getElementById( "public" ).checked ){
		document.getElementById( "protect" ).checked = true;
		document.getElementById( "draft" ).checked = false;
	}
};

// Protect button
var recipeBit_protect = function(){
	if( document.getElementById( "protect" ).checked ){
		document.getElementById( "draft" ).checked = false;
	}else{
		document.getElementById( "public" ).checked = false;
	}
};

// Draft button
var recipeBit_draft = function(){
	if( document.getElementById( "draft" ).checked ){
		document.getElementById( "protect" ).checked = false;
		document.getElementById( "public" ).checked = false;
	}
};

// Tree button
var open_tree = function(){
	if( document.getElementById( "tree" ).style.display == 'none' ){
		document.getElementById( "tree" ).style.display = 'block';
	}else{
		document.getElementById( "tree" ).style.display = 'none';
	}
};

// words paste to protocol button
var words2Protocol = function(){
	var protocol = document.getElementById( 'protocol' );
	var words = document.getElementById( 'words' ).value;
	protocol.value = protocol.value.substr( 0, protocol.selectionStart ) + words + protocol.value.substr( protocol.selectionStart );
};

// words paste to mother button
var words2Root = function(){
	document.getElementById( 'root' ).value = document.getElementById( 'words' ).value;
};

</script>
JS
	puts js
end
