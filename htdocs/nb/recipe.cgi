#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 recipe editor 0.06b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require './brain'
require 'fileutils'


#==============================================================================
#STATIC
#==============================================================================
script = 'recipe'
@debug = false
#$UDIC = '/usr/local/share/mecab/dic/ipadic/sys.dic'


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


#### POST
command = @cgi['command']
code = @cgi['code']
if @debug
	puts "commnad:#{command}<br>"
	puts "code:#{code}<br>"
end

recipe = Recipe.new( user.name )
recipe.debug if @debug

case command
when 'view'
	# Loading recipe from DB
	recipe.load_db( code, true ) if code != ''

when 'save'
	recipe.load_cgi( @cgi )

	# excepting for tags
	recipe.protocol = wash( recipe.protocol )

	r = mdb( "SELECT sum, name, dish from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	# Inserting new recipe
	if r.first['name'] == ''
		recipe.code = generate_code( user.name, 'r' )
		recipe.sum = r.first['sum']
		recipe.dish = r.first['dish'].to_i
  		recipe.insert_db

	# Updating recipe
	else
		pre_recipe = Recipe.new( user.name )
		pre_recipe.code = recipe.code
		pre_recipe.load_db( code, true )
		recipe.sum = r.first['sum']
		recipe.dish = r.first['dish'].to_i

		# Import mode
		copy_flag = false
		original_user = nil

		if user.name != pre_recipe.user
			copy_flag = true
			original_user = pre_recipe.user
			recipe.draft = 1
			recipe.user = user.name
			recipe.sum = r.first['sum']
			recipe.dish = r.first['dish'].to_i
		end

		# Canceling public mode of recipe using puseudo user foods
		a = recipe.sum.split( "\t" )
		a.each do |e|
			sum_items = e.split( ':' )
			recipe.public = 0 if /^U/ =~ sum_items[0]
		end

		# Draft mode
		if recipe.draft == 1
			recipe.protect = 0
			recipe.public = 0
			recipe.update_db

		# Normal mode
		elsif recipe.draft == 0 && recipe.protect == 0
			if recipe.name == pre_recipe.name
				recipe.update_db
			else
				recipe.protect = 1 if recipe.public == 1
				copy_flag = true
			end

		# Protect mode
		else
			recipe.protect = 1 if recipe.public == 1
			if pre_recipe.protect == 0 && recipe.name == pre_recipe.name
				recipe.update_db
			else
				copy_flag = true
			end
		end

		if copy_flag == true
			puts "Copying recipe<br>" if @debug
			recipe.code = generate_code( user.name, 'r' )

			# Copying name
			if recipe.name == pre_recipe.name && user.name == pre_recipe.user
				t = pre_recipe.name.match( /\((\d+)\)$/ )
				sn = 1
				sn = t[1].to_i + 1 if t != nil
				pre_recipe.name.sub!( /\((\d+)\)$/, '' )
				recipe.name = "#{pre_recipe.name}(#{sn})"
			end

			puts "checking media<br>" if @debug
			new_media_code = generate_code( user.name, 'p' )

			rr = ''
			if original_user
				rr = mdb( "SELECT mcode, origin FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' and code='#{code}';", false, @debug )
			else
				rr = mdb( "SELECT mcode, origin FROM #{$MYSQL_TB_MEDIA} WHERE user='#{original_user}' and code='#{code}';", false, @debug )
			end
			if rr.first
				puts "Copying photo<br>" if @debug
				r.each do |e|
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
check_public = checked( recipe.public )
check_protect = checked( recipe.protect )
check_draft =  checked( recipe.draft )
if user.name != recipe.user
	check_public = 'DISABLED'
	check_protect = 'DISABLED'
	check_draft = 'CHECKED DISABLED'
end


puts "HTML SELECT Recipe type<br>" if @debug
html_type = lp[1]
html_type << '<select class="form-select form-select-sm" id="type">'
s = selected( 0, @recipe_type.size - 1, recipe.type )
@recipe_type.size.times do |i| html_type << "<option value='#{i}' #{s[i]}>#{@recipe_type[i]}</option>" end
html_type << '</select>'


puts "HTML SELECT Recipe role<br>" if @debug
html_role = lp[2]
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
html_tech = lp[3]
html_tech << '<select class="form-select form-select-sm" id="tech">'
s = selected( 0, @recipe_tech.size - 1, recipe.tech )
@recipe_tech.size.times do |i| html_tech << "<option value='#{i}' #{s[i]}>#{@recipe_tech[i]}</option>" end
html_tech << '</select>'


puts "HTML SELECT Cooking time<br>" if @debug
html_time = lp[4]
html_time << '<select class="form-select form-select-sm" id="time">'
s = selected( 0, @recipe_time.size - 1, recipe.time )
@recipe_time.size.times do |i| html_time << "<option value='#{i}' #{s[i]}>#{@recipe_time[i]}</option>" end
html_time << '</select>'


puts "HTML SELECT Cooking cost<br>" if @debug
html_cost = lp[5]
html_cost << '<select class="form-select form-select-sm" id="cost">'
s = selected( 0, @recipe_cost.size - 1, recipe.cost )
@recipe_cost.size.times do |i| html_cost << "<option value='#{i}' #{s[i]}>#{@recipe_cost[i]}</option>" end
html_cost << '</select>'


puts "HTML Photo upload form<br>" if @debug
form_photo = ''
form_photo = "<form method='post' enctype='multipart/form-data' id='photo_form'>"
form_photo << '<div class="input-group input-group-sm">'
form_photo << "<label class='input-group-text'>#{lp[13]}</label>"
if recipe.code == nil
	form_photo << "<input type='file' class='form-control' DISABLED>"
else
	form_photo << "<input type='file' class='form-control' name='photo' onchange=\"photoSave( '#{recipe.code}', '#photo_form', 'recipe' )\">"
end
form_photo << '</form></div>'


puts "HTML FORM recipe<br>" if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{lp[6]}</h5></div>
		<div class='col-1'>#{lp[6]}</div>
		<div class="col-3">
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="public" #{check_public} onchange="recipeBit_public()"> #{lp[7]}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="protect" #{check_protect} onchange="recipeBit_protect()"> #{lp[8]}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="draft" #{check_draft} onchange="recipeBit_draft()"> #{lp[9]}
  				</label>
			</div>
		</div>
		<div class="col-1">
    	</div>
  		<div class="col-5">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="recipe_name">#{lp[10]}</label>
      			<input type="text" class="form-control" id="recipe_name" value="#{recipe.name}" required>
      			<button class="btn btn-outline-primary" type="button" onclick="recipeSave( '#{recipe.code}' )">#{lp[11]}</button>
    		</div>
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
		<div class="col form-group">
			<div class="col">
    			<label for="exampleFormControlTextarea1">#{lp[12]}</label>
				<textarea class="form-control" id="protocol" rows="10">#{recipe.protocol}</textarea>
			</div>
  		</div>
	</div>
	<div class='row'>
		<div class='col-4'>
			#{form_photo}
		</div>
		<div align='right' class='col-8 code'>#{recipe.code}</div>
		</div>
	</div>

</div>
HTML

puts html

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
puts "(^q^)<br>" if @debug
