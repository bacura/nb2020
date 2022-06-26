#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser Lucky sum input driver 0.01b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require 'natto'


#==============================================================================
#STATIC
#==============================================================================
@debug = true
script = 'lucky'


#==============================================================================
#DEFINITION
#==============================================================================
def predict_html( lucky_data )
	html = ''

	# 仕上げ
	lucky_data.gsub!( /\n+/, "\n" )
	lucky_data.gsub!( /\t+/, '' )


	html = '<table class="table table-sm">'
	html << '<thead><tr>'
  	html << '<th scope="col">検出</th>'
  	html << '<th scope="col">食品番号</th>'
  	html << '<th scope="col">食品</th>'
  	html << '<th scope="col">メモ</th>'
  	html << '<th scope="col">量</th>'
  	html << '<th scope="col">単位</th>'
  	html << '<th scope="col">採用</th>'
  	html << '</tr></thead>'
	id_counter = 0
	lucky_solid = lucky_data.split( "\n" )
	lucky_solid.each do |e|
		food_no = ''
		weight = 100
		memo = ''
		vol = ''
		unit = ''
		food = e.split( '#' ).first
      	id_counter += 1

		puts 'vol~' if @debug
		a = e.scan( /\#(.+)\#/ )
		if a.size > 0
			vol = a.first.first
			aa = e.scan( /\[(.+)\]/ )
			if aa.size > 0
				unit = aa.first.first
			else
				unit = 'g'
			end
		else
			food_no = '+'
			food = ''
			memo = e
		end

		puts 'kakko~' if @debug
		a = e.scan( /\((.+)\)/ )
		if a.size > 0 && memo == ''
			memo = a.first.first
			food.sub!( /\(.+\)/, '' )
		end

		puts 'Dic~' if @debug
		dic_hit = 0
		if memo == ''
			predict_food = ''
			r = mdb( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE alias='#{food}';", false, @debug )
			dic_hit = r.size
			if r.first
				if r.first['def_fn'] != ''
					predict_food = r.first['org_name']
					food_no = r.first['def_fn']
				else
					food_no = '+'
					food = ''
					vol = ''
					unit = ''
					memo = e
				end
			else
				food_sub_max = 0
				mecab.parse( food ) do |n|
					food_sub = n.feature.force_encoding( 'utf-8' ).split( ',' )
					if foos_sub.size > foos_sub_max
						rr = mdb( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE alias='#{food_sub}';", false, @debug )
						if rr.first
							predict_food = rr.first['org_name']
							food_no = rr.first['def_fn']
							food_sub_max = food_sub.size
						end
					end
				end

				if food_sub_max == 0
					food_no = '+'
					food = ''
					vol = ''
					unit = ''
					memo = e
				end
			end
		end

		puts 'Unit~' if @debug
		if vol == '0' || food_no == '+'
			memo = unit
			unit = 'g'
		else
			r = mdb( "SELECT unit from #{$MYSQL_TB_EXT} WHERE FN='#{food_no}';", false, @debug )
			if r.first
				unith = JSON.parse( r.first['unit'] )
				p unith[unit]





			else
				unit = 'g'
				weight = vol
			end
		end


		lucky_sum = "#{food_no}:#{weight}:#{unit}:#{vol}:0:#{memo}:1.0:#{weight}"

		puts 'Check~' if @debug
		checked = ''
		checked = 'CHECKED' unless food_no == ''
		html << '<tr>'
      	html << "<td>#{food}[#{dic_hit}]</td>"
      	html << "<td>#{food_no}</td>"
      	html << "<td>#{predict_food}</td>"
      	html << "<td>#{memo}</td>"
      	html << "<td>#{vol}</td>"
      	html << "<td>#{unit}</td>"
      	html << "<td><input type='checkbox' id='lucky#{id_counter}' CHECKED></td>"
      	html << "</tr>"
      	html << "<input type='hidden' id='lucky_sum#{id_counter}' value='#{lucky_sum}'></td>"

	end

	html << '</table><br>'

	html << '<div class="row" align="right">'
	html << "<button class='btn btn-sm btn-success' onclick=\"luckyPush( '#{id_counter}' )\" >追加</button>"
	html << '</div>'

	return html
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


puts "POST<br>" if @debug
command = @cgi['command']
lucky_data = @cgi['lucky_data']
lucky_solid = @cgi['lucky_solid']
if @debug
	puts "command:#{command}<br>"
	puts "lucky_data:#{lucky_data}<br>"
	puts "<hr>"
end


####
html = ''
case command
when 'form'
	html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-10'>
			<textarea class="form-control" aria-label="lucky_data" id="lucky_data"></textarea>
		</div>
		<div class='col-2'>
			<button type='button' class='btn btn-warning' onclick=\"luckyAnalyze()\">#{lp[2]}</button>
		</div>
	</div>
</div>
HTML

# 解析
when 'analyze'
	candidate = nil

	# 特異データ検出
	# 栄養くん
	candidate = 'eiyo_kun' if /\[5A食品コード\]/ =~ lucky_data
	puts "candidate:#{candidate}<br>" if @debug

	case candidate
	when 'eiyo_kun'
		require "#{$HTDOCS_PATH}/lucky_/eiyo_kun.rb"
		html = ''
	else
		# 表記ゆれの統一
		lucky_data.tr!( '０-９ａ-ｚＡ-Ｚ','0-9a-zA-Z' )
		lucky_data.downcase!
		lucky_data.gsub!( "\r\n", "\n")
		lucky_data.gsub!( "\r", "\n")
		lucky_data.gsub!( /\n+/, "\n")
		lucky_data.gsub!( " ", "\t")
		lucky_data.gsub!( "　", "\t")
		lucky_data.gsub!( ",", "\t")
		lucky_data.gsub!( /\t+/, "\t")
		lucky_data.gsub!( '．', '.')
		lucky_data.gsub!( '（', '(')
		lucky_data.gsub!( '）', ')')
		lucky_data.gsub!( '[', '')
		lucky_data.gsub!( ']', '')
		lucky_data.gsub!( '#', '')

		# 単位の検出とマーク
		lucky_data.gsub!( /g/, "\t[g]" )
		lucky_data.gsub!( /ｇ/, "\t[g]" )
		lucky_data.gsub!( 'グラム', "\t[g]" )
		lucky_data.gsub!( /cup/, "\t[カップ]" )
		lucky_data.gsub!( 'カップ', "\t[カップ]" )
		lucky_data.gsub!( /ml/, "\t[ml]" )
		lucky_data.gsub!( 'cc', "\t[cc]" )
		lucky_data.gsub!( 'dl', "\t[dl]" )
		lucky_data.gsub!( 'cm', "\t[cm]" )
		lucky_data.gsub!( '大さじ', "\t[大さじ]" )
		lucky_data.gsub!( 'おおさじ', "\t[大さじ]" )
		lucky_data.gsub!( '小さじ', "\t[小さじ]" )
		lucky_data.gsub!( 'こさじ', "\t[小さじ]" )

		lucky_data.gsub!( '本', "\t[本]" )
		lucky_data.gsub!( '枚', "\t[枚]" )
		lucky_data.gsub!( '個', "\t[個]" )
		lucky_data.gsub!( '玉', "\t[玉]" )
		lucky_data.gsub!( '株', "\t[株]" )
		lucky_data.gsub!( '匹', "\t[匹]" )
		lucky_data.gsub!( '切れ', "\t[切れ]" )
		lucky_data.gsub!( '片', "\t[片]" )

		lucky_data.gsub!( 'ひとつまみ', "\t1\t[つまみ]" )
		lucky_data.gsub!( 'ふたつまみ', "\t2\t[つまみ]" )
		lucky_data.gsub!( '半分', "\t0.5\t[個]" )

		lucky_data.gsub!( '適量', "\t0\t[適量]" )
		lucky_data.gsub!( '適当', "\t0\t[適当]" )
		lucky_data.gsub!( '少々', "\t0\t[少々]" )
		lucky_data.gsub!( 'お好み', "\t0\t[お好み]" )
		lucky_data.gsub!( '好み', "\t0\t[お好み]" )


		# 分数の処理
		lucky_data = lucky_data.gsub( /(\d+)\/(\d+)/ ) do |x|
			x = ( $1.to_f / $2.to_f ).round( 2 ).to_s
		end

		# 数値→単位の順番に並べ替える
		lucky_data = lucky_data.gsub( /(\[[^\[]+\])\t?(\d+\.?\d*)/ ) do |x|
			x = "#{$2}\t#{$1}"
		end

		# 単位の後で改行
		lucky_data = lucky_data.gsub( /(\[[^\[]+\])/ ) do |x|
			x = "#{$1}\n"
		end

		# 数字のマーク
		lucky_data = lucky_data.gsub( /(\d+\/?\.?\d*)/ ) do |x|
			x = "##{$1}#"
		end
	end

	html = predict_html( lucky_data )

when 'push'
	new_sum = "+:-:-:-:0:UNLUCKY!:-:-\t"

	if mode == 'add'
		# まな板データの読み込み
		q = "SELECT sum from #{$MYSQL_TB_SUM} WHERE user='#{uname}';"
		err = 'sum select'
#		r = db_process( q, err, false )
		new_sum << "#{r.first['sum']}\t" if r.first
	end

	lucky_solid.each do |e|
		# dummy
	end
	new_sum.chop!

	# まな板データ更新
	q = "UPDATE #{$MYSQL_TB_SUM} SET sum='#{new_sum}' WHERE user='#{uname}';"
	err = 'sum update'
#	db_process( q, err, false )
end

puts html
