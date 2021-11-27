# Nutorition browser 2020 Config module for koyomiex 0.10b
#encoding: utf-8

@debug = false

def config_module( cgi, user, lp )
	l = module_lp( user.language )
	module_js()

	step = cgi['step']
	puts "step: #{step}<br>" if @debug

	kex_select = Hash.new
	kex_item = Hash.new
	kex_unit = Hash.new

	case step
	when 'update'
		start = cgi['start'].to_i
		puts "start: #{start}<br>" if @debug

		0.upto( 9 ) do |c|
			kex_select[c.to_s] = cgi["kex_select#{c}"].to_i
			kex_item[c.to_s] = cgi["item#{c}"]
			kex_unit[c.to_s] = cgi["unit#{c}"]
			unless kex_select[c.to_s] == 0 || kex_select[c.to_s] == 1
				kex_item[c.to_s] = ''
				kex_unit[c.to_s] = ''
			end
		end
		koyomi_ = JSON.generate( { "start" => start,  "kex_select" => kex_select, "kex_item" => kex_item, "kex_unit" => kex_unit } )
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET koyomi='#{koyomi_}' WHERE user='#{user.name}';", false, false )

	when 'delete'
		del_no = cgi['del_no'].to_i
		puts "del_no: #{del_no}<br>" if @debug

		mdb( "UPDATE #{$MYSQL_TB_KOYOMIEX} SET item#{del_no}='' WHERE user='#{user.name}';", false, @debug )

		r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
		if r.first
			if r.first['koyomi'] != nil && r.first['koyomi'] != ''
				koyomi = JSON.parse( r.first['koyomi'] )
				start = koyomi['start'].to_i
				kex_select = koyomi['kex_select']
				kex_item = koyomi['kex_item']
				kex_unit = koyomi['kex_unit']
				p koyomi if @debug
			end
		end
		kex_select[del_no.to_s] = 0
		kex_item[del_no.to_s] = ''
		kex_unit[del_no.to_s] = ''

		koyomi_ = JSON.generate( { "start" => start, "kex_select" => kex_select, "kex_item" => kex_item, "kex_unit" => kex_unit } )
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET koyomi='#{koyomi_}' WHERE user='#{user.name}';", false, false )
	end

	t = Time.new
	start = t.year

	r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
	if r.first
		if r.first['koyomi'] != nil && r.first['koyomi'] != ''
			koyomi = JSON.parse( r.first['koyomi'] )
			start = koyomi['start'].to_i
			kex_select = koyomi['kex_select']
			kex_item = koyomi['kex_item']
			kex_unit = koyomi['kex_unit']
			p koyomi if @debug
		end
	end

	puts 'Setting koyomi start year<br>' if @debug
	start_select = "<select class='form-select' id='start'>"
	2000.upto(2050) do |c|
		selectd = ''
		selected = 'SELECTED' if c == start
		start_select << "<option value='#{c}' #{selected}>#{c}</option>"
	end
  	start_select << "</select>"


 	puts 'HTML<br>' if @debug
	html = <<-"HTML"
	<div class="container">
		<div class='row'>
			<div class='col-3'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>#{l['start']}</span>
					#{start_select}
				</div>
			</div>
		</div>
		<hr>

		<h5>#{l['menu_title']}</h5>
		<br>
HTML

	0.upto( 9 ) do |c|
		html << "<div class='row'>"
		html << "	<div class='col-3'>"
		html << "		<div class='input-group input-group-sm'>"
    	html << "			<label class='input-group-text'>#{l['item']}#{c}</label>"
  		html << "			<select class='form-select' id='kex_select#{c}' onChange=\"kexChangeselect( '#{c}' )\">"

		@kex_item.size.times do |cc|
			selected = ''
			selected = 'SELECTED' if cc == kex_select[c.to_s]
    		html << "<option value='#{cc}' #{selected}>#{@kex_item[cc]}</option>"
    	end

  		html << "			</select>"
		html << "		</div>"
		html << "	</div>"
		html << "	<div class='col-3'>"
		html << "		<div class='input-group input-group-sm'>"
		html << "			<span class='input-group-text'>#{l['org_name']}</span>"

		disabled = 'DISABLED'
		disabled = '' if kex_select[c.to_s] == 1
		html << "<input type='text' maxlength='32' id='item#{c}' class='form-control form-control-sm' value='#{kex_item[c.to_s]}' #{disabled}>"

		html << "		</div>"
		html << "	</div>"
		html << "	<div class='col-2'>"
		html << "		<div class='input-group input-group-sm'>"
		html << "				<span class='input-group-text'>#{l['unit']}</span>"

		disabled = 'DISABLED'
		disabled = '' if kex_select[c.to_s] == 1
		html << "<input type='text' maxlength='32' id='unit#{c}' class='form-control form-control-sm' value='#{kex_unit[c.to_s]}' #{disabled}>"

		html << "		</div>"
		html << "	</div>"
		html << "	<div class='col-1'></div>"
		html << "	<div class='col-2'><input type='checkbox' id='kex_del#{c}'>&nbsp;<button type='button' class='btn btn-outline-danger btn-sm' onclick=\"koyomiex_cfg( 'delete', 'kex_del#{c}', '#{c}' )\">#{l['init']}</button></div>"
		html << "</div><br>"
	end

  	html << "<div class='row'>"
	html << "<div class='col-2'></div>"
	html << "<div class='col-4'><button type='button' class='btn btn-outline-primary btn-sm nav_button' onclick=\"koyomiex_cfg( 'update' )\">#{l['save']}</button></div>"
	html << "</div>"
	html << "</div>"

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

//
var koyomiex_cfg = function( step, del_id, del_no ){
	if( step == 'update' ){
		var start = document.getElementById( "start" ).value;

		var kex_select0 = document.getElementById( "kex_select0" ).value;
		var kex_select1 = document.getElementById( "kex_select1" ).value;
		var kex_select2 = document.getElementById( "kex_select2" ).value;
		var kex_select3 = document.getElementById( "kex_select3" ).value;
		var kex_select4 = document.getElementById( "kex_select4" ).value;
		var kex_select5 = document.getElementById( "kex_select5" ).value;
		var kex_select6 = document.getElementById( "kex_select6" ).value;
		var kex_select7 = document.getElementById( "kex_select7" ).value;
		var kex_select8 = document.getElementById( "kex_select8" ).value;
		var kex_select9 = document.getElementById( "kex_select9" ).value;

		var item0 = document.getElementById( "item0" ).value;
		var item1 = document.getElementById( "item1" ).value;
		var item2 = document.getElementById( "item2" ).value;
		var item3 = document.getElementById( "item3" ).value;
		var item4 = document.getElementById( "item4" ).value;
		var item5 = document.getElementById( "item5" ).value;
		var item6 = document.getElementById( "item6" ).value;
		var item7 = document.getElementById( "item7" ).value;
		var item8 = document.getElementById( "item8" ).value;
		var item9 = document.getElementById( "item9" ).value;

		var unit0 = document.getElementById( "unit0" ).value;
		var unit1 = document.getElementById( "unit1" ).value;
		var unit2 = document.getElementById( "unit2" ).value;
		var unit3 = document.getElementById( "unit3" ).value;
		var unit4 = document.getElementById( "unit4" ).value;
		var unit5 = document.getElementById( "unit5" ).value;
		var unit6 = document.getElementById( "unit6" ).value;
		var unit7 = document.getElementById( "unit7" ).value;
		var unit8 = document.getElementById( "unit8" ).value;
		var unit9 = document.getElementById( "unit9" ).value;

		$.post( "config.cgi", {
			mod:'koyomi', step:step, start:start,
			kex_select0:kex_select0, kex_select1:kex_select1, kex_select2:kex_select2, kex_select3:kex_select3, kex_select4:kex_select4, kex_select5:kex_select5, kex_select6:kex_select6, kex_select7:kex_select7, kex_select8:kex_select8, kex_select9:kex_select9,
			item0:item0, item1:item1, item2:item2, item3:item3, item4:item4, item5:item5, item6:item6, item7:item7, item8:item8, item9:item9,
			unit0:unit0, unit1:unit1, unit2:unit2, unit3:unit3, unit4:unit4, unit5:unit5, unit6:unit6, unit7:unit7, unit8:unit8, unit9:unit9,
		}, function( data ){ $( "#L1" ).html( data );});
		displayVIDEO( 'Saved' );
	}else if( step == 'delete' ){
		if( document.getElementById( del_id ).checked ){
			$.post( "config.cgi", { mod:'koyomi', step:step, del_no:del_no }, function( data ){ $( "#L1" ).html( data );});
			displayVIDEO( 'Deleted' );
		}else{
			displayVIDEO( 'Check!(>_<)' );
		}
	}else{
		$.post( "config.cgi", { mod:'koyomi', step:step,  }, function( data ){ $( "#L1" ).html( data );});
	}

	flashBW();
	dl1 = true;
	dline = true;
	displayBW();
};

var kexChangeselect = function( no ){
	var select_id = 'kex_select' + no;
	displayVIDEO( document.getElementById( select_id ).value );

	if( document.getElementById( select_id ).value == 1 ){

		document.getElementById('item' + no ).disabled = false;
		document.getElementById('unit' + no ).disabled = false;
	}else{
		document.getElementById('item' + no ).disabled = true;
		document.getElementById('unit' + no ).disabled = true;
	}
};

</script>
JS
	puts js
end


def module_lp( language )
	l = Hash.new
	l['jp'] = {
		'start' => "こよみ開始年",\
		'menu_title' => "こよみ拡張・項目設定:",\
		'item' => "項目",\
		'org_name' => "名称",\
		'unit' => "単位",\
		'init' => "初期化",\
		'save' => "保存"
	}

	return l[language]
end
