# Config module for sum 0.01b
#encoding: utf-8

def config_module( cgi, user, lp )
	module_js()

	step = cgi['step']

	if step == 'sum_reset'
		mdb( "UPDATE sum set sum='', name='', code='' WHERE user='#{user.name}';", false, false )
	elsif step == 'meal_reset'
		mdb( "UPDATE meal set meal='', name='', code='' WHERE user='#{user.name}';", false, false )
	end

	html = <<-"HTML"
     <div class="container">
      	<div class='row'>
    		#{lp[32]}
		</div>
		<br>
		<div class='row'>
			<div class='col-6'>
				<button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="sum_cfg( 'sum_reset' )">#{lp[33]}</button>
			</div>
			<div class='col-6'>
				<button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="sum_cfg( 'meal_reset' )">#{lp[33]}</button>
			</div>
		</div>
	</div>
HTML
	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// Chopping board initialisation
var sum_cfg = function( step ){
	closeBroseWindows( 1 );
	displayLINE( 'on' )
	$.post( "config.cgi", { mod:'sum', step:step }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';

	if( step == 'sum_reset' ){ displayVIDEO( 'SUM reset' ); }
	if( step == 'meal_reset' ){ displayVIDEO( 'MEAL reset' ); }
	var fx = function(){ refreshCB(); };
	setTimeout( fx, 1000 );
};

</script>
JS
	puts js
end
