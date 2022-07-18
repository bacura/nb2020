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
@debug = false
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
		food.gsub!( /\(/, '' )
		food.gsub!( /\)/, '' )
		puts food if @debug

		if food.size < 1
			puts "<br>" if @debug
			next 
		end
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
		end

		puts 'kakko~' if @debug
		a = e.scan( /\((.+)\)/ )
		if a.size > 0 && memo == ''
			memo = a.first.first
			food.gsub!( /\(.+\)/, '' )
		end

		puts 'Dic~' if @debug
		dic_hit = 0
		if memo == '' && food.size >= 1
			predict_food = ''
			r = mdb( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE alias='#{food}';", false, @debug )
			dic_hit = r.size
			if r.first
				if r.first['def_fn'] != ''
					predict_food = r.first['org_name']
					food_no = r.first['def_fn']
				else
					food_no = '+'
				end
			else
				food_sub_max = 0
				mecab = Natto::MeCab.new
				mecab.parse( food ) do |n|
					a = n.feature.force_encoding( 'utf-8' ).split( ',' )
		 			if a[0] == '名詞' && ( a[1] == '一般' || a[1] == '固有名詞' || a[1] == '普通名詞'  || a[1] == '人名' )
						if n.surface.size > food_sub_max
							rr = mdb( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE alias='#{n.surface}';", false, @debug )
							if rr.first
								dic_hit = rr.size
								predict_food = rr.first['org_name']
								food_no = rr.first['def_fn']
								food_sub_max = n.surface.size
							end
						end
					end
				end

				food_no = '+' if predict_food == ''
			end
		end

		puts 'Unit~' if @debug
		if food_no == '+' || food_no == '' || food_no == nil
			food_no = '+'
			predict_food = '-'
			unit = '-'
			dic_hit = '-'
			vol = '-'
			weight = '-'
			memo = e.gsub( '#', '' ).gsub( '[', '' ).gsub( ']', '' )
		elsif vol == 0
			memo = unit
			unit = 'g'
			weight = 0
		else
			r = mdb( "SELECT unit from #{$MYSQL_TB_EXT} WHERE FN='#{food_no}';", false, @debug )
			if r.first
				unith = JSON.parse( r.first['unit'] )
				if unith[unit] != nil
					weight = ( vol.to_f * unith[unit].to_f ).round( 2 )
				elsif unith["#{unit}M"] != nil
					unit = "#{unit}M"
					weight = ( vol.to_f * unith["#{unit}M"].to_f ).round( 2 )
				elsif unith["#{unit}S"] != nil
					unit = "#{unit}S"
					weight = ( vol.to_f * unith["#{unit}S"].to_f ).round( 2 )
				elsif unith["#{unit}L"] != nil
					unit = "#{unit}L"
					weight = ( vol.to_f * unith["#{unit}L"].to_f ).round( 2 )
				else
					memo = "#{vol}#{unit}"
					unit = 'g'
					vol = 0
					weight = 0
				end
			else
				memo = "#{vol}#{unit}"
				vol = 0
				unit = 'g'
				weight = vol
			end
		end

		lucky_sum = "#{food_no}:#{weight}:#{unit}:#{vol}:0:#{memo}:1.0:#{weight}"

		puts 'Check~<br>' if @debug
		checked = ''
		disabled = 'DISABLED'
		if food_no != '' && food_no != nil
			checked = 'CHECKED'
			disabled = ''
		end
		html << '<tr>'
      	html << "<td>#{food}[#{dic_hit}]</td>"
      	html << "<td>#{food_no}</td>"
      	html << "<td>#{predict_food}</td>"
      	html << "<td>#{memo}</td>"
      	html << "<td>#{vol}</td>"
      	html << "<td>#{unit}</td>"
      	html << "<td><input type='checkbox' id='lucky#{id_counter}' #{checked} #{disabled}></td>"
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
	puts "lucky_solid:#{lucky_solid}<br>"
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
			<textarea class="form-control" rows="10" aria-label="lucky_data" id="lucky_data"></textarea>
		</div>
		<div class='col-2'>
			<button type='button' class='btn btn-warning' onclick="luckyAnalyze()">#{lp[2]}</button>
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

		lucky_data.gsub!( "\s", "\t")
		lucky_data.gsub!( "　", "\t")
		lucky_data.gsub!( ",", "\t")
		lucky_data.gsub!( /\t+/, "\t")
		lucky_data.gsub!( '．', '.')
		lucky_data.gsub!( '（', '(')
		lucky_data.gsub!( '）', ')')
		lucky_data.gsub!( '[', '')
		lucky_data.gsub!( ']', '')
		lucky_data.gsub!( '#', '')
		lucky_data.gsub!( '…', '')

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
		lucky_data.gsub!( '束', "\t[束]" )
		lucky_data.gsub!( '缶', "\t[缶]" )

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

		# ()付き数字のマーク
		lucky_data = lucky_data.gsub( /(\(\d+g\))/ ) do |x|
			x = ""
		end

		# 数字のマーク
		lucky_data = lucky_data.gsub( /(\d+\/?\.?\d*)/ ) do |x|
			x = "##{$1}#"
		end

	end

	html = predict_html( lucky_data )

when 'push'
	new_sum = ''
	lucky_solid.sub!( /^\t/, '' )

	# まな板データの読み込み
	r = mdb( "SELECT sum from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	new_sum << r.first['sum'] if r.first
	new_sum << "\t" if new_sum != ''
	new_sum << lucky_solid if lucky_solid != ''

	# まな板データ更新
	mdb( "UPDATE #{$MYSQL_TB_SUM} SET sum='#{new_sum}' WHERE user='#{user.name}';", false, @debug )
end

puts html
