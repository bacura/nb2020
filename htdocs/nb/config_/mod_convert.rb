# Nutorition browser 2020 Config module for food number converter 0.00b
#encoding: utf-8

def config_module( cgi, user, lp )
	lp = module_lp( user.language )
	module_js()
	from_fn = cgi['from_fn'].to_s
	into_fn = cgi['into_fn'].to_s
	ignore_p = cgi['ignore_p']

	html = ''
	case cgi['step']
	when 'confirm'
		r = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{into_fn}';", false, false )
		if r.first
			rr = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{from_fn}';", false, false )
			if rr.first
				count = 0
				protect = ''
				protect = ' AND protect!="1"' if ignore_p == 'off'
				rrr = mdb( "SELECT sum FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}'#{protect};", false, false )
				rrr.each do |e|
					hit_flag = false
					a = e['sum'].split( "\t" )
					a.each do |ee|
						sum = ee.split( ':' )
						hit_flag = true if from_fn == sum[0]
					end
					count += 1 if hit_flag
				end
				convert_button = ''
				convert_button = "<div class='col-3' align='right'><button type='button' class='btn btn-outline-warning btn-sm nav_button' onclick=\"convert_cfg2( 'exchange', '#{from_fn}', '#{into_fn}', '#{ignore_p}' )\">#{lp[8]}</button></div>" if count > 0
				ignore_html = lp[7]
				ignore_html = lp[6] if ignore_p == 'on'

    			html << '<div class="container">'
    			html << '<div class="row">'
				html << "<div class='col-2'>#{rr.first['name']}</div>"
				html << "<div class='col-1' align='center'>#{lp[2]}</div>"
				html << "<div class='col-2'>#{r.first['name']}</div>"
				html << "<div class='col-2'>#{ignore_html}</div>"
				html << "<div class='col-2'>#{count} #{lp[9]}</div>"
				html << convert_button
				html << '</div>'
			else
				html << "#{lp[6]}"
			end
		else
			html << "#{lp[5]}"
		end

	when 'exchange'
		count = 0
		protect = ''
		protect = ' AND protect!="1"' if ignore_p == 'off'
		r = mdb( "SELECT sum, code, user FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}'#{protect};", false, false )
		r.each do |e|
			sums = []
			a = e['sum'].split( "\t" )
			a.each do |ee|
				sums << ee.sub( /^#{from_fn}/, into_fn )
			end
			sum_post = sums.join( "\t" )

			if e['sum'] != sum_post
				mdb( "UPDATE #{$MYSQL_TB_RECIPE} set sum='#{sum_post}' WHERE user='#{user.name}' AND code='#{e['code']}';", false, false )
				count += 1
			end
		end

    	html << '<div class="container">'
    	html << '<div class="row">'
		html << "<div class='col-2'>#{count} #{lp[10]}</div>"
		html << '</div>'
		html << '</div>'
	else
		html = <<-"HTML"
    <div class="container">
    	<div class='row'>
	    	<div class='col-2'><input type="text" id="from_fn" class="form-control form-control-sm" placeholder='#{lp[1]}'></div>
	    	<div class='col-1' align="center">#{lp[2]}</div>
			<div class='col-2'><input type="text" id="into_fn" class="form-control form-control-sm" placeholder='#{lp[3]}'></div>
	    	<div class='col-2'><div class="form-check">
				<input class="form-check-input" type="checkbox" value="on" id="ignore_p">
				<label class="form-check-label">#{lp[6]}</label>
			</div></div>
 			<div class='col-5' align="right"><button type="button" class="btn btn-outline-primary btn-sm nav_button" onclick="convert_cfg( 'confirm' )">#{lp[4]}</button></div>
		</div>
	</div>
HTML
	end

	####

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// Food number converter init
var convert_cfg = function( step ){
	var from_fn = document.getElementById( "from_fn" ).value;
	var into_fn = document.getElementById( "into_fn" ).value;
	if( document.getElementById( "ignore_p" ).checked ){var ignore_p = 'on'; }else{ var ignore_p = 'off'; }
	if( from_fn != '' && into_fn != '' ){
		if( into_fn != from_fn ){
			$.post( "config.cgi", { mod:'convert', step:step, from_fn:from_fn, into_fn:into_fn, ignore_p:ignore_p }, function( data ){ $( "#L2" ).html( data );});
			flashBW();
			dl1 = true;
			dl2 = true;
			dline = true;
			displayBW();
		}else{
			displayVIDEO( 'Same!(>_<)');
		}
	}else{
		displayVIDEO( 'Empty!(>_<)');
	}
};

// Food number converter exchange
var convert_cfg2 = function( step, from_fn, into_fn, ignore_p ){
	$.post( "config.cgi", { mod:'convert', step:step, from_fn:from_fn, into_fn:into_fn, ignore_p:ignore_p }, function( data ){ $( "#L2" ).html( data );});
};

</script>
JS
	puts js
end


def module_lp( language )
	mlp = Hash.new
	mlp['jp'] = []
	mlp['jp'][1] = "元食品番号"
	mlp['jp'][2] = "→"
	mlp['jp'][3] = "先食品番号"
	mlp['jp'][4] = "確認"
	mlp['jp'][5] = "変換先の食品番号は存在しません。"
	mlp['jp'][6] = "保護レシピを含める"
	mlp['jp'][7] = "保護レシピを除外する"
	mlp['jp'][8] = "変換"
	mlp['jp'][9] = "レシピが該当します"
	mlp['jp'][10] = "レシピを変換しました"

	return mlp[language]
end