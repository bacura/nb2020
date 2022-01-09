#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser cooking school custom 0.01b


#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


#==============================================================================
#STATIC
#==============================================================================
script = 'school-custom'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

# Cooking school course
class Custom
  attr_accessor :code, :name, :format, :enable, :checked, :title, :menu_group, :document, :print_ins, :qr_ins

  def initialize()
  	@code = ''
  	@name = ''
  	@format = 0
    @enable = []
    @checked = []
    @title = []
    @menu_group = []
    @document = []
    @print_ins = ''
    @qr_ins = ''
    @debug = false
  end

  def cgi( cgi )
  	@code = cgi['cs_code'].to_s
  	@name = cgi['cs_name'].to_s
  	@format = cgi['format'].to_i
    @print_ins = cgi["print_ins"].to_s
    @qr_ins = cgi["qe_ins"].to_s
  	4.times do |c|
    	@enable[c] = cgi["enable#{c}"].to_i
			@checked[c] = 'CHECKED' if @enable[c] == 1
    	@title[c] = cgi["title#{c}"].to_s
    	@menu_group[c] = cgi["menu_group#{c}"].to_s
    	@document[c] = cgi["document#{c}"].to_s
  	end
  end

  def load_db( user )
  	r = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLC} WHERE user='#{user.name}';", false, @debug )
		if r.first
  		@code = r.first['code'].to_s
  		@name = r.first['name'].to_s
  		@format = r.first['format'].to_i
    	@print_ins = r.first["print_ins"].to_s
    	@qr_ins = r.first["qe_ins"].to_s
  		4.times do |c|
    		@enable[c] = r.first["enable#{c}"].to_i
				@checked[c] = 'CHECKED' if @enable[c] == 1
    		@title[c] = r.first["title#{c}"].to_s
    		@menu_group[c] = r.first["menu_group#{c}"].to_s
    		@document[c] = r.first["document#{c}"].to_s
    	end
    end
  end

  def save_db( user )
  	set_set = "code='#{@code}', name='#{@name}', format='#{@format}', print_ins='#{@print_ins}', qr_ins='#{@qr_ins}' "
  	4.times do |c|
			set_set << " ,title#{c}='#{@title[c]}', enable#{c}='#{@enable[c]}', menu_group#{c}='#{@menu_group[c]}', document#{c}='#{@document[c]}'"
  	end

  	r = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLC} WHERE user='#{user.name}';", false, @debug )
  	if r.first
  		mdb( "UPDATE #{$MYSQL_TB_SCHOOLC} SET #{set_set} WHERE user='#{user.name}';", false, @debug )
  	else
 			mdb( "INSERT INTO #{$MYSQL_TB_SCHOOLC} SET user='#{user.name}', #{set_set};", false, @debug )
  	end
  end

  def debug( debug )
  	@debug = debug
  	if @debug
			puts "code:#{@code}<br>\n"
			puts "name:#{@name}<br>\n"
			puts "enable:#{@enable}<br>\n"
			puts "title:#{@title}<br>\n"
			puts "menu_group:#{@menu_group}<br>\n"
			puts "document:#{@document}<br>\n"
		end
  end
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )

#### Guild member check
if user.status < 5 && !@debug
	puts "Guild member shun error."
	exit
end


puts 'Getting POST<br>' if @debug
command = @cgi['command']
if @debug
	puts "command:#{command}<br>\n"
	puts "<hr>\n"
end


custom = Custom.new()
if command == 'save'
		custom.cgi( @cgi )
		custom.save_db( user )
else
		custom.load_db( user )
end
custom.debug( @debug )


menu_group_option = [ '', '', '', '' ]
r = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLM} WHERE user='#{user.name}';", false, @debug )
r.each do |e|
	4.times do |c|
		if e['label_group'] == custom.menu_group[c]
			menu_group_option[c] << "<option value=\"#{e['label_group']}\" SELECTED>#{e['label_group']}</option>"
		else
			menu_group_option[c] << "<option value=\"#{e['label_group']}\">#{e['label_group']}</option>"
		end
	end
end


puts 'html_course<br>' if @debug
html_course = []
4.times do |c|
	html_course[c] = <<-"HTML_COURSE"
	<div class='row'>
		<div class='col-2'>
			<div class="form-check form-switch">
				<input class="form-check-input" type="checkbox" id="enable#{c}" #{custom.checked[c]}>
				<label class="form-check-label"><h5>#{lp[3]}#{c}</h5></label>
			</div>
		</div>
		<div class='col-4'>
			<input type="text" class="form-control" id="title#{c}" value="#{custom.title[c]}">
		</div>

		<div class='col-4'>
			<div class="input-group mb-3">
				<label class="input-group-text">#{lp[7]}</label>
				<select class="form-select" id="menu_group#{c}">
					#{menu_group_option[c]}
				</select>
			</div>
		</div>
	</div>
	<div class='row'>
		<div class='col-2'></div>
		<div class='col-10'>
			<label class="form-label">#{lp[8]}</label>
			<textarea class="form-control" id="document#{c}" rows="3">#{custom.document[c]}</textarea>
		</div>
	</div>
HTML_COURSE

end


puts 'HTML<br>' if @debug
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{lp[1]}</h5></div>
		<div class="col-2">
			<input type="text" class="form-control" id="cs_code" value="#{custom.code}" max="32">
		</div>
		<div class="col-2">
			#{lp[9]}
		</div>

		<div class='col-2'><h5>#{lp[2]}</h5></div>
		<div class='col'>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="format" id="format_m" value="1" CHECKED>
				<label class="form-check-label">#{lp[10]}</label>
			</div>
			<div class="form-check form-check-inline">
  				<input class="form-check-input" type="radio" name="format" id="format_w" value="2" disabled>
				<label class="form-check-label">#{lp[11]}</label>
			</div>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="format" id="format_dw" value="3" disabled>
				<label class="form-check-label">#{lp[12]}</label>
			</div>
		</div>
		<div align='right' class="col-1">
			<button type="button" class='btn btn-sm btn-outline-primary' onclick="saveSchoolCustom()">#{lp[5]}</button>
		</div>
	</div>
	<br>

	<div class='row'>
		<div class='col-2'><h5>#{lp[14]}</h5></div>
		<div class="col-4">
			<input type="text" class="form-control" id="cs_name" value="#{custom.name}" max="255">
		</div>
	</div>
	<br>

	#{html_course[0]}
	<br>
	#{html_course[1]}
	<br>
	#{html_course[2]}
	<br>
	#{html_course[3]}
	<br>

	<div class='row'>
		<div class='col-2'><h5>#{lp[4]}</h5></div>
		<div class='col-10'>
			<textarea class="form-control" id="print_ins" rows="3" value="#{custom.print_ins}"></textarea>
		</div>
	</div>
	<br>

	<div class='row'>
		<div class='col-2'><h5>#{lp[6]}</h5></div>
		<div class='col-10'>
			<input type="text" class="form-control" id="qr_ins" value="#{custom.qr_ins}" max="128">
		</div>
	</div>
HTML

puts html
