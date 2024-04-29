# Nutorition browser 2020 Config module for koyomiex 0.23b (2023/07/13)
#encoding: utf-8

@debug = false
@kex_max = 10

def config_module( cgi, db )
	module_js()
	l = module_lp( db.user.language )

	koyomi = Hash.new
	start = Time.new.year
	kexu = Hash.new
	kexa = Hash.new

	html = []

	step = cgi['step']
	kex_key = cgi['kex_key']
	kex_add_key = cgi['kex_add_key']
	kex_add_unit = cgi['kex_add_unit']
	kex_add_select = cgi['kex_add_select']
	if @debug
		puts "step: #{step}<br>"
	end


	puts 'LOAD config<br>' if @debug
	r = db.query( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{db.user.name}';", false )
	if r.first
		if r.first['koyomi'] != nil && r.first['koyomi'] != ''
			koyomi = JSON.parse( r.first['koyomi'] )
			start = koyomi['start'].to_i unless koyomi['start'] == nil
			kexu = koyomi['kexu'] unless koyomi['kexu'] == nil
			kexa = koyomi['kexa'] unless koyomi['kexa'] == nil
		end
	end


	case step
	when 'kstart'
		start = cgi['kstart'].to_i
		puts "start: #{start}<br>" if @debug

	when 'new'
		kexu[kex_add_key] = kex_add_unit
		kexa[kex_add_key] = "1"

	when 'select'
		kexu[kex_add_select] = @kex_std[kex_add_select]
		kexa[kex_add_select] = "1"

	when 'delete'
		kexu.delete( kex_key )
		kexa.delete( kex_key )

	when 'available'
		kex_onoff = cgi['kex_onoff']
		kexa[kex_key] = kex_onoff

	end


	puts 'UPDATE config<br>' if @debug
	if step != ''
		koyomi['start'] = start
		koyomi['kexu'] = kexu
		koyomi['kexa'] = kexa
		koyomi_ = JSON.generate( koyomi )
		db.query( "UPDATE #{$MYSQL_TB_CFG} SET koyomi='#{koyomi_}' WHERE user='#{db.user.name}';", true )
	end


	puts 'HTML start year option<br>' if @debug
	start_select = "<select class='form-select' id='kstart' onchange=\"ksChange()\">"
	2000.upto( 2050 ) do |c|
		selected = ''
		selected = 'SELECTED' if c == start
		start_select << "<option value='#{c}' #{selected}>#{c}</option>"
	end
  	start_select << "</select>"


	####
####
puts 'HTML10<br>' if @debug
html[10] = <<-"HTML10"
<div class="container">
	<div class='row'>
		<div class='col-4'>
			<div class='input-group input-group-sm'>
				<span class='input-group-text'>#{l['start']}</span>
				#{start_select}
			</div>
		</div>
	</div>
	<hr>

	<h5>#{l['menu_title']}</h5>
	<br>
HTML10
####
	####


	puts 'HTML20<br>' if @debug
	ht = ''
	kexu.each do |k, v|
		checked = ''
		checked = 'CHECKED' if kexa[k] == '1'

		ht << "<div class='row'>"
		ht << "	<div class='col-1'>"
		ht << "		<div class='form-check form-switch'>"
		ht << "			<input class='form-check-input' type='checkbox' id='kex_onoff#{k}' #{checked} onchange=\"kexOnOff( '#{k}' )\">"
		ht << "		</div>"
		ht << "	</div>"
		ht << "	<div class='col-4'>"
		ht << "		<div class='input-group input-group-sm'>"
    	ht << "			<label class='input-group-text'>#{l['item']}</label>"
		ht << "			<input type='text' maxlength='32' class='form-control form-control-sm' value='#{k}' DISABLED>"
		ht << "		</div>"
		ht << "	</div>"
		ht << "	<div class='col-2'>"
		ht << "		<div class='input-group input-group-sm'>"
		ht << "			<span class='input-group-text'>#{l['unit']}</span>"
		ht << "			<input type='text' maxlength='32' id='' class='form-control form-control-sm' value='#{v}' DISABLED>"
		ht << "		</div>"
		ht << "	</div>"
		ht << "	<div class='col-1'></div>"
		ht << "	<div class='col-2'><input type='checkbox' id='kex_del#{k}'>&nbsp;<span onclick=\"kexDel( '#{k}' )\">#{l['init']}</span></div>"
		ht << "</div><br>"
	end
	html[20] = ht

	if kexu.size <= @kex_max
		option = ''
		@kex_std.each do |k, v|
			option << "<option value='#{k}'>#{k} (#{v})</option>" unless kexu.key?( k )
		end


		########
########
puts 'HTML30<br>' if @debug
html[30] = <<-"HTML30"
<hr>
<div class='row'>
	<div class='col-1'></div>
	<div class='col-4'>
		<div class='input-group input-group-sm'>
			<label class='input-group-text'>#{l['koho']}</label>
			<select class='form-select' id='kex_add_select'>
				#{option}
			</select>
		</div>
	</div>
	<div class='col-3'></div>
	<div class='col'><button type='button' class='btn btn-dark btn-sm' onclick="kexAdd()">#{l['add']}</button></div>
</div><br>

<div class='row'>
	<div class='col-1'></div>
	<div class='col-4'>
		<div class='input-group input-group-sm'>
			<label class='input-group-text'>#{l['novel']}</label>
			<input type='text' maxlength='32' id='kex_new_item' class='form-control form-control-sm' value=''>
		</div>
	</div>
	<div class='col-2'>
		<div class='input-group input-group-sm'>
			<span class='input-group-text'>#{l['unit']}</span>
			<input type='text' maxlength='32' id='kex_new_unit' class='form-control form-control-sm' value=''>
		</div>
	</div>
	<div class='col-1'></div>
	<div class='col'><button type='button' class='btn btn-dark btn-sm' onclick="kexNew()">#{l['add']}</button></div>
</div><br>
HTML30
########
		########

	end

	return html.join
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

var ksChange = function(){
	const kstart = document.getElementById( 'kstart' ).value;
	$.post( "config.cgi", { mod:'koyomi', step:'kstart', kstart:kstart }, function( data ){
		$( "#L1" ).html( data );
	});
};

var kexAdd = function(){
	const kex_add_select = document.getElementById( 'kex_add_select' ).value;
	$.post( "config.cgi", { mod:'koyomi', step:'select', kex_add_select:kex_add_select }, function( data ){
		$( "#L1" ).html( data );
	});
};

var kexNew = function(){
	const kex_add_key = document.getElementById( 'kex_add_key' ).value;
	const kex_add_unit = document.getElementById( 'kex_add_unit' ).value;

	if( kex_add_key != '' ){
		$.post( "config.cgi", { mod:'koyomi', step:'new', kex_add_key:kex_add_key, kex_add_unit:kex_add_unit }, function( data ){
			$( "#L1" ).html( data );
		});
	}
};

var kexOnOff = function( kex_key ){
	let kex_onoff = 0;
	if( document.getElementById( 'kex_onoff' + kex_key ).checked ){ kex_onoff = 1; }
	$.post( "config.cgi", { mod:'koyomi', step:'available', kex_key:kex_key, kex_onoff:kex_onoff }, function( data ){
		$( "#L1" ).html( data );
	});
};

var kexDel = function( kex_key ){
	if( document.getElementById( 'kex_del' + kex_key ).checked ){
		$.post( "config.cgi", { mod:'koyomi', step:'delete', kex_key:kex_key }, function( data ){
			$( "#L1" ).html( data );
		});
	}else{
		displayVIDEO( "Check!(>_<)" );
	}
};
</script>
JS
	puts js
end


def module_lp( language )
	l = Hash.new
	l['jp'] = {
		'mod_name'	=> "こよみ",\
		'start' => "こよみ開始年",\
		'menu_title' => "こよみ拡張:",\
		'item' => "項目名",\
		'org_name' => "名称",\
		'unit' => "単位",\
		'init' => "<img src='bootstrap-dist/icons/trash.svg' style='height:1.8em; width:1.8em;'>",\
		'add' => "＋",\
		'koho' => "候　補",\
		'novel' => "新　規"
	}

	return l[language]
end
