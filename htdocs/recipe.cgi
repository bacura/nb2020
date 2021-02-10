#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 recipe editor 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'recipe'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### Fig copy method
def copy_fig( slot, code, source_code )
	FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-#{slot}tns.jpg", "#{$PHOTO_PATH}/#{code}-#{slot}tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-#{slot}tns.jpg" )
	FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-#{slot}tn.jpg", "#{$PHOTO_PATH}/#{code}-#{slot}tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-#{slot}tn.jpg" )
	FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-#{slot}.jpg", "#{$PHOTO_PATH}/#{code}-#{slot}.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-#{slot}.jpg" )
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.language( script )


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
	recipe.load_db( code ) unless code == ''

when 'save'
	recipe.load_cgi( @cgi )

	# excepting for tags
	recipe.protocol.gsub!( '<', '&lt;')
	recipe.protocol.gsub!( '>', '&gt;')
	recipe.protocol.gsub!( ';', '；')

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
		pre_recipe.load_db( code )
		recipe.sum = r.first['sum']
		recipe.dish = r.first['dish'].to_i
		recipe.fig1 = pre_recipe.fig1
		recipe.fig2 = pre_recipe.fig2
		recipe.fig3 = pre_recipe.fig3

		copy_flag = false

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
			recipe.code = generate_code( user.name, 'r' )

			# Copying name
			if recipe.name == pre_recipe.name
				t = pre_recipe.name.match( /\((\d+)\)$/ )
				sn = 1
				sn = t[1].to_i + 1 if t != nil
				pre_recipe.name.sub!( /\((\d+)\)$/, '' )
				recipe.name = "#{pre_recipe.name}(#{sn})"
			end

			# Cocying figs
			if recipe.fig1 == 1 || recipe.fig2 == 1 || recipe.fig3 == 1
			require 'fileutils'
				copy_fig( 1, recipe.code, pre_recipe.code )if recipe.fig1 == 1
				copy_fig( 2, recipe.code, pre_recipe.code )if recipe.fig2 == 1
				copy_fig( 3, recipe.code, pre_recipe.code )if recipe.fig3 == 1
			end
			recipe.insert_db
		end
	end

	mdb( "UPDATE #{$MYSQL_TB_SUM} SET name='#{recipe.name}', code='#{recipe.code}', protect='#{recipe.protect}' WHERE user='#{user.name}';", false, @debug )
end


# HTML SELECT Recipe attribute
check_public = checked( recipe.public )
check_protect = checked( recipe.protect )
check_draft =  checked( recipe.draft )


# HTML SELECT Recipe type
html_type = lp[1]
html_type << '<select class="form-select form-select-sm" id="type">'
@recipe_type.size.times do |c|
	if recipe.type == c
		html_type << "<option value='#{c}' SELECTED>#{@recipe_type[c]}</option>"
	else
		html_type << "<option value='#{c}'>#{@recipe_type[c]}</option>"
	end
end
html_type << '</select>'


# HTML SELECT Recipe role
html_role = lp[2]
html_role << '<select class="form-select form-select-sm" id="role">'
@recipe_role.size.times do |c|
	if recipe.role == c
		html_role << "<option value='#{c}' SELECTED>#{@recipe_role[c]}</option>"
	else
		html_role << "<option value='#{c}'>#{@recipe_role[c]}</option>"
	end
end
if recipe.role == 100
	html_role << "<option value='100' SELECTED>[ 調味％ ]</option>"
else
	html_role << "<option value='100'>[ 調味％ ]</option>"
end
html_role << '</select>'


# HTML SELECT Recipe technique
html_tech = lp[3]
html_tech << '<select class="form-select form-select-sm" id="tech">'
@recipe_tech.size.times do |c|
	if recipe.tech == c
		html_tech << "<option value='#{c}' SELECTED>#{@recipe_tech[c]}</option>"
	else
		html_tech << "<option value='#{c}'>#{@recipe_tech[c]}</option>"
	end
end
html_tech << '</select>'


# HTML SELECT Recipe time
html_time = lp[4]
html_time << '<select class="form-select form-select-sm" id="time">'
@recipe_time.size.times do |c|
	if recipe.time == c
		html_time << "<option value='#{c}' SELECTED>#{@recipe_time[c]}</option>"
	else
		html_time << "<option value='#{c}'>#{@recipe_time[c]}</option>"
	end
end
html_time << '</select>'


# HTML SELECT Recipe cost
html_cost = lp[5]
html_cost << '<select class="form-select form-select-sm" id="cost">'
@recipe_cost.size.times do |c|
	if recipe.cost == c
		html_cost << "<option value='#{c}' SELECTED>#{@recipe_cost[c]}</option>"
	else
		html_cost << "<option value='#{c}'>#{@recipe_cost[c]}</option>"
	end
end
html_cost << '</select>'


#### HTML FORM recipe
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-3'><h5>#{lp[6]}</h5></div>
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
	<div align='right' class='code'>#{recipe.code}</div>
</div>
HTML

puts html
