# TokeR module for test 0.00b
#encoding: utf-8

def toker_module( cgi, user )

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
		<div class='row'><h5>統計(R) #{mod} フォーム</h5></div>
		<br>

		<div class='row'>
			<div class='col-2'>
				<button class='btn btn-sm btn-primary' onclick="tokerTESTready( '#{token}' )">データ送信</button>
			</div>
		</div>
		<br>

		<div class='row'>
			<div class='col'>
				<div class="form-group">
					<label for="test_group">データ形式：半角数字（区切りは改行、カンマ、空白）</label>
					<textarea class="form-control" id="test_group" rows="10"></textarea>
				</div>
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
				html << "<button class='btn btn-sm btn-primary' onclick=\"tokerTESTprocess( '#{token}' )\">データ処理</button>"

				html << "<div align='right'class='code'>#{token}</div>"
			rescue
				html << "<div class='row'>"
				html << "送信データの格納に失敗しました。"
				html << "</div>"
			end
		end

	when 'process'
		require "open3"

		html = "<div class='row'><h5>#{mod}: 処理結果</h5></div>"
		stdo, stde = Open3.capture3( "Rscript  #{$HTDOCS_PATH}/toker_/mod_#{mod}.R #{token}" )

		r = mdbr( "SELECT result FROM #{mod} WHERE token='#{token}';", false, false )
		if r.first
			if r.first['result'] != 'NA'
				html << "<div class='row'>"
				html << "<div class='col-2'>平均</div><div class='col-10'>#{r.first['result']}</div>"
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

var tokerTESTready = function( token ){
	var test_group = document.getElementById( "test_group" ).value;
	$.post( "toker.cgi", { mod:'#{mod}', command:'ready', token:token, test_group:test_group }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'none';
};

var tokerTESTprocess = function( token ){
	$.post( "toker.cgi", { mod:'#{mod}', command:'process', token:token }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
};

</script>
JS
	puts js
end
