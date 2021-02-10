# Nutorition browser 2020 Config module for bio 0.00b
#encoding: utf-8

def config_module( cgi, user, lp )
	module_js()

	step = cgi['step']

	r = mdb( "SELECT * FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, false )
	sex = r.first['sex'].to_i
	age = r.first['age'].to_i
	height = r.first['height'].to_f
	weight = r.first['weight'].to_f

	if step ==  'change'
		sex = cgi['sex'].to_i
		age = cgi['age'].to_i
		height = cgi['height'].to_f
		weight = cgi['weight'].to_f

		# Updating bio information
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET sex='#{sex}', age='#{age}', height='#{height}', weight='#{weight}' WHERE user='#{user.name}';", false, false )
	end

	male_check = ''
	female_check = ''
	if sex == 0
		male_check = 'CHECKED'
	else
		female_check = 'CHECKED'
	end

	html = <<-"HTML"
    <div class="container">
    	<div class='row'>
	    	<div class='col-2'>#{lp[20]}</div>
			<div class='col-4'>
				<div class='form-check form-check-inline'>
					<input class='form-check-input' type='radio' name='sex' id='male' value='0' #{male_check}>
					<label class='form-check-label' for='male'>#{lp[21]}</label>
				</div>
				<div class='form-check form-check-inline'>
					<input class='form-check-input' type='radio' name='sex' id='female' value='1' #{female_check}>
					<label class='form-check-label' for='female'>#{lp[22]}</label>
				</div>
			</div>
		</div>
		<br>
    	<div class='row'>
	    	<div class='col-2'>#{lp[23]}</div>
			<div class='col-3'><input type="number" min="0" id="age" class="form-control login_input" value="#{age}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>#{lp[24]}</div>
			<div class='col-3'><input type="text" maxlength="5" id="height" class="form-control login_input" value="#{height}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>#{lp[25]}</div>
			<div class='col-3'><input type="text" maxlength="5" id="weight" class="form-control login_input" value="#{weight}"></div>
		</div>

		<hr>

    	<div class='row'>
	    	<div class='col-2'></div>
			<div class='col-4'><button type="button" class="btn btn-outline-warning btn-sm nav_button" onclick="bio_cfg( 'change' )">#{lp[26]}</button></div>
		</div>
	</div>
HTML
	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// Updating bio information
var bio_cfg = function( step ){
	var sex = '';
	var age = '';
	var height = '';
	var weight = '';

	if( step == 'change' ){
		if( document.getElementById( "male" ).checked ){
			sex = 0;
		}else{
			sex = 1;
		}
		var age = document.getElementById( "age" ).value;
		var height = document.getElementById( "height" ).value;
		var weight = document.getElementById( "weight" ).value;
	}
	closeBroseWindows( 1 );

	$.post( "config.cgi", { mod:'bio', step:step, sex:sex, age:age, height:height, weight:weight }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
	displayLine( 'on' );
};

</script>
JS
	puts js
end
