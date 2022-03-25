# Nutorition browser 2020 Config module for koyomiex 0.11b
#encoding: utf-8

@debug = false

def config_module( cgi, user, lp )
	l = module_lp( user.language )
	module_js()

	step = cgi['step']
	puts "step: #{step}<br>" if @debug

	kex_select = Hash.new
	kex_oname = Hash.new
	kex_ounit = Hash.new

	case step
	when 'update'
		start = cgi['start'].to_i
		puts "start: #{start}<br>" if @debug

		0.upto( 9 ) do |c|
 			kex_select[c.to_s] = cgi["kex_select#{c}"]
			if kex_select[c.to_s] == 'ND'
 				kex_oname[c.to_s] = ''
				kex_ounit[c.to_s] = ''
			elsif kex_select[c.to_s] == 'original'
				kex_oname[c.to_s] = cgi["oname#{c}"]
				kex_ounit[c.to_s] = cgi["ounit#{c}"]
			else
				kex_oname[c.to_s] = @kex_item[kex_select[c.to_s]]
				kex_ounit[c.to_s] = @kex_unit[kex_select[c.to_s]]
			end
		end

		koyomi_ = JSON.generate( { "start" => start,  "kex_select" => kex_select, "kex_oname" => kex_oname, "kex_ounit" => kex_ounit } )
		r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
		if r.first
			mdb( "UPDATE #{$MYSQL_TB_CFG} SET koyomi='#{koyomi_}' WHERE user='#{user.name}';", false, @debug )
		else
			mdb( "INSERT INTO #{$MYSQL_TB_CFG} SET koyomi='#{koyomi_}', user='#{user.name}';", false, @debug )
		end

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
				kex_oname = koyomi['kex_oname']
				kex_ounit = koyomi['kex_ounit']
				p koyomi if @debug
			end
		end
		kex_select[del_no.to_s] = 'ND'
		kex_oname[del_no.to_s] = ''
		kex_ounit[del_no.to_s] = ''

		koyomi_ = JSON.generate( { "start" => start, "kex_select" => kex_select, "kex_oname" => kex_oname, "kex_ounit" => kex_ounit } )
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
			kex_oname = koyomi['kex_oname']
			kex_ounit = koyomi['kex_ounit']
			p koyomi if @debug
			if kex_select == nil || kex_oname == nil || kex_ounit == nil
				kex_select = { "0"=>"ND", "1"=>"ND", "2"=>"ND", "3"=>"ND", "4"=>"ND", "5"=>"ND", "6"=>"ND", "7"=>"ND", "8"=>"ND", "9"=>"ND" }
				kex_oname = { "0"=>"", "1"=>"", "2"=>"", "3"=>"", "4"=>"", "5"=>"", "6"=>"", "7"=>"", "8"=>"", "9"=>"" }
				kex_ounit = { "0"=>"", "1"=>"", "2"=>"", "3"=>"", "4"=>"", "5"=>"", "6"=>"", "7"=>"", "8"=>"", "9"=>"" }
			end
		else
			kex_select = { "0"=>"ND", "1"=>"ND", "2"=>"ND", "3"=>"ND", "4"=>"ND", "5"=>"ND", "6"=>"ND", "7"=>"ND", "8"=>"ND", "9"=>"ND" }
			kex_oname = { "0"=>"", "1"=>"", "2"=>"", "3"=>"", "4"=>"", "5"=>"", "6"=>"", "7"=>"", "8"=>"", "9"=>"" }
			kex_ounit = { "0"=>"", "1"=>"", "2"=>"", "3"=>"", "4"=>"", "5"=>"", "6"=>"", "7"=>"", "8"=>"", "9"=>"" }
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
HTML

	0.upto( 9 ) do |c|
		html << "<div class='row'>"
		html << "	<div class='col-3'>"
		html << "		<div class='input-group input-group-sm'>"
    	html << "			<label class='input-group-text'>#{l['item']}#{c}</label>"
  		html << "			<select class='form-select' id='kex_select#{c}' onChange=\"kexChangeselect( '#{c}' )\">"

		@kex_item.each do |k, v|
			selected = ''
			selected = 'SELECTED' if kex_select[c.to_s] == k
    		html << "<option value='#{k}' #{selected}>#{v}</option>"
    	end

  		html << "			</select>"
		html << "		</div>"
		html << "	</div>"
		html << "	<div class='col-3'>"
		html << "		<div class='input-group input-group-sm'>"
		html << "			<span class='input-group-text'>#{l['org_name']}</span>"

		disabled = 'DISABLED'
		disabled = '' if kex_select[c.to_s] == 'original'

		html << "<input type='text' maxlength='32' id='oname#{c}' class='form-control form-control-sm' value='#{kex_oname[c.to_s]}' #{disabled}>"
		html << "		</div>"
		html << "	</div>"
		html << "	<div class='col-2'>"
		html << "		<div class='input-group input-group-sm'>"
		html << "				<span class='input-group-text'>#{l['unit']}</span>"

		disabled = 'DISABLED'
		disabled = '' if kex_select[c.to_s] == 'original'
		html << "<input type='text' maxlength='32' id='ounit#{c}' class='form-control form-control-sm' value='#{kex_ounit[c.to_s]}' #{disabled}>"

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

		var oname0 = document.getElementById( "oname0" ).value;
		var oname1 = document.getElementById( "oname1" ).value;
		var oname2 = document.getElementById( "oname2" ).value;
		var oname3 = document.getElementById( "oname3" ).value;
		var oname4 = document.getElementById( "oname4" ).value;
		var oname5 = document.getElementById( "oname5" ).value;
		var oname6 = document.getElementById( "oname6" ).value;
		var oname7 = document.getElementById( "oname7" ).value;
		var oname8 = document.getElementById( "oname8" ).value;
		var oname9 = document.getElementById( "oname9" ).value;

		var ounit0 = document.getElementById( "ounit0" ).value;
		var ounit1 = document.getElementById( "ounit1" ).value;
		var ounit2 = document.getElementById( "ounit2" ).value;
		var ounit3 = document.getElementById( "ounit3" ).value;
		var ounit4 = document.getElementById( "ounit4" ).value;
		var ounit5 = document.getElementById( "ounit5" ).value;
		var ounit6 = document.getElementById( "ounit6" ).value;
		var ounit7 = document.getElementById( "ounit7" ).value;
		var ounit8 = document.getElementById( "ounit8" ).value;
		var ounit9 = document.getElementById( "ounit9" ).value;

		$.post( "config.cgi", {
			mod:'koyomi', step:step, start:start,
			kex_select0:kex_select0, kex_select1:kex_select1, kex_select2:kex_select2, kex_select3:kex_select3, kex_select4:kex_select4, kex_select5:kex_select5, kex_select6:kex_select6, kex_select7:kex_select7, kex_select8:kex_select8, kex_select9:kex_select9,
			oname0:oname0, oname1:oname1, oname2:oname2, oname3:oname3, oname4:oname4, oname5:oname5, oname6:oname6, oname7:oname7, oname8:oname8, oname9:oname9,
			ounit0:ounit0, ounit1:ounit1, ounit2:ounit2, ounit3:ounit3, ounit4:ounit4, ounit5:ounit5, ounit6:ounit6, ounit7:ounit7, ounit8:ounit8, ounit9:ounit9,
		}, function( data ){
			$( "#L1" ).html( data );
			displayVIDEO( 'Saved' );
		});
	}else if( step == 'delete' ){
		if( document.getElementById( del_id ).checked ){
			$.post( "config.cgi", { mod:'koyomi', step:step, del_no:del_no }, function( data ){
				$( "#L1" ).html( data );
				displayVIDEO( 'Deleted' );
			});
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

	if( document.getElementById( select_id ).value == 'original' ){
		document.getElementById('oname' + no ).disabled = false;
		document.getElementById('ounit' + no ).disabled = false;
	}else{
		document.getElementById('oname' + no ).disabled = true;
		document.getElementById('ounit' + no ).disabled = true;
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
