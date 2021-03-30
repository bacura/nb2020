#! /usr/bin/ruby
# coding: UTF-8
#Nutrition browser cooking school yoyaku Mobi 0.00b

#==============================================================================
#CHANGE LOG
#==============================================================================
#20200520, 0.00, start


#==============================================================================
#MEMO
#==============================================================================
#ampm:0->am, 1->pm
#status:0->close, 1->Reserved, 7->No show, 8->Done, 9->Open

#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'
require 'mail'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'yoyaku-mobi'

ampm_time = []
ampm_time[0] = '午前'
ampm_time[1] = '午後'

basic_label = %w( [基礎-和1] [基礎-和1s] [基礎-洋1] [基礎-洋1s] [基礎-中1] [基礎-中1s] )
season_label = %w( [季節-和1] [季節-和1s] [季節-洋1] [季節-洋1s] [基礎-中1] [基礎-中1s] )

weeks = %w( 日 月 火 水 木 金 土 )

#==============================================================================
#DEFINITION
#==============================================================================

class Reservation
	attr_accessor :yyyy, :mm, :dd, :wd, :status_am, :status_pm, :available

	def initialize( yyyy, mm, dd, available )
    	@yyyy = yyyy
    	@mm = mm
    	@dd = dd
    	@wd = Date.new( yyyy, mm, dd ).wday unless dd == 0
		@available = available
    	@status_am = 0
    	@status_pm = 0
		r = mdb( "SELECT ampm, status FROM #{$MYSQL_TB_SCHOOLK} WHERE date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
		r.each do |e|
			if e['status'] != 0
				if e['ampm'] == 0
					@status_am = e['status']
				else
					@status_pm = e['status']
				end
			end
		end
	end
end


def html_header()
	html = <<-"HTML"
<!DOCTYPE html>
<head>
  <title>嵯峨お料理教室予約フォーム</title>
  <meta charset="UTF-8">
  <meta name="keywords" content="嵯峨お料理教室,予約">
  <meta name="description" content="京都市右京区の料理教室、嵯峨お料理教室の予約フォーム">
  <meta name="robots" content="index,follow">
  <meta name="author" content="Shinji Yoshiyama">
  <!-- bootstrap -->
  <link rel="stylesheet" href="bootstrap-dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="#{$CSS_PATH}/core.css">
<!-- Jquery -->
  <script type="text/javascript" src="./jquery-3.5.1.min.js"></script>
<!-- bootstrap -->
  <script type="text/javascript" src="bootstrap-dist/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="#{$JS_PATH}/core.js"></script>
  <script type="text/javascript" src="#{$JS_PATH}/shun.js"></script>

 #{tracking()}
</head>

<body class="body">
  <span class="world_frame" id="world_frame">
HTML

	puts html
end


def mail_message( message )
	mail = Mail.new
	mail.charset = 'UTF-8'
	mail.from = 'info@bacura.jp'
	mail.to = 'yossy@bacura.jp'
	mail.subject = 'Message[SCS]'
	mail.body = message

	mail.delivery_method( :smtp, address:'localhost', port:25 )
	mail.deliver
end


#==============================================================================
# Main
#==============================================================================
#### Getting Cookie
cgi = CGI.new
user = User.new( cgi )
user.status = 8
#lp = lp_init( 'yoyaku', language )

html_init( nil )
html_header()


#### Getting GET
get = get_data()
command = get['command']
yyyy = get['yyyy'].to_i
mm = get['mm'].to_i
dd = get['dd'].to_i
dd = 1 if dd == 0
ampm = get['ampm'].to_i
if @debug
  puts "command:#{command}<br>\n"
  puts "yyyy:#{yyyy}<br>\n"
  puts "mm:#{mm}<br>\n"
  puts "dd:#{dd}<br>\n"
  puts "mapm:#{ampm}<br>\n"
  puts "<hr>\n"
end


case command
#==============================================================================
# 基本の献立コース
when 'basic'
#==============================================================================
menu_html = ''
basic_label.each do |e|
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MENU} WHERE label='#{e}' AND protect='1';", false, @debug )
	if r.first
		menu_html << "<div class='row'>"
		menu_html << "	<div class='col-1' align='right'><input type='radio' name='menu' value='#{r.first['code']}' required class='form-check-input'></div>"
		menu_html << "	<div class='col'>"
		menu_html << "		<h4>#{r.first['name']}</h4>"

	 	recipe_set = r.first['meal'].split( "\t" )
	 	recipe_set.each do |ee|
			rr = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{ee}' AND public='1';", false, @debug )
			if rr.first
				menu_html << "<img src='photo/#{rr.first['code']}-1tns.jpg' style='border-radius:5px;'>&nbsp;"
				menu_html << "#{rr.first['name']}&nbsp;&nbsp;&nbsp;"
			end
	 	end

		menu_html << "	</div>"
		menu_html << "</div>"
		menu_html << "<hr>"
	end

end

name_html = ''
name_html = "<div align='center' class='month'>#{user.name} さん</div>" if user.name != '' && user.name != nil

html = <<-"HTML"
<div align="right">[<a href='#{script}.cgi?command=select&yyyy=#{yyyy}&mm=#{mm}&dd=#{dd}&ampm=#{ampm}'>コース選択に戻る</a>]</div>
<div align="center" class='month'>嵯峨お料理教室 予約</div>
#{name_html}
<div align="center" class='month'>#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}</div>
<hr>
<h3 align="center">[基礎の献立コース] 献立を選んで予約してください。</h3>
<hr>
<ul class='h3'>
	<li>受講料は5品献立：1人2000円。3品献立：1人1500円。</li>
	<li>3品献立にはレトルトまたは冷凍のご飯が付きます。</li>
	<li>1～2人で受講できます。※5品献立は2人での受講をオススメします。<br>
	<li>5品献立は2人で試食、後片付けを含め、3時間程かかります。<br>
</ul>
<hr>
<br>

<form action='#{script}.cgi?command=basic_r&yyyy=#{yyyy}&mm=#{mm}&dd=#{dd}&ampm=#{ampm}' method='post'>
<div class='container'>
	<div class='row'>
		<div align='right' class='col-2'>代表者のお名前</div>
		<div class='col-5'><input type='text' name='student' size='30' maxlength='30' class='form-control form-control-lg' required></div>
	</div>
	<br>
	<div class='row'>
		<div align='right' class='col-2'>メールアドレス</div>
		<div class='col-5'><input type='email' name='pass' size='60' maxlength='30' class='form-control form-control-lg' required></div>
	</div>
	<div class='row'>
		<div align='right' class='col-2'></div>
		<div class='col-5'>※メールアドレスの不備によるトラブルは関知いたしません。</div>
	</div>
	<div class='row'>
		<div align='right' class='col-2'>参加人数</div>
		<div class='col-5'>
			<select name='num' class='form-select form-select-lg'>
				<option valuse='1'>1</option>
				<option valuse='2'>2</option>
				<option valuse='3'>3</option>
			</select>
		</div>
	</div>
	<hr>
	#{menu_html}
	<br>
	<div align='center'><input type='submit' value='予約する' class='btn btn-lg btn-info'></div>
</div>
</form>
HTML

when 'basic_r'
#### 基本の献立コース応答

menu = cgi['menu']
student = cgi['student']
num = cgi['num']
pass = cgi['pass']

r = mdb( "SELECT * FROM #{$MYSQL_TB_MENU} WHERE code='#{menu}' AND protect=1;", false, @debug )
menu_name = r.first['name']

html = <<-"HTML"
<div align="right">[<a href='#{script}.cgi'>カレンダーに戻る</a>]</div>
<div align="center" class='month'>嵯峨お料理教室 予約</div>

<div align="center" class='month'>#{student} さん</div>
<div align="center" class='month'>#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}</div>
<hr>
<h3 align="center">[基本の献立コース]</h3>
<hr>
<div align="center" class='h4'>選択献立：#{menu_name} [#{num}人] 予約完了しました。</div>
HTML

mdb( "UPDATE #{$MYSQL_TB_SCHOOLK} SET user='#{user.name}', student='#{student}', num='#{num}', pass='#{pass}', menu='#{menu}', status=1 WHERE ampm=#{ampm} AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )

message = "#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}\n[基本の献立コース]\n#{student} さん\n#{menu_name} [#{num}人] 予約が入りました。"
mail_message( message )

#==============================================================================
# 季節の献立コース
when 'monthly'
#==============================================================================
menu_html = ''
season_label.each do |e|
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MENU} WHERE label='#{e}' AND protect='1';", false, @debug )
	if r.first
		menu_html << "<div class='row'>"
		menu_html << "	<div class='col-1' align='right'><input type='radio' name='menu' value='#{r.first['code']}' required class='form-check-input'></div>"
		menu_html << "	<div class='col'>"
		menu_html << "		<h4>#{r.first['name']}</h4>"

	 	recipe_set = r.first['meal'].split( "\t" )
	 	recipe_set.each do |ee|
			rr = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{ee}' AND public='1';", false, @debug )
			if rr.first
				menu_html << "<img src='photo/#{rr.first['code']}-1tns.jpg' style='border-radius:5px;'>&nbsp;"
				menu_html << "#{rr.first['name']}&nbsp;&nbsp;&nbsp;"
			end
	 	end

		menu_html << "	</div>"
		menu_html << "</div>"
		menu_html << "<hr>"
	end

end

name_html = ''
name_html = "<div align='center' class='month'>#{user.name} さん</div>" if user.name != '' && user.name != nil

html = <<-"HTML"
<div align="right">[<a href='#{script}.cgi?command=select&yyyy=#{yyyy}&mm=#{mm}&dd=#{dd}&ampm=#{ampm}'>コース選択に戻る</a>]</div>
<div align="center" class='month'>嵯峨お料理教室 予約</div>
#{name_html}
<div align="center" class='month'>#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}</div>
<hr>
<h3 align="center">[季節の献立コース] 献立を選んで予約してください。</h3>
<hr>
<ul class='h3'>
	<li>受講料は5品献立：1人2000円。3品献立：1人1500円。</li>
	<li>3品献立にはレトルトまたは冷凍のご飯が付きます。</li>
	<li>1～2人で受講できます。※5品献立は2人での受講をオススメします。<br>
	<li>5品献立は2人で試食、後片付けを含め、3時間程かかります。<br>
</ul>
<hr>
<form action='#{script}.cgi?command=monthly_r&yyyy=#{yyyy}&mm=#{mm}&dd=#{dd}&ampm=#{ampm}' method='post'>
<div class='container'>
	<div class='row'>
		<div align='right' class='col-2'>代表者のお名前</div>
		<div class='col-5'><input type='text' name='student' size='30' maxlength='30' class='form-control form-control-lg' required></div>
	</div>
	<br>
	<div class='row'>
		<div align='right' class='col-2'>メールアドレス</div>
		<div class='col-5'><input type='email' name='pass' size='60' maxlength='30' class='form-control form-control-lg' required></div>
	</div>
	<div class='row'>
		<div align='right' class='col-2'></div>
		<div class='col-5'>※メールアドレスの不備によるトラブルは関知いたしません。</div>
	</div>
	<div class='row'>
		<div align='right' class='col-2'>参加人数</div>
		<div class='col-5'>
			<select name='num' class='form-select form-select-lg'>
				<option valuse='1'>1</option>
				<option valuse='2'>2</option>
				<option valuse='3'>3</option>
			</select>
		</div>
	</div>
	<hr>
	#{menu_html}
	<br>
	<div align='center'><input type='submit' value='予約する' class='btn btn-lg btn-info'></div>
</div>
</form>
HTML

when 'monthly_r'
#### 季節の献立コース応答

menu = cgi['menu']
student = cgi['student']
num = cgi['num']
pass = cgi['pass']

r = mdb( "SELECT * FROM #{$MYSQL_TB_MENU} WHERE code='#{menu}' AND protect=1;", false, @debug )
menu_name = r.first['name']

html = <<-"HTML"
<div align="right">[<a href='#{script}.cgi'>カレンダーに戻る</a>]</div>
<div align="center" class='month'>嵯峨お料理教室 予約</div>

<div align="center" class='month'>#{student} さん</div>
<div align="center" class='month'>#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}</div>
<hr>
<h3 align="center">[基本の献立コース]</h3>
<hr>
<div align="center" class='h4'>選択献立：#{menu_name} [#{num}人] 予約完了しました。</div>
HTML

mdb( "UPDATE #{$MYSQL_TB_SCHOOLK} SET user='#{user.name}', student='#{student}', num='#{num}',pass='#{pass}', menu='#{menu}', status=1 WHERE ampm=#{ampm} AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )

message = "#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}\n[基本の献立コース]\n#{student} さん\n#{menu_name} [#{num}人] 予約が入りました。"
mail_message( message )

#==============================================================================
# 自由なの献立コース
when 'free'
#==============================================================================
name_html = ''
name_html = "<div align='center' class='month'>#{user.name} さん</div>" if user.name != '' && user.name != nil

html = <<-"HTML"
<div align="right">[<a href='#{script}.cgi?command=select&yyyy=#{yyyy}&mm=#{mm}&dd=#{dd}&ampm=#{ampm}'>コース選択に戻る</a>]</div>
<div align="center" class='month'>嵯峨お料理教室 予約</div>
#{name_html}
<div align="center" class='month'>#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}</div>
<hr>
<h3 align="center">[自由な献立コース] 献立を作成して予約してください。</h3>
<hr>
HTML

#==============================================================================
# キッチン間借りコース
when 'sfree'
#==============================================================================
name_html = ''
name_html = "<div align='center' class='month'>#{user.name} さん</div>" if user.name != '' && user.name != nil
name_form_html = "<input type='text' name='student' size='30' maxlength='30'>"
time_select_html = ''
if ampm == 0
	time_select_html << "<div class='input-group'>"
	time_select_html << "<select name='start_h' class='form-select form-select-lg'>"
	time_select_html << "<option valuse='9' SELECTED>9:00</option>"
	time_select_html << "<option valuse='10'>10:00</option>"
	time_select_html << "<option valuse='11'>11:00</option>"
	time_select_html << "<option valuse='12'>12:00</option>"
	time_select_html << "</select>"
	time_select_html << "<span class='h2'>&nbsp;→&nbsp;</span>"
	time_select_html << "<select name='end_h' class='form-select form-select-lg'>"
	time_select_html << "<option valuse='9'>10:00</option>"
	time_select_html << "<option valuse='11'>11:00</option>"
	time_select_html << "<option valuse='12'>12:00</option>"
	time_select_html << "<option valuse='13' SELECTED>13:00</option>"
	time_select_html << "</select>"
	time_select_html << "</div>"
else
	time_select_html << "<div class='input-group'>"
	time_select_html << "<select name='start_h' class='form-select form-select-lg'>"
	time_select_html << "<option valuse='16' SELECTED>16:00</option>"
	time_select_html << "<option valuse='17'>17:00</option>"
	time_select_html << "<option valuse='18'>18:00</option>"
	time_select_html << "<option valuse='19'>19:00</option>"
	time_select_html << "</select>"
	time_select_html << "<span class='h2'>&nbsp;→&nbsp;</span>"
	time_select_html << "<select name='end_h' class='form-select form-select-lg'>"
	time_select_html << "<option valuse='17'>17:00</option>"
	time_select_html << "<option valuse='18'>18:00</option>"
	time_select_html << "<option valuse='19'>19:00</option>"
	time_select_html << "<option valuse='20' SELECTED>20:00</option>"
	time_select_html << "</select>"
	time_select_html << "</div>"
end

html = <<-"HTML"
<div align="right">[<a href='#{script}.cgi?command=sfree_c&yyyy=#{yyyy}&mm=#{mm}&dd=#{dd}&ampm=#{ampm}'>コース選択に戻る</a>]</div>
<div align="center" class='month'>嵯峨お料理教室 予約</div>
#{name_html}
<div align="center" class='month'>#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}</div>
<hr>
<h1 align="center">[キッチン間借りコース]</h1>
<ul class='h3'>
	<li>ご利用人数にかかわらず1時間300円です。</li>
	<li>※食事、後片付けの時間も含みます。</li>
	<li>1～3人でご利用できます。<br>
</ul>
<hr>
<br>
<form action='#{script}.cgi?command=sfree_r&yyyy=#{yyyy}&mm=#{mm}&dd=#{dd}&ampm=#{ampm}' method='post'>
<div class='container'>
	<div class='row'>
		<div align='right' class='col-2'>代表者のお名前</div>
		<div class='col-9'><input type='text' name='student' size='30' maxlength='30' class='form-control form-control-lg' required></div>
	</div>
	<br>
	<div class='row'>
		<div align='right' class='col-2'>メールアドレス</div>
		<div class='col-9'><input type='email' name='pass' size='60' maxlength='30' class='form-control form-control-lg' required></div>
	</div>
	<div class='row'>
		<div align='right' class='col-2'></div>
		<div class='col-9'>※メールアドレスの不備によるトラブルは関知いたしません。</div>
	</div>
	<br>
	<div class='row'>
		<div align='right' class='col-2'>ご利用時間	</div>
		<div class='col-9'>#{time_select_html}</div>
	</div>
	<br>
	<div class='row'>
		<div align='right' class='col-2'>参加人数</div>
		<div class='col-9'>
			<select name='num' class='form-select form-select-lg'>
				<option valuse='1'>1</option>
				<option valuse='2'>2</option>
				<option valuse='3'>3</option>
			</select>
		</div>
	</div>
	<br>
	<div align='center'><input type='submit' value='予約する' class='btn btn-lg btn-info'></div>
</div>
</form>
HTML

when 'sfree_r'
#### キッチン間借りコース応答

start_h = cgi['start_h']
end_h = cgi['end_h']
student = cgi['student']
num = cgi['num']
pass = cgi['pass']

html = <<-"HTML"
<div align="right">[<a href='#{script}.cgi'>カレンダーに戻る</a>]</div>
<div align="center" class='month'>嵯峨お料理教室 予約</div>

<div align="center" class='month'>#{student} さん</div>
<div align="center" class='month'>#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}</div>
<hr>
<h3 align="center">[キッチン間借りコース]</h3>
<hr>
<div align="center" class='scs_message'>#{start_h} ~ #{end_h} [#{num}人] 予約完了しました。</div>
HTML

mdb( "UPDATE #{$MYSQL_TB_SCHOOLK} SET user='#{user.name}', student='#{student}', num=#{num}, pass='#{pass}', menu='sf#{start_h}-#{end_h}', status=1 WHERE ampm=#{ampm} AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )

message = "#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}\n[キッチン間借りコース]\n#{student} さん\n#{start_h} ~ #{end_h} [#{num}人] 予約が入りました。"
mail_message( message )

#==============================================================================
# コース選択
when 'select'
#==============================================================================

html = <<-"HTML"
<div align="right">[<a href='#{script}.cgi'>カレンダーに戻る</a>]</div>
<div align="center" class='month'>嵯峨お料理教室 予約</div>

<div align="center" class='month'>#{user.name} さん</div>
<div align="center" class='month'>#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}</div>
<hr>
<h3 align="center">献立コースを選択してください</h3>
<hr>

<div class='container-fluid'>
	<div class='row'>
		<div class='col-1'></div>
  		<div class='col-10 scs_course_mobi' onclick='window.location.href="#{script}.cgi?command=basic&yyyy=#{yyyy}&mm=#{mm}&dd=#{dd}&ampm=#{ampm}";'>
    		<h4 class='scs_menu'>基礎の献立コース</h4>
    		<ul>
    			<li>和食、洋食、中華の基礎的な献立から選べます。</li>
    			<li>未経験者、初心者にオススメです。</li>
    		</ul>
		</div>
		<div class='col-1'></div>
	</div>
	<br>
	<div class='row'>
		<div class='col-1'></div>
  		<div class='col-10 scs_course_mobi' onclick='window.location.href="#{script}.cgi?command=monthly&yyyy=#{yyyy}&mm=#{mm}&dd=#{dd}&ampm=#{ampm}";'>
			<h4 class='scs_menu'>季節の献立コース</h4>
    		<ul>
     			<li>月替わりで旬の食材を使用した和食、洋食、中華から選べます。</li>
    			<li>希にイベント特別教室があります。</li>
    		</ul>
  		</div>
		<div class='col-1'></div>
	</div>
	<br>
	<div class='row'>
		<div class='col-1'></div>
		<div class='col-10 scs_course_mobi' >
			<h4 class='scs_menu'>自由な献立コース<br>（現在は選択できません）</h4>
    		<ul>
     			<li>レシピデーターベースからお好きな料理を選べます。</li>
    			<li>料理の幅を広げたい方にオススメです。<br>
    		</ul>
		</div>
		<div class='col-1'></div>
	</div>
	<br>
	<div class='row'>
		<div class='col-1'></div>
		<div class='col-10 scs_course_mobi' onclick='window.location.href="#{script}.cgi?command=sfree&yyyy=#{yyyy}&mm=#{mm}&dd=#{dd}&ampm=#{ampm}";'>
			<h4 class='scs_menu'>キッチン間借りコース</h4>
    		<ul>
     			<li>教室の台所を使用してご自身で調理していただきます。</li>
    			<li>基礎調味料以外の食材は持ち込みになります。</li>
    			<li>ご利用できる調味料・機材一覧</li>
    		</ul>
		</div>
		<div class='col-1'></div>
	</div>
	<br>
</div>
HTML

#==============================================================================
# 予約のキャンセル
when 'cancel'
#==============================================================================
pass = cgi['pass']
cancel_flag = false

r = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLK} WHERE pass='#{pass}' AND ampm=#{ampm} AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
if user.status >= 8
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_SCHOOLK} SET status=9, user=NULL, pass=NULL, student=NULL, num=NULL, menu=NULL WHERE ampm=#{ampm} AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_SCHOOLK} SET status=9, ampm=#{ampm}, date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
	end
	cancel_flag = true
else
	if r.first
		if pass == r.first['pass']
			mdb( "UPDATE #{$MYSQL_TB_SCHOOLK} SET status=9, user=NULL, pass=NULL, student=NULL, num=NULL, menu=NULL WHERE ampm='#{ampm}' AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
			cancel_flag = true
		end
	end
end
message = '予約をキャンセル出来ませんでした。メールなどで連絡してください'
message = '予約をキャンセルしました。' if cancel_flag

html = <<-"HTML"
<div align="right">[<a href='#{script}.cgi'>カレンダーに戻る</a>]</div>
<div align="center" class='month'>嵯峨お料理教室 予約キャンセル</div>
<div align="center" class='month'>#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}</div>
<hr>
<h3 align="center">#{message}</h3>
<hr>
HTML

if cancel_flag
	message = "#{yyyy}年 #{mm}月 #{dd}日 #{ampm_time[ampm]}\n予約がキャンセルされました。"
	mail_message( message )
end


#==============================================================================
# 予約の確認
when 'confirm'
#==============================================================================
pass = cgi['pass']

confirm_message = '<div align="center" class="h4">現在、このメールアドレスでの予約はありません。</div>'
r = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLK} WHERE pass='#{pass}' AND status=1;", false, @debug )
if r.first
	confirm_message = ''
	r.each do |e|
		confirm_message << "<div class='row h5'>"
		confirm_message << "<div class='col-1'></div>"
		confirm_message << "<div class='col-2'>#{e['date']}<br>#{ampm_time[e['ampm']]}</div>"
		confirm_message << "<div class='col-2'>#{e['student']} さん</div>"
		confirm_message << "<div class='col-1'>#{e['num']} 人</div>"
		if e['menu'] =~ /\-m\-/
			rr = mdb( "SELECT * FROM #{$MYSQL_TB_MENU} WHERE code='#{e['menu']}' AND protect='1';", false, @debug )
			confirm_message << "<div class='col-3'>#{rr.first['name']}</div>"
		else
			sfree = e['menu'].sub( 'sf', 'キッチン間借り:' )
			confirm_message << "<div class='col-3'>#{sfree}</div>"
		end
		a = e['date'].to_s.split( '-' )
		confirm_message << "<div class='col-1'><form action='#{script}.cgi?command=cancel&yyyy=#{a[0]}&mm=#{a[1].to_i}&dd=#{a[2].to_i}&ampm=#{e['ampm']}' method='post'>"
		confirm_message << "<input type='hidden' name='pass' value='#{pass}'>"
		confirm_message << "<input type='submit' class='btn btn-sm btn-warning' value='キャンセル'>"
		confirm_message << "</form></div>"
		confirm_message << '</div><br>'
	end
	confirm_message << '<br><div align="center">午前は9:30~10:00スタート、午後は17:00~17:30スタート。※キッチン間借りコースを除く。</div>'
end

html = <<-"HTML"
<div align="right">[<a href='#{script}.cgi'>カレンダーに戻る</a>]</div>
<div align="center" class='month'>嵯峨お料理教室 予約確認</div>
<hr>
<div align="center" class='scs_message'>#{pass}</div>
<hr>
#{confirm_message}
HTML


#==============================================================================
# カレンダー表示
#==============================================================================
else
	#### Date & calendar config
	calendar = Calendar.new( user.name, 0, 0, 1 )
	calendar.wf = 7 if calendar.wf == 0

	calendar_next = Calendar.new( user.name, 0, 0, 1 )
	calendar_next.move_mm( 1 )
	calendar_next.wf = 7 if calendar_next.wf == 0

	calendar.debug if @debug
	calendar_next.debug if @debug
	sql_ymd = "#{calendar.yyyy}-#{calendar.mm}-#{calendar.dd}"
	sql_ym = "#{calendar.yyyy}-#{calendar.mm}"


	calendar_set = []
	days = []
	mm_set = []
	yyyy_set = []
	1.upto( calendar.ddl ) do |c|
		days << c
		mm_set << calendar.mm
		yyyy_set << calendar.yyyy
		calendar_set << Reservation.new( calendar.yyyy, calendar.mm, c, true )
	end

	calendar_next_set = []
	days_next = []
	mm_next_set = []
	yyyy_next_set = []
	1.upto( calendar_next.ddl ) do |c|
		days_next << c
		mm_next_set << calendar_next.mm
		yyyy_next_set << calendar_next.yyyy
		calendar_next_set << Reservation.new( calendar_next.yyyy, calendar_next.mm, c, true )
	end

	#### This month
	week_count = 0
	cal_html = ''
	cal_html << "<tr><td width='20%'></td><td class='month'>午前</td><td class='month'>午後</td></tr>"

	0.upto( days.size - 1 ) do |c|
		week_c = 'weekday_mobi'
		week_c = 'sunday_mobi' if calendar_set[c].wd == 0
		week_c = 'saturday_mobi' if calendar_set[c].wd == 6

		if calendar_set[c].dd > calendar.dd + 1 && calendar_set[c].dd < calendar.dd + 29
			cal_html << "<tr>"
			cal_html << "<td class='#{week_c}' align='center'>#{days[c]} (#{weeks[calendar_set[c].wd]})</td>"
			if calendar_set[c].status_am == 9
				cal_html << "<td class='day_on'><a href='#{script}.cgi?command=select&yyyy=#{calendar_set[c].yyyy}&mm=#{calendar_set[c].mm}&dd=#{calendar_set[c].dd}&ampm=0'><div align='center' class='btn-outline-dark'>○</div></a></td>"
			elsif calendar_set[c].status_am == 0
				cal_html << "<td class='day_off_mobi text-success' align='center'>休</td>"
			else
				cal_html << "<td class='day_out text-danger' align='center'>×</td>"
			end

			if calendar_set[c].status_pm == 9
				cal_html << "<td class='day_on'><a href='#{script}.cgi?command=select&yyyy=#{calendar_set[c].yyyy}&mm=#{calendar_set[c].mm}&dd=#{calendar_set[c].dd}&ampm=1'><div align='center' class='btn-outline-dark'>○</div></a></td>"
			elsif calendar_set[c].status_pm == 0
				cal_html << "<td class='day_off_mobi text-success' align='center'>休</td>"
			else
				cal_html << "<td class='day_out text-danger' align='center'>×</td>"
			end
			cal_html << "</tr>"
		elsif calendar_set[c].dd == calendar.dd || calendar_set[c].dd == calendar.dd + 1
			cal_html << "<tr>"
			cal_html << "<td class='#{week_c}' align='center'>#{days[c]} (#{weeks[calendar_set[c].wd]})</td>"
			if calendar_set[c].status_am == 9 || calendar_set[c].status_am == 0
				cal_html << "<td class='day_off_mobi text-success' align='center'>休</td>"
			else
				cal_html << "<td class='day_out text-danger' align='center'>×</td>"
			end

			if calendar_set[c].status_pm == 9 || calendar_set[c].status_pm == 0
				cal_html << "<td class='day_off_mobi text-success' align='center'>休</td>"
			else
				cal_html << "<td class='day_out text-danger' align='center'>×</td>"
			end
			cal_html << "</tr>"
		end

		if week_count ==  6
			cal_html << '</tr>'
			week_count = 0
		else
			week_count += 1
		end
	end

	#### Next month
	week_count = 0
	cal_next_html = ''
	cal_next_html << "<tr><td width='20%'></td><td class='month'>午前</td><td class='month'>午後</td></tr>"


	dd_delta = calendar.ddl - calendar.dd
	0.upto( days_next.size - 1 ) do |c|
		week_c = 'weekday_mobi'
		week_c = 'sunday_mobi' if calendar_next_set[c].wd == 0
		week_c = 'saturday_mobi' if calendar_next_set[c].wd == 6
		if calendar_next_set[c].dd + dd_delta <= 28
			cal_next_html << "<tr>"
			cal_next_html << "<td class='#{week_c}' align='center'>#{days_next[c]} (#{weeks[calendar_next_set[c].wd]})</td>"
			if calendar_next_set[c].status_am == 9
				cal_next_html << "<td class='day_on' align='center'><a href='#{script}.cgi?command=select&yyyy=#{calendar_next_set[c].yyyy}&mm=#{calendar_next_set[c].mm}&dd=#{calendar_next_set[c].dd}&ampm=0'><div align='center' class='btn-outline-dark'>○</div></a></td>"

			elsif calendar_next_set[c].status_am == 0
				cal_next_html << "<td class='day_off_mobi text-success' align='center'>休</div>"
			else
				cal_next_html << "<td class='day_out text-danger' align='center'>×</td>"
			end

			if calendar_next_set[c].status_pm == 9
				cal_next_html << "<td class='day_on' align='center'><a href='#{script}.cgi?command=select&yyyy=#{calendar_next_set[c].yyyy}&mm=#{calendar_next_set[c].mm}&dd=#{calendar_next_set[c].dd}&ampm=1'><div align='center' class='btn-outline-dark'>○</div></a></td>"
			elsif calendar_next_set[c].status_pm == 0
				cal_next_html << "<td class='day_off_mobi text-success' align='center'>休</div>"
			else
				cal_next_html << "<td class='day_out text-danger' align='center'>×</td>"
			end
			cal_next_html << '</td>'
		end
		if week_count ==  6
			cal_next_html << '</tr>'
			week_count = 0
		else
			week_count += 1
		end
	end

	html = <<-"HTML"
	<h1 align="center" class='month'>嵯峨お料理教室 予約</h1>
	<div id='world_frame'>
	<div align="center">
		○…予約可能
		×…予約済み
		休…お休み
	</div>
	<div align="center">
		午前は9:30~10:00スタート、午後は17:00~17:30スタート。
	</div>
	<br>
	<div class='row'>
		<div  class='col-3'></div>
		<div  class='col-6'>
			<form action='#{script}.cgi?command=confirm' method='post'>
			<div class="input-group mb-3">
				<span class="input-group-text">メールアドレス</span>
				<input type="email" class="form-control" name='pass' required>
				<input type="submit" class="btn btn-outline-info" value='予約確認'>
			</div>
			</form>
		</div>
		<div  class='col-3'></div>
	</div>
	<h2 align="center" class='month'>#{calendar.yyyy}年 #{calendar.mm}月</h2>
	<table align='center' width='90%'>
	  #{cal_html}
	</table>
	<br>
	<h2 align="center" class='month'>#{calendar_next.yyyy}年　#{calendar_next.mm}月</h2>
	<table align='center' width='90%'>
	  #{cal_next_html}
	</table>
HTML
end

puts html

html_foot
