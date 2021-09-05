#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser cooking school custom 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'school-custom'
@debug = true


#==============================================================================
#DEFINITION
#==============================================================================

# Cooking school course
class Course
  attr_accessor :enable, :title, :menu_group, :document, :c_order

  def initialize()
    @enable = 0
    @title = ''
    @menu_group = ''
    @document = ''
    @c_order = 0
  end

  def cgi( cgi )
    @enable = @cgi['enable'].to_i
    @cs_code = @cgi['cs_code'].to_i
    @title = @cgi['title'].to_s
    @menu_group = @cgi['menu_group'].to_s
    @document = @cgi['document'].to_s
    @c_order = @cgi['c_order'].to_i
  end

  def load_db( user, c_order )
  	r = mdb( "SELECT * FROM #{} WHERE user='#{user.name}' AND order='#{c_order}';", false, false )
  	if r.first
    	@enable = r.first['enable'].to_i
    	@title = r.first['title'].to_s
    	@menu_group = r.first['menu_group'].to_s
    	@document = r.first['document'].to_s
    	@c_order = r.first['c_order'].to_i
	end
  end

  def save_db( user )
    @enable = @cgi['enable'].to_i
    @title = @cgi['title'].to_s
    @menu_group = @cgi['menu_group'].to_s
    @document = @cgi['document'].to_s
    @c_order = @cgi['c_order'].to_i
  end

  def debug()
	puts "enable:#{@enable}<br>\n"
	puts "title:#{@title}<br>\n"
	puts "menu_group:#{@menu_group}<br>\n"
	puts "document:#{document}<br>\n"
	puts "c_order:#{c_order}<br>\n"
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


#### Getting POST
command = @cgi['command']
cs_code = @cgi['cs_code'].to_s
cs_format = @cgi['format'].to_i
if @debug
	puts "command:#{command}<br>\n"
	puts "cs_code:#{cs_code}<br>\n"
	puts "cs_format:#{cs_format}<br>\n"
	puts "<hr>\n"
end

courses = []
4.times do |c|
	courses[i] = Course.new
	if command == 'save'
		courses[c] = Course.cgi( @cgi )
	else
		courses[c] = Course.load_db( user, c )
	end
end

html_course = []
4.times do |c|
	html_course[c] = <<-"HTML_COURSE"
	<div class='row'>
		<div class='col-2'>
			<div class="form-check form-switch">
				<input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault">
				<label class="form-check-label"><h5>#{lp[3]}</h5></label>
			</div>
		</div>
		<div class='col-4'>
			<input type="text" class="form-control" id="title#{c}" value="#{courses[c].tile}">
		</div>

		<div class='col-4'>
			<div class="input-group mb-3">
				<label class="input-group-text">#{lp[7]}</label>
				<select class="form-select" id="c1group">
					<option selected>Choose...</option>
					<option value="1">One</option>
					<option value="2">Two</option>
					<option value="3">Three</option>
				</select>
			</div>
		</div>
	</div>
	<div class='row'>
		<div class='col-2'></div>
		<div class='col-10'>
			<label class="form-label">#{lp[8]}</label>
			<textarea class="form-control" id="c1text" rows="5"></textarea>
		</div>
	</div>
HTML_COURSE

end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{lp[1]}</h5></div>
		<div class="col-2">
			<input type="text" class="form-control" id="cs_code" value="#{cs_code}">
		</div>
		<div class="col">
			#{lp[9]}
		</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-2'><h5>#{lp[2]}</h5></div>
		<div class='col'>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="cs_mode" id="cs_mode_m" value="1">
				<label class="form-check-label">#{lp[10]}</label>
			</div>
			<div class="form-check form-check-inline">
  				<input class="form-check-input" type="radio" name="cs_mode" id="cs_mode_w" value="2" disabled>
				<label class="form-check-label">#{lp[11]}</label>
			</div>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" name="cs_mode" id="cs_mode_dw" value="3" disabled>
				<label class="form-check-label">#{lp[12]}</label>
			</div>
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


HTML

puts html
