#データの特徴
# TokeR module for overlook 0.00b
#encoding: utf-8

def table_check( table )
	r = mdbr( "SHOW TABLES LIKE '#{table}';", false, false )
	mdbr( "CREATE TABLE #{table} ( token VARCHAR(20) NOT NULL PRIMARY KEY, date DATETIME, data TEXT, num_ VARCHAR(32), sum_ VARCHAR(32), mean_ VARCHAR(32), min_ VARCHAR(32 ), max_ VARCHAR(32), median_ VARCHAR(32), var_ VARCHAR(32), sd_ VARCHAR(32));", false, false ) unless r.first
end


def toker_module( cgi, user, debug )
	mod = cgi['mod']
	command = cgi['command']
	token = cgi['token']
	test_group = cgi['test_group']
	html = ''

	module_js( mod )

	case command
	when 'form'
		token = "#{SecureRandom.hex( 2 )}#{SecureRandom.hex( 2 )}#{SecureRandom.hex( 2 )}#{SecureRandom.hex( 2 )}#{SecureRandom.hex( 2 )}"

html = <<-"HTML"

		<div class='row'>
			<div class='col-11'><h5>#{mod}</h5></div>
			<div class='col-1'><a href='pass-text.cgi?toker=#{mod}' target="source"><span class='badge bg-dark'>R source</span></a></div>
		</div>
		<div class='row'>
			集団の基礎統計値を算出します。
		</div>
		<br>
		<div class='row'>
			<div class='col'>
				<div class="form-group">
					<label for="test_group">データ形式：半角数字（区切りは改行、カンマ、空白）</label>
					<textarea class="form-control" id="test_group" rows="3"></textarea>
				</div>
			</div>
		</div>
		<br>
		<div class='row'>
			<div class='col-2'>
				<button class='btn btn-sm btn-primary' onclick="tokerSampleReady( '#{token}' )">サンプルデータ送信</button>
			</div>
		</div>
HTML
	when 'ready'
		html = "<div class='row'><h5>#{mod}: データ確認</h5></div>"

		if test_group == '' || test_group == nil
			html << "<div class='row'>"
			html << "送信データが空です。"
			html << "</div>"
		else
			test_group.gsub!( "\n", "\t" )
			test_group.gsub!( ',', "\t" )
			test_group.gsub!( ' ', "\t" )
			test_group.gsub!( /[^0-9\-\.\t]/, "" )
			a = test_group.split( "\t" ) - ['', nil]
			data_num = a.size
			clean_data = a.join( "\t" )

			begin
				mdbr( "INSERT INTO #{mod} SET token='#{token}', data='#{clean_data}';", false, false )

				html << "<div class='row'>"
				html << "<div class='col-2'>データ数</div><div class='col-10'>#{data_num}</div>"
				html << "</div>"
				html << "<div class='row'>"
				html << "<div class='col-2'>サンプル</div><div class='col-10'>#{clean_data[0..100]}</div>"
				html << "</div>"
				html << "<br>"
				html << "<button class='btn btn-sm btn-primary' onclick=\"tokerSampleAnalyize( '#{token}' )\">サンプルデータ解析</button>"

				html << "<div align='right'class='code'>#{token}</div>"
			rescue
				html << "<div class='row'>"
				html << "送信データのDBへの格納に失敗しました。"
				html << "</div>"
			end
		end

	when 'process'
		require "open3"

		html = "<div class='row'><h5>#{mod}: 解析結果</h5></div>"

		rsquery = "Rscript  #{$HTDOCS_PATH}/toker_/mod_#{mod}.R #{mod} #{token} #{$MYSQL_DBR} #{$MYSQL_USERR}"
		puts rsquery if debug
		stdo, stde = Open3.capture3( rsquery )
		puts "#{stdo}<br>" if debug
		puts "#{stde}<br>" if debug

		puts "Moving png image to photo path<br>" if debug
		png = Media.new( user )
		png.origin = token
		png.type = 'png'
		png.date = @datetime
		png.mcode = generate_code( user.name, 'p' )
		FileUtils.mv( "#{$TMP_PATH}/#{token}.png", "#{$PHOTO_PATH}/#{png.mcode}.png" )
		png.save_db

		puts "Moving pdf image to photo path<br>" if debug
		pdf = Media.new( user )
		pdf.origin = token
		pdf.type = 'pdf'
		pdf.date = @datetime
		pdf.mcode = generate_code( user.name, 'p' )
		FileUtils.mv( "#{$TMP_PATH}/#{token}.pdf", "#{$PHOTO_PATH}/#{pdf.mcode}.pdf" )
		pdf.save_db

		r = mdbr( "SELECT * FROM #{mod} WHERE token='#{token}';", false, false )
		if r.first
			if r.first['mean'] != 'NA'
				html << "<table class='table table-striped'>"
				html << "<tr><td>サンプル数</td><td>#{r.first['num_']}</td><td>説明なし</td></tr>"
				html << "<tr><td>合計値</td><td>#{r.first['sum_']}</td><td>説明なし。</td></tr>"
				html << "<tr><td>平均値</td><td>#{r.first['mean_']}</td><td>最も単純な算術平均値。データの重心。</td></tr>"
				html << "<tr><td>中央値</td><td>#{r.first['median_']}</td><td>データの中央に位置する代表値。極端な値が混ざるデータで有効。</td></tr>"
				html << "<tr><td>最小値</td><td>#{r.first['min_']}</td><td>説明なし。</td></tr>"
				html << "<tr><td>最大値</td><td>#{r.first['max_']}</td><td>説明なし。</td></tr>"
				html << "<tr><td>分散</td><td>#{r.first['var_']}</td><td>データのばらけ具合。各データと平均値の差を2乗して合算した値。</td></tr>"
				html << "<tr><td>標準偏差</td><td>#{r.first['sd_']}</td><td>分散を平方根。分散同様ばらけ具合を示すが、単位がデータと同じに戻っている。</td></tr>"
				html << "</table>"

				html << "<div class='row'>"
				html << "<div class='col-3'>"

				rr = mdb( "SELECT * FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' AND mcode='#{png.mcode}';", false, debug )
				if rr.first
					html << "<img src='#{$PHOTO}/#{rr.first['mcode']}.png' class='img-thumbnail'><br>"
				end

				rr = mdb( "SELECT * FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' AND mcode='#{pdf.mcode}';", false, debug )
				if rr.first
					html << "<div align='right'><a href='#{$PHOTO}/#{pdf.mcode}.pdf' target='pdf'><img src='bootstrap-dist/icons/file-earmark-pdf.svg' style='height:1.5em; width:1.5em;'>PDF</a></div>"
				end

				html << "</div>"
				html << "</div>"
			else
				html << "<div class='row'>"
				html << "Rでの処理中にエラーが発生しました。"
				html << "</div>"
				html << "<div class='row'>"
				html << "#{stde}"
				html << "</div>"
			end
		else
			html << "<div class='row'>"
			html << "結果が存在しません。"
			html << "</div>"
		end

		html << "<div align='right'class='code'>#{token}</div>"
	end

	return html
end


def module_js( mod )
	js = <<-"JS"
<script type='text/javascript'>

var tokerSampleReady = function( token ){
	var test_group = document.getElementById( "test_group" ).value;
	$.post( "toker.cgi", { mod:'#{mod}', command:'ready', token:token, test_group:test_group }, function( data ){ $( "#L1" ).html( data );});

	flashBW();
	dline = true;
	dl1 = true;
	displayBW();
};

var tokerSampleAnalyize = function( token ){
	$.post( "toker.cgi", { mod:'#{mod}', command:'process', token:token }, function( data ){ $( "#L2" ).html( data );});

	dl2 = true;
	displayBW();
};

</script>
JS
	puts js
end
