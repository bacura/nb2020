# Nutorition browser 2020 Config module for school 0.00b
#encoding: utf-8

def config_module( cgi, user, lp )
	module_js()
	school_mode = cgi['school_mode'].to_i

	case cgi['step']
	when 'update'
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET school='#{school_mode}' WHERE user='#{user.name}';", false, @debug )
	end

	####
	r = mdb( "SELECT school FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
	school_mode = r.first['school'].to_i if r.first
	school_mode = 1 if school_mode == 0

	checked = ['', 'CHECKED', '', ''] if school_mode == 1
	checked = ['', '', 'CHECKED', ''] if school_mode == 2
	checked = ['', '', '', 'CHECKED'] if school_mode == 3

	html = <<-"HTML"
     <div class="container">

      	<div class='row'>
      		<h5>#{lp[72]}</h5>
      	</div>
     	<div class='row'>
			<div class='col'>
				<div class="form-check form-check-inline">
					<input class="form-check-input" type="radio" name="school_mode" id="school_mode1" value="1" #{checked[1]} onclick="school_cfg( '#{lp[74]}' )">
					<label class="form-check-label" for="inlineRadio1">#{lp[74]}</label>
				</div>
				<div class="form-check form-check-inline">
					<input class="form-check-input" type="radio" name="school_mode" id="school_mode2" value="2" #{checked[2]} onclick="school_cfg( '#{lp[75]}' )">
					<label class="form-check-label" for="inlineRadio2">#{lp[75]}</label>
				</div>
				<div class="form-check form-check-inline">
					<input class="form-check-input" type="radio" name="school_mode" id="school_mode3" value="3" #{checked[3]} onclick="school_cfg( '#{lp[77]}' )">
					<label class="form-check-label" for="inlineRadio3">#{lp[77]}</label>
				</div>
			</div>
		</div>
	</div>
HTML
	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// History initialisation
var school_cfg = function( mode ){
	var school_mode = 1;
	if ( document.getElementById( "school_mode2" ).checked ){ school_mode = 2; }
	if ( document.getElementById( "school_mode3" ).checked ){ school_mode = 3; }
	$.post( "config.cgi", { mod:'school', step:'update', school_mode:school_mode }, function( data ){ $( "#L1" ).html( data );});

	displayVIDEO( 'School mode -> '+ mode );
};


</script>
JS
	puts js
end
