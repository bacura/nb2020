#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 menu 0.01b


#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'menu'


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


#### Getting POST data
command = @cgi['command']
code = @cgi['code']
if @debug
	puts "commnad:#{command}<br>"
	puts "code:#{code}<br>"
	puts "<hr>"
end


menu = Menu.new( user.name )
menu.debug if @debug


case command
when 'view'
	puts 'Displaing menu<br>' if @debug
	menu.load_db( code, true ) unless code == ''

when 'save'
	puts 'Saving menu<br>' if @debug
	menu.load_cgi( @cgi )

	r = mdb( "SELECT * from #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';", false, @debug )
	# Inserting new menu
	if r.first['name'] == ''
		menu.code = generate_code( user.name, 'm' )
		menu.meal = r.first['meal']
  		menu.insert_db

	# Updating menu
	else
		pre_menu = Menu.new( user.name )
		pre_menu.code = menu.code
		pre_menu.load_db( code, true )
		menu.meal = r.first['meal']

		if menu.name != pre_menu.name
			# 名前が一致しなければ、新規コードとメニューを登録
			# バグに近い仕様：名前を変えて新規コードになるけど、写真はコピーされない
			menu.code = generate_code( user.name, 'm' )
			menu.insert_db
			mdb( "UPDATE #{$MYSQL_TB_MEAL} SET name='#{menu.name}', code='#{menu.code}', protect='#{recipe.protect}' WHERE user='#{user.name}';", false, @debug )
		end
	end
	# Updating menu
	menu.debug if @debug
	menu.update_db
end


puts 'Label HTML<br>' if @debug
r = mdb( "SELECT label from #{$MYSQL_TB_MENU} WHERE user='#{user.name}' AND name!='';", false, @debug )
label_list = []
r.each do |e| label_list << e['label'] end
label_list.uniq!

html_label = '<select class="form-select form-select-sm" id="label">'
html_label << "<option value='#{lp[2]}' id='normal_label0' style='display:inline'>#{lp[2]}</option>"

normal_label_c = 0
label_list.each do |e|
	selected = ''
	selected = 'SELECTED' if e == menu.label
	unless e == lp[2]
		normal_label_c += 1
		html_label << "<option value='#{e}' id='normal_label#{normal_label_c}' style='display:inline' #{selected}>#{e}</option>"
	end
end

school_flavor = ''
if user.status >= 5 && user.status != 6
	school_label_c = 0
	r = mdb( "SELECT label FROM #{$MYSQL_TB_SCHOOLM} WHERE user='#{user.name}';", false, @debug )
	r.each do |e|
		school_flavor = 'btn-outline-info'
		a = e['label'].split( "\t" )
		a.each do |ee|
			selected = ''
			selected = 'SELECTED' if ee == menu.label
			school_label_c += 1
			html_label << "<option value='#{ee}' id='school_label#{school_label_c}' style='display:none' #{selected}>#{ee}</option>"
		end
	end
end
html_label << '</select>'


puts 'Photo upload form<br>' if @debug
form_photo = ''
form_photo = "<form method='post' enctype='multipart/form-data' id='photo_form'>"
form_photo << '<div class="input-group input-group-sm">'
form_photo << "<label class='input-group-text'>#{lp[12]}</label>"
if menu.code == nil
	form_photo << "<input type='file' class='form-control' DISABLED>"
else
	form_photo << "<input type='file' class='form-control' name='photo' onchange=\"photoSave( '#{menu.code}', '#photo_form', 'menu' )\">"
end
form_photo << '</form></div>'


puts 'HTML<br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{lp[3]}</h5></div>
		<div class="col-4">
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="public" #{checked( menu.public )}> #{lp[4]}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="protect" #{checked( menu.protect )}> #{lp[5]}
  				</label>
			</div>
		</div>
    </div>
    <br>
	<div class='row'>
		<div class="col-3">
			<div class="input-group input-group-sm">
				<label class="input-group-text #{school_flavor}" id='label_group' onclick="switchLabelset( '#{normal_label_c}', '#{school_label_c}' )">#{lp[9]}</label>
				#{html_label}
			</div>
		</div>

		<div align='center' class="col-1">
			<span onclick="copyLabel()">#{lp[13]}</span>
		</div>

		<div class="col-3">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="menu_name">#{lp[10]}</label>
      			<input type="text" class="form-control" id="new_label" value="">
	   		</div>
    	</div>

		<div class="col-5">
			<div class="input-group input-group-sm">
				<label class="input-group-text">#{lp[6]}</label>
      			<input type="text" class="form-control" id="menu_name" value="#{menu.name}" required>
      			<button class="btn btn-outline-primary" type="button" onclick="menuSave( '#{menu.code}' )">#{lp[7]}</button>
    		</div>
    	</div>
	</div>
    <br>
	<div class='row'>
		<div class="col">
			<div class="form-group">
    			<label for='memo'>#{lp[11]}</label>
				<textarea class="form-control" id='memo' rows="3">#{menu.memo}</textarea>
   			</div>
		</div>
	</div>
	<div class='row'>
		<div class='col-4'>
			#{form_photo}
		</div>
		<div align='right' class='col-8 code'>#{menu.code}</div>
	</div>
</div>
HTML

puts html
