#! /usr/bin/ruby
#encoding: utf-8
#Nutritoin browser history 0.10b


#==============================================================================
# LIBRARY
#==============================================================================
require './probe'


#==============================================================================
# STATIC
#==============================================================================
@debug = false
script = 'history'
$ALL_LIMIT = 100


#==============================================================================
# DEFINITION
#==============================================================================

#### Getting history
def get_histry( lp, user, sub_fg )
	db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
	history = []
	res = db.query( "SELECT his FROM #{$MYSQL_TB_HIS} WHERE user='#{user.name}';" )
	t = res.first['his'].split( "\t" )

	gycv = false
	if sub_fg == '6_'
		gycv = true
		sub_fg = '6'
	end

	if sub_fg == 'all'
		$ALL_LIMIT.times do |c|
			break if c > t.size - 1
			history << t[c]
		end
	else
		t.each do |e|
			if /P|U/ =~ e
				history << e if e[1..2].to_i == sub_fg.to_i
			else
				history << e if e[0..1].to_i == sub_fg.to_i
			end
		end
	end

	html = ''
	history.each do |e|
		q = "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{e}';"
		r_tag = db.query( q )
		if sub_fg == '6'
			res2 = db.query( "SELECT gycv FROM #{$MYSQL_TB_EXT} WHERE FN='#{e}';" )
			if res2.first
				next if res2.first['gycv'] == 1 && ( not gycv )
				next if res2.first['gycv'] != 1 && gycv
			end
		end


		food_name = r_tag.first['name']
		tags = bind_tags( r_tag ) if r_tag.first

		# buttons
		add_button = "<span onclick=\"addingCB( '#{e}', '', '#{food_name}' )\">#{lp[3]}</span>" if user.name
		koyomi_button = "<span onclick=\"addKoyomi( '#{e}', 1 )\">#{lp[35]}</span>" if user.status >= 2

		html << "<tr class='fct_value'><td class='link_cursor' onclick=\"detailView_his( '#{e}' )\">#{tags}</td><td>#{add_button}&nbsp;#{koyomi_button}</td></tr>\n"
	end
	db.close

	return html
end

#### Sub group HTML
def sub_menu( lp )
	html_sub = <<-"HTML_SUB"
<span class="btn badge rounded-pill bg-info text-dark" onclick="historySub( '1' )">#{lp[7]}</span>
<span class="btn badge rounded-pill bg-info text-dark" onclick="historySub( '2' )">#{lp[8]}</span>
<span class="btn badge rounded-pill bg-info text-dark" onclick="historySub( '3' )">#{lp[9]}</span>
<span class="btn badge rounded-pill bg-danger" onclick="historySub( '4' )">#{lp[10]}</span>
<span class="btn badge rounded-pill bg-warning text-dark" onclick="historySub( '5' )">#{lp[11]}</span>
<span class="btn badge rounded-pill bg-light text-success" onclick="historySub( '6' )">#{lp[12]}</span>
<span class="btn badge rounded-pill bg-success" onclick="historySub( '6_' )">#{lp[12]}</span>
<span class="btn badge rounded-pill bg-info text-dark" onclick="historySub( '7' )">#{lp[13]}</span>
<span class="btn badge rounded-pill bg-success" onclick="historySub( '8' )">#{lp[14]}</span>
<span class="btn badge rounded-pill bg-success" onclick="historySub( '9' )">#{lp[15]}</span>
<span class="btn badge rounded-pill bg-danger" onclick="historySub( '10' )">#{lp[16]}</span>
<span class="btn badge rounded-pill bg-danger" onclick="historySub( '11' )">#{lp[17]}</span>
<span class="btn badge rounded-pill bg-danger" onclick="historySub( '12' )">#{lp[18]}</span>
<span class="btn badge rounded-pill bg-light text-dark" onclick="historySub( '13' )">#{lp[19]}</span>
<span class="btn badge rounded-pill bg-warning text-dark" onclick="historySub( '14' )">#{lp[20]}</span>
<span class="btn badge rounded-pill bg-secondary" onclick="historySub( '15' )">#{lp[21]}</span>
<span class="btn badge rounded-pill bg-primary" onclick="historySub( '16' )">#{lp[22]}</span>
<span class="btn badge rounded-pill bg-light text-dark" onclick="historySub( '17' )">#{lp[23]}</span>
<span class="btn badge rounded-pill bg-secondary" onclick="historySub( '18' )">#{lp[24]}</span>
<span class="btn badge rounded-pill bg-light text-dark" onclick="historySub( '00' )">#{lp[25]}</span>
HTML_SUB
	puts html_sub
	exit
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


#### Getting POST
command = @cgi['command']
sub_fg = @cgi['sub_fg']
if @debug
	puts "command: #{command}<br>"
	puts "sub_fg: #{sub_fg}<br>"
	puts "<hr>"
end


#### Sub group menu
sub_menu( lp ) if command == 'menu'


#### Sub group
if sub_fg == 'init'
	r = mdb( "SELECT his_sg FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
	if r.first
		sub_fg = r.first['his_sg']
	else
		sub_fg = 1
	end
end


#### グループ名変換
sub_title = ''
if sub_fg == '00'
	sub_title = "#{lp[2]}"
elsif sub_fg == '6'
	sub_title = "#{lp[5]}"
elsif sub_fg == '6_'
	sub_title = "#{lp[6]}"
else
	sub_title = @category[sub_fg.to_i]
end


#### 各食品ラインの生成
food_html_all = get_histry( lp, user, 'all' )
food_html_sg = get_histry( lp, user, sub_fg )


#### HTML生成
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col">
			<h5>#{lp[27]}: #{lp[1]}</h5>
			<table class="table table-sm table-hover">
				#{food_html_all}
			</table>
		</div>
		<div class="col">
			<h5>#{lp[27]}: #{sub_title}</h5>
			<table class="table table-sm table-hover">
				#{food_html_sg}
			</table>
		</div>
	</div>
</div>
HTML

puts html

r = mdb( "SELECT user FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
if r.first
	mdb( "UPDATE #{$MYSQL_TB_CFG} SET his_sg='#{sub_fg}' WHERE user='#{user.name}';", false, @debug )
else
	mdb( "INSERT INTO #{$MYSQL_TB_CFG} SET his_sg='#{sub_fg}' ,user='#{user.name}';", false, @debug )
end
