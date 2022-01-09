#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 print web page 0.14b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require './brain'
require 'rqrcode'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
fct_num = 14
frct_select = %w( 四捨五入 四捨五入 切り上げ 切り捨て )
accu_check = %w( 通常合計 精密合計 )
ew_check = %w( 単純g 予想g )


#==============================================================================
#DEFINITION
#==============================================================================

#### html_header for printv
def html_head_pv( recipe )
	code = recipe.code
	mcode = recipe.media
	recipe_name = recipe.name
	tw_image = ''
	tw_image = "<meta name='twitter:image' content='https://bacura.jp/nb/#{$PHOTO}/#{mcode[0]}-tn.jpg' />" if mcode.size > 0

	html = <<-"HTML"
<!DOCTYPE html>
<head>
 	<title>栄養ブラウザ レシピ：#{recipe_name}</title>
 	<meta charset="UTF-8">
 	<meta name="keywords" content="栄養,nutrition, Nutritionist, food,検索,計算,解析,評価">
 	<meta name="description" content="食品成分表の検索,栄養計算,栄養評価, analysis, calculation">
 	<meta name="robots" content="index,follow">
 	<meta name="author" content="Shinji Yoshiyama">

 	<!-- Twitter card -->
 	<meta name="twitter:card" content="summary" />
 	<meta name="twitter:site" content="@ho_meow" />
 	<meta name="twitter:title" content="ユビキタス総合栄養ツール：栄養ブラウザ" />
 	<meta name="twitter:description" content="公開レシピ紹介///#{recipe_name}" />
 	#{tw_image}
 	<meta name="twitter:image:alt" content="ばきゅら京都Labロゴ" />

 	<!-- bootstrap -->
 	<link rel="stylesheet" href="bootstrap-dist/css/bootstrap.min.css">
 	<link rel="stylesheet" href="#{$CSS_PATH}/core.css">

	<!-- Jquery -->
  	<script type="text/javascript" src="./jquery-3.6.0.min.js"></script>
	<!-- bootstrap -->
	<script type="text/javascript" src="bootstrap-dist/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="#{$JS_PATH}/core.js"></script>
	<script type='text/javascript' src='#{$JS_PATH}/recipe.js'></script>

	#{tracking}
</head>

<body class="body">
  <span class="world_frame" id="world_frame">
HTML

  puts html
end


#### QRコード生成
def makeQRcode( text, code )
	qrcode = RQRCode::QRCode.new( text, :level => :m )

	# With default options specified explicitly
	png = qrcode.as_png(
		resize_gte_to: false,
		resize_exactly_to: false,
		fill: 'white',
		color: 'black',
		size: 100,
		border_modules: 4,
		module_px_size: 6,
		file: nil # path to write
	)
	IO.write( "#{$PHOTO_PATH}/#{code}-qr.png", png.to_s )
end


#### 食材抽出
def extract_foods( recipe, dish, template, ew_mode )
	sum = recipe.sum
	dish_recipe = recipe.dish
	uname = recipe.user
	calc_weight = [ '単純換算g','予想摂取g' ]
	return_foods = "<table class='table table-sm'>\n"

	case template
	when 0
		return_foods << "<thead><tr><th class='align_c'>食材</th><th class='align_r'>数量</th><th class='align_r'>単位</th></tr></thead>\n"
	when 1
		return_foods << "<thead><tr><th class='align_c'>食材</th><th class='align_c'>備考</th><th class='align_r'>数量</th><th class='align_r'>単位</th></tr></thead>\n"
	when 2
		return_foods << "<thead><tr><th>食品番号</th><th class='align_c'>食材</th><th class='align_c'>備考</th><th class='align_r'>数量</th><th class='align_r'>単位</th><th class='align_r'>#{calc_weight[ew_mode]}</th></tr></thead>\n"
	when 3
		return_foods << "<thead><tr><th>食品番号</th><th class='align_c'>食材</th><th class='align_c'>備考</th><th class='align_r'>数量</th><th class='align_r'>単位</th><th class='align_r'>#{calc_weight[ew_mode]}</th><th class='align_r'>廃棄率%</th><th class='align_r'>発注量kg</th></tr></thead>\n"
	end

	db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
	a = sum.split( "\t" )

	a.each do |e|
		fn, fw, fu, fuv, fc, fi, frr, few = e.split( ':' )
		few = fw if few == nil

		if fn == '-'
			return_foods << "<tr><td></td></tr>\n"
		elsif fn == '+'
			return_foods << "<tr><td class='print_subtitle'>#{fi}</td></tr>\n"
		else
			# 人数分調整
			z, fuv = food_weight_check( fuv ) if /\// =~ fuv
			fuv = BigDecimal( fuv ) / dish_recipe * dish
			fuv_v = fuv.to_f
			fuv_v = fuv.to_i if fuv_v >= 10
			few = BigDecimal( few ) / dish_recipe * dish
			few_v = few.to_f
			few_v = few.to_i if few_v >= 10

			query = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{fn}';"
			res = db.query( query )

			case template
			when 0
  				class_add = ''
  				if /\+/ =~ res.first['class1']
    				class_add = "<span class='tagc'>#{res.first['class1'].sub( '+', '' )}</span> "
  				elsif /\+/ =~ res.first['class2']
    				class_add = "<span class='tagc'>#{res.first['class2'].sub( '+', '' )}</span> "
  				elsif /\+/ =~ res.first['class3']
    				class_add = "<span class='tagc'>#{res.first['class3'].sub( '+', '' )}</span> "
  				end
  				food_name = res.first['name']
				if /^\=/ =~ fi
					food_name = fi.sub( '=', '' )
					fi = ''
				end
				return_foods << "<tr><td>#{class_add}#{food_name}</td><td align='right'>#{fuv_v.ceil( 1 )}</td><td align='right'>#{fu}</td></tr>\n" if res.first
			when 1
				tags = bind_tags( res )
				if /^\=/ =~ fi
					tags = fi.sub( '=', '' )
					fi = ''
				end
				return_foods << "<tr><td>#{tags}</td><td>#{fi}</td><td align='right'>#{fuv_v.ceil( 1 )}</td><td align='right'>#{fu}</td></tr>\n" if res.first
			when 2
				tags = bind_tags( res )
				if /^\=/ =~ fi
					tags = fi.sub( '=', '' )
					fi = ''
				end
				return_foods << "<tr><td>#{fn}</td><td>#{tags}</td><td>#{fi}</td><td align='right'>#{fuv_v.ceil( 1 )}</td><td align='right'>#{fu}</td><td align='right'>#{few_v.ceil( 1 )}</td></tr>\n" if res.first
			when 3
				tags = bind_tags( res )
				fi.sub!( '=', '' )
				refuse = 0
				query = ''
				if /U|P/ =~ fn
					query = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{fn}' AND ( user='#{uname}' OR user='#{$GM}' );"
				else
					query = "SELECT REFUSE from #{$MYSQL_TB_FCT} WHERE FN='#{fn}';"
				end
				res = db.query( query )
				refuse = res.first['REFUSE'].to_i if res.first
				if fuv >= 10
					t = ( fuv / ( 100 - refuse ) / BigDecimal( 10 )).ceil( 2 ).to_f.to_s
				else
					t = ( fuv / ( 100 - refuse ) / BigDecimal( 10 )).ceil( 3 ).to_f.to_s
				end
				df = t.split( '.' )
				comp = ( 2 - df[1].size )
				comp.times do |c| df[1] = df[1] << '0' end
				ordering_weight = df[0] + '.' + df[1]
				return_foods << "<tr><td>#{fn}</td><td>#{tags}</td><td>#{fi}</td><td align='right'>#{fuv_v}</td><td align='right'>#{fu}</td><td align='right'>#{few_v}</td><td align='right'>#{res.first['REFUSE']}</td><td align='right'>#{ordering_weight}</td></tr>\n" if res.first
			end
		end
	end
	db.close
	return_foods << "</table>\n"

	return return_foods
end


#### プロトコール変換
def modify_protocol( protocol )
	return_protocol = "<ul>\n"
	a = protocol.split( "\n" )
	a.each do |e|
		if /^\@/ =~ e
			t = e.delete( '@' )
			return_protocol << "<span class='print_comment'>(#{t})</span><br>\n"
		elsif /^\!/ =~ e
			t = e.delete( '!' )
			return_protocol << "<span class='print_subtitle'>#{t}</span><br>\n"
		elsif /^\#/ =~ e
		elsif e == ''
			return_protocol << "<br>\n"
		else
			return_protocol << "<li>#{e}</li>\n"
		end
	end
	return_protocol << "</ul>\n"

	return return_protocol
end


#### 写真構成
def arrange_photo( recipe )
	code = recipe.code
	mcode = recipe.media
	main_photo = ''
	main_photo = "<img src='#{$PHOTO}/#{mcode[0]}.jpg' width='100%' height='100%' class='img-fluid rounded'>\n" if mcode.size > 0

	sub_photos = ''
	if mcode.size > 1
		1.upto( mcode.size - 1 ) do |c|
			sub_photos << "<img src='#{$PHOTO}/#{mcode[c]}-tn.jpg' width='25%' height='25%' class='img-fluid rounded'>\n"
		end
	end

	return main_photo, sub_photos
end


#==============================================================================
# Main
#==============================================================================

html_init( nil )

user = User.new( @cgi )

puts "Getting GET<br>" if @debug
get_data = get_data()
code = get_data['c']
template = get_data['t'].to_i
dish = get_data['d'].to_i
palette = get_data['p'].to_i
frct_accu = get_data['fa'].to_i
ew_mode = get_data['ew'].to_i
frct_mode = get_data['fm'].to_i
csc = get_data['cs'].to_s
url = "https://bacura.jp/nb/printv.cgi?c=#{code}&t=#{template}&d=#{dish}&p=#{palette}"
url << "&cs=#{csc}" unless csc == ''
if @debug
	puts "code: #{code}<br>"
	puts "template: #{template}<br>"
	puts "dish: #{dish}<br>"
	puts "url: #{url}<br>"
	puts "<hr>"
end


puts "Loading recipe<br>" if @debug
recipe = Recipe.new( user )
recipe.load_db( code, true )
dish = recipe.dish if dish = 0
recipe.load_media
photo_num = recipe.media.size


puts "html header<br>" if @debug
html_head_pv( recipe )


puts "extract foods<br>" if @debug
foods = extract_foods( recipe, dish, template, ew_mode )
puts "foods: #{foods}<br>" if @debug


puts 'Protocol html<br>' if @debug
protocol = modify_protocol( recipe.protocol )


puts 'Photo html<br>' if @debug
main_photo, sub_photos = arrange_photo( recipe )


puts 'Generating QR code<br>' if @debug
makeQRcode( url, code )


puts 'Mode select HTML<br>' if @debug
mode_list = %w( シンプル表示 標準表示 栄養表示 完全栄養表示 )
mode_selected = selected( 0, 3, template )
mode_html = '<div class="input-group input-group-sm">'
mode_html << '<span class="input-group-text">表示モード</span>'
mode_html << "<select class='form-select' name='t'>"
0.upto( 3 ) do |c| mode_html << "<option value='#{c}' #{mode_selected[c]}>#{mode_list[c]}</option>" end
mode_html << "</select>"
mode_html << '</div>'


puts 'Palette select HTML<br>' if @debug
palette_sets = []
palette_name = []
palette_html = ''
palette_start = 0
if template >= 2
	if user.name
		r = mdb( "SELECT * from #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}';", false, @debug )
		r.each do |e|
			a = e['palette'].split( '' )
			a.map! do |x| x.to_i end
			palette_sets << a
			palette_name << e['name']
		end
	else
		@palette_default.each do |e|
			a = e.split( '' )
			a.map! do |x| x.to_i end
			palette_sets << a
		end
		palette_name = @palette_default_name
		palette_start = 1
	end

	palette_selected = selected( 0, palette_name.size - 1, palette )
	palette_html = '<div class="input-group input-group-sm">'
	palette_html << '<span class="input-group-text">栄養パレット</span>'
	palette_html << "<select class='form-select' name='p'>"
	palette_start.upto( palette_name.size - 1  ) do |c| palette_html << "<option value='#{c}' #{palette_selected[c]}>#{palette_name[c]}</option>" end
	palette_html << "</select>"
	palette_html << '</div>'
end


puts 'Nimono alart select HTML<br>' if @debug
nimono_html = ''
if recipe.dish != dish
end


#### 食品番号から食品成分と名前を抽出
fct = []
fct_name = []
fct_sum = []

if template >= 2
	palette_set = palette_sets[palette]

	# 成分項目の抽出
	fct_item = []
	@fct_item.size.times do |c|
		fct_item << @fct_item[c] if palette_set[c] == 1
	end

	food_no, food_weight, total_weight = extract_sum( recipe.sum, recipe.dish, ew_mode )
	db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )

	# 食品成分データの抽出と名前の書き換え
	food_no.each do |e|
		fct_tmp = []
		if e == '-'
			fct << '-'
		elsif e == '+'
			fct << '+'
		elsif e == '00000'
			fct << '0'
		else
			if /P|U/ =~ e
				query = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{e}' AND ( user='#{uname}' OR user='#{$GM}' );"
			else
				query = "SELECT * from #{$MYSQL_TB_FCT} WHERE FN='#{e}';"
			end
			res = db.query( query )
			fct_name << res.first['Tagnames']
			@fct_item.size.times do |c|
				fct_tmp << res.first[@fct_item[c]] if palette_set[c] == 1
			end

			fct << Marshal.load( Marshal.dump( fct_tmp ))
		end
	end

	# 名前の書き換え
	if true
		food_no.size.times do |c|
			query = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}';"
			res = db.query( query )
			fct_name[c] = bind_tags( res ) if res.first
		end
	end
	db.close

	# データ計算
	fct_item.size.times do |c| fct_sum << BigDecimal( 0 ) end
	food_no.size.times do |fn|
		unless food_no[fn] == '-' || food_no[fn] == '+'
			fct_item.size.times do |fi|
				t = convert_zero( fct[fn][fi] )

				# 通常計算
				fct[fn][fi] = num_opt( t, food_weight[fn], frct_mode, @fct_frct[fct_item[fi]] )
				if frct_accu == 0
					# 通常計算
					fct_sum[fi] += BigDecimal( fct[fn][fi] )
				else
					# 精密計算
					fct_sum[fi] += BigDecimal( num_opt( t, food_weight[fn], frct_mode, @fct_frct[fct_item[fi]] + 3 ))
				end
			end
		end
	end

	# 合計値の桁合わせ
	fct_sum = adjust_digit( fct_item, fct_sum, frct_mode )
end

if template >= 2
	fct_html = ''
	table_num = fct_item.size / fct_num
	table_num += 1 if ( fct_item.size % fct_num ) != 0
	table_num.times do |c|
		fct_html << '<table class="table table-sm">'

		# 項目名
		fct_html << '<tr>'
		if template > 2
			fct_html << '<th align="center" width="6%" class="fct_item">食品番号</th>'
			fct_html << '<th align="center" width="20%" class="fct_item align_c">食品名</th>'
			fct_html << '<th align="center" width="4%" class="fct_item">重量</th>'
		end

		fct_num.times do |cc|
			fct_no = fct_item[( c * fct_num ) + cc]
			if @fct_name[fct_no]
				fct_html << "<th align='center' width='5%' class='fct_item'>#{@fct_name[fct_no]}</th>"
			else
				fct_html << "<th align='center' width='5%' class='fct_item'>&nbsp;</th>"
			end
		end
		fct_html << '</tr>'

		# 単位
		fct_html << '<tr>'
		if template > 2
			fct_html << '<td colspan="2" align="center"></td>'
			fct_html << "<td align='center' class='fct_unit'>( g )</td>"
		end
		fct_num.times do |cc|
			fct_no = fct_item[( c * fct_num ) + cc]
			if @fct_unit[fct_no]
				fct_html << "<td align='center' class='fct_unit'>( #{@fct_unit[fct_no]} )</td>"
			else
				fct_html << "<td align='center' class='fct_unit'>&nbsp;</td>"
			end
		end
		fct_html << '</tr>'

		if template > 2
		# 各成分値
			food_no.size.times do |cc|
				unless food_no[cc] == '-' || food_no[cc] == '+'
					fct_html << '    <tr>'
					fct_html << "      <td align='center'>#{food_no[cc]}</td>"
					fct_html << "      <td>#{fct_name[cc]}</td>"
					fct_html << "      <td align='right'>#{food_weight[cc].to_f}</td>"
					fct_num.times do |ccc|
						fct_no = ( c * fct_num ) + ccc
						fct_html << "      <td align='right'>#{fct[cc][fct_no]}</td>"
					end
					fct_html << '    </tr>'
				end
			end
		end

		# 合計値
		fct_html << '    <tr>'
		if template > 2
			fct_html << '      <td colspan="2" align="center" class="fct_sum">合計</td>'
			fct_html << "      <td align='right' class='fct_sum'>#{total_weight.to_f}</td>"
		end
		fct_num.times do |cc|
			fct_no = ( c * fct_num ) + cc
			fct_html << "      <td align='right' class='fct_sum'>#{fct_sum[fct_no]}</td>"
		end
		fct_html << '    </tr>'
		fct_html << '</table>'
		fct_html << "<div class='fct_item'>#{frct_select[frct_mode]} / #{accu_check[frct_accu]} / #{ew_check[ew_mode]}</div>\n"
	end
end


#### 共通ヘッダ
html_head = <<-"HTML"
<div class='container'>
	<div class='row'>
		<div class='col-8'><h4>#{recipe.name}</h4></div>
		<div class='col-4' align="right">Recipe code: #{code}</div>
	</div>
	<hr>
	<form action='' method='get'>
	<div class='row' align='center'>
		<div class='col'>
			<div class="input-group input-group-sm">
				<span for="dish_num" class="input-group-text">人数</span>
				<input type='number' name='d' size='3' min='1' value='#{dish}' class="form-control">
			</div>
		</div>
		<div class='col'>
				#{mode_html}
		</div>
		<div class='col'>
				#{palette_html}
		</div>
		<div class='col'>
				<input type='hidden' name='c' value='#{code}'>
				<input type='hidden' name='fa' value='#{frct_accu}'>
				<input type='hidden' name='ew' value='#{ew_mode}'>
				<input type='hidden' name='fm' value='#{frct_mode}'>
				<input type='submit' value='変更' class='btn btn-sm btn-outline-primary'>
		</div>
	</div>
	</form>
	<hr>
HTML


#### 共通フッタ
if csc == ''
	html_foot = <<-"HTML"
	<hr>
	<div class='row'>
		<div class='col-10'>
			栄養士・管理栄養士のための欲しい機能を無節操に同化するユビキタス総合栄養ツール<br><br>
			<a href='https://bacura.jp/nb/' class='h4 alert alert-danger'>栄養ブラウザ</a>
		</div>
		<div class='col-2'>
			レシピQRコード<br>
			<img src='#{$PHOTO}/#{code}-qr.png'>
		</div>
	</div>
</div>
HTML
else
	r = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLC} WHERE code='#{csc}';", false, @debug )
	print_ins = ''
	school_name = ''
	qr_ins = ''
	qr_img= ''
	if r.first
		print_ins = r.first['print_ins']
		school_name = r.first['name']
		if r.first['qr_ins'] != ''
			makeQRcode( r.first['qr_ins'], csc )
			qr_img = "<img src='#{$PHOTO}/#{csc}-qr.png'>"
		end
	end


	html_foot = <<-"HTML"
	<hr>
	<div class='row'>
		<div class='col-5'>
			<h5>#{school_name}</h5>
			#{print_ins}
		</div>
		<div class='col-2'>
			#{qr_img}
		</div>
		<div class='col-3'>
			<a href='https://nb.bacura.jp/'>栄養ブラウザ</a><br>
			レシピコード：<br>
			<a href='#{url}'>#{code}</a>
		</div>
		<div class='col-2'>
			<img src='#{$PHOTO}/#{code}-qr.png'>
		</div>
	</div>
</div>
HTML
end

case template
#### 基本レシピ・写真有
when 0
html = <<-"HTML"
	<div class='row'>
		<div class='col'>
			#{main_photo}
		</div>
		<div class='col'>
			<h5>材料</h5>
			#{foods}
		</div>
	</div>
	<hr>
	<div class='row'>
		<div class='col'>
			<h5>作り方</h5>
			#{protocol}
		</div>
	</div>
HTML


#### 詳細レシピ・写真有
when 1
html = <<-"HTML"
	<div class='row'>
		<div class='col-5'>
			#{main_photo}
		</div>
		<div class='col-7'>
			<h5>材料</h5>
			#{foods}
		</div>
		<div class='col'>
			<h5>作り方</h5>
			#{protocol}
		</div>
	</div>
HTML


#### 栄養レシピ・写真有
when 2, 3
html = <<-"HTML"
	<div class='row'>
		<div class='col-8'>
			<h5>材料</h5>
			#{foods}
		</div>
		<div class='col-4'>
			#{main_photo}
		</div>
	</div>
	<hr>
	<div class='row'>
		<div class='col'>
			<h5>作り方</h5>
			#{protocol}
		</div>
	</div>
	<h5>栄養成分</h5>
	#{fct_html}
HTML

end

puts html_head
puts html
puts html_foot
