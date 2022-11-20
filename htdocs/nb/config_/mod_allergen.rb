# Nutorition browser 2020 Config module for Allergen 0.00b
#encoding: utf-8

#### mod debug mode
@degug = true


def config_module( cgi, user, lp )
	l = module_lp( user.language )
	module_js()

	step = cgi['step']
	code = cgi['code']
	code.gsub!( /\s/, ',' ) unless code == ''
	code.gsub!( '　', ',' ) unless code == ''
	code.gsub!( '、', ',' ) unless code == ''
	fn = code.split( ',' )

	html = ''
	case step
	when 'on'
		fn.each do |e|
			if /P|U?\d\d\d\d\d/ =~ e
				mdb( "INSERT INTO #{$MYSQL_TB_PAG} SET user='#{user.name}', FN='#{e}';", false, @debug )
				r = mdb( "SELECT allergen FROM #{$MYSQL_TB_EXT} WHERE FN='#{e}' AND allergen>0;", false, @debug )
				mdb( "UPDATE #{$MYSQL_TB_EXT} SET allergen='3' WHERE FN='#{e}';", false, @debug ) unless r.first
			end
		end
	when 'off'
		fn.each do |e|
			if /P|U?\d\d\d\d\d/ =~ e
				mdb( "DELETE FROM #{$MYSQL_TB_PAG} WHERE user='#{user.name}' AND FN='#{e}';", false, @debug )
				r = mdb( "SELECT allergen FROM #{$MYSQL_TB_EXT} WHERE FN='#{e}' AND allergen=1 OR allergen=2;", false, @debug )
				mdb( "UPDATE #{$MYSQL_TB_EXT} SET allergen='0' WHERE FN='#{e}';", false, @debug ) unless r.first
			end
		end
	end

	list_html = ''
	r = mdb( "SELECT t1.* FROM #{$MYSQL_TB_TAG} AS t1 INNER JOIN #{$MYSQL_TB_PAG} AS t2 ON t1.FN = t2.FN WHERE t2.user='#{user.name}' ORDER BY t1.FN;", false, @debug )
	r.each do |e|
		list_html << "<tr>"
		list_html << "<td>#{e['FN']}</td>"
		list_html << "<td>#{e['name']} #{e['tag1']} #{e['tag2']} #{e['tag3']} #{e['tag4']} #{e['tag5']}</td>"
		list_html << "<td><span onclick=\"allergen_cfg( 'off', '#{e['FN']}' )\">#{l['trash']}</span></td>"
		list_html << '</tr>'
	end
	list_html << '<tr><td>no item listed.</td></tr>' if list_html == ''

	####
####
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{l['allergen']}</h5></div>
	</div>
	<div class='row'>
		<div class='col-12'>
			<div class="input-group input-group-sm">
				<label class="input-group-text">#{l['fn']}</label>
				<input type="text" class="form-control" id="code" value="">
			</div>
		</div>
	</div>
	<br>

	<div class='row'>
		<button class="btn btn-sm btn-info" type="button" onclick="allergen_cfg( 'on', '' )">#{l['regist']}</button>
	</div>
	<br>

	<table class='table table-sm table-striped'>
		<thead>
			<td>#{l['fn']}</td>
			<td>#{l['name']}</td>
			<td></td>
		</thead>

		#{list_html}
	</table>
HTML
####
	####

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>
var allergen_cfg = function( step, code ){
	if( step == 'on' ){
		var code = document.getElementById( 'code' ).value;
		$.post( "config.cgi", { mod:'allergen', step:step, code:code }, function( data ){
			$( "#L1" ).html( data );
			displayVIDEO( code + ':allergen ON' );
		});
	}

	if( step == 'off' ){
		$.post( "config.cgi", { mod:'allergen', step:step, code:code }, function( data ){
			$( "#L1" ).html( data );
			displayVIDEO( code + ':allergen OFF' );
		});
	}

	flashBW();
	dl1 = true;
	dline = true;
	displayBW();
};

</script>
JS
	puts js
end


def module_lp( language )
	l = Hash.new
	l['jp'] = {
		'fn' => "食品番号",\
		'name' => "食品名",\
		'allergen' => "アレルゲン登録（ユーザー）",\
		'regist' => "登　録",\
		'trash' 	=> "<img src='bootstrap-dist/icons/trash.svg' style='height:1.2em; width:1.2em;'>"
	}

	return l[language]
end
