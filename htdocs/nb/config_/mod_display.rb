# Nutorition browser 2020 Config module for NB display 0.02b
#encoding: utf-8

def config_module( cgi, user, lp )
	module_js()

	step = cgi['step']

	icache = 0
	ifix = 0
	recipel_max = 50
	icalc = 14
	if step ==  'update'
		icache = cgi['icache'].to_i
		ifix = cgi['ifix'].to_i
		recipel_max = cgi['recipel_max'].to_i
		icalc = cgi['icalc'].to_i

		# Updating bio information
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET icache='#{icache}', ifix='#{ifix}', recipel_max='#{recipel_max}', icalc='#{icalc}' WHERE user='#{user.name}';", false, false )
	else
		r = mdb( "SELECT * FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, false )
		icache = r.first['icache'].to_i
		ifix = r.first['ifix'].to_i
		recipel_max = r.first['recipel_max'].to_i
		icalc = r.first['icalc'].to_i
	end

	icache_checked = ''
	icache_checked = 'CHECKED' if icache == 1

	ifix_checked = ''
	ifix_checked = 'CHECKED' if ifix == 1

	list_selected = Hash.new
	list_selected.default = ''
	list_selected[recipel_max.to_s] = 'SELECTED'


	icalc = 14 if icalc == 0

	html = <<-"HTML"
    <div class="container">
    	<div class='row'>
	    	<div class='col-3'>#{lp[65]}</div>
			<div class='col-4'>
				<div class="custom-control custom-switch">
					<input type="checkbox" class="custom-control-input" id="icache" #{icache_checked} onchange="display_cfg()">
					<label class="custom-control-label" for="icache"></label>
				</div>
			</div>
		</div>
		<br>
    	<div class='row'>
	    	<div class='col-3'>#{lp[66]}</div>
			<div class='col-4'>
				<div class="custom-control custom-switch">
					<input type="checkbox" class="custom-control-input" id="ifix" #{ifix_checked} onchange="display_cfg()">
					<label class="custom-control-label" for="ifix">#{lp[67]}</label>
				</div>
			</div>
		</div>
		<br>
    	<div class='row'>
	    	<div class='col-3'>#{lp[68]}</div>
			<div class='col-2'>
				<select class="form-select form-select-sm" id='recipel_max' onchange="display_cfg()">
					<option value='10' #{list_selected['10']}>10</option>
					<option value='25' #{list_selected['25']}>25</option>
					<option value='50' #{list_selected['50']}>50</option>
					<option value='75' #{list_selected['75']}>75</option>
					<option value='100' #{list_selected['100']}>100</option>
					<option value='150' #{list_selected['150']}>150</option>
					<option value='200' #{list_selected['200']}>200</option>
				</select>
			</div>
		</div>
		<br>
    	<div class='row'>
	    	<div class='col-3'>#{lp[69]}</div>
			<div class='col-2'>
				<input class="form-control form-control-sm" type="number" min='5' max='20' id='icalc' value='#{icalc}' onchange="display_cfg()">
			</div>
		</div>
		<br>
 	</div>
HTML
	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// Updating bio information
var display_cfg = function(){
	var icache = 0
	var ifix = 0
	if( document.getElementById( "icache" ).checked ){ icache = 1; }else{ icache = 0; }
	if( document.getElementById( "ifix" ).checked ){ ifix = 1; }else{ ifix = 0; }
	var recipel_max = document.getElementById( "recipel_max" ).value;
	var icalc = document.getElementById( "icalc" ).value;

	$.post( "config.cgi", { mod:'display', step:'update', icache:icache, ifix:ifix, recipel_max:recipel_max, icalc:icalc }, function( data ){ $( "#L1" ).html( data );});

	flashBW();
	dl1 = true;
	dline = true;
	displayBW();
	displayVIDEO( 'Updated' );
};

</script>
JS
	puts js
end
