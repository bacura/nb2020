# Nutorition browser 2020 Config module for bio 0.20b
#encoding: utf-8

def config_module( cgi, user, lp )
	lp = module_lp( user.language )
	module_js()

	step = cgi['step']

	r = mdb( "SELECT * FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, false )
	sex = r.first['sex'].to_i
	age = r.first['age'].to_i
	birth = r.first['birth']
	height = r.first['height'].to_f
	weight = r.first['weight'].to_f
	bio_kexow = r.first['bio_kexow'].to_i
	if step ==  'change'
		sex = cgi['sex'].to_i
		age = cgi['age'].to_i
		birth = cgi['birth']
		height = cgi['height'].to_f
		weight = cgi['weight'].to_f
		bio_kexow = cgi['bio_kexow'].to_i

		# Updating bio information
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET sex='#{sex}', age='#{age}', birth='#{birth}', height='#{height}', weight='#{weight}', bio_kexow='#{bio_kexow}' WHERE user='#{user.name}';", false, false )
	end

	male_check = ''
	female_check = ''
	if sex == 0
		male_check = 'CHECKED'
	else
		female_check = 'CHECKED'
	end

	bio_kexow_check = ''
	if user.status >= 2
		bio_kexow_check = 'CHECKED' if bio_kexow == 1
	else
		bio_kexow_disabled = 'DISABLED'
	end


	html = <<-"HTML"
    <div class="container">
    	<div class='row'>
	    	<div class='col-2'>#{lp[1]}</div>
			<div class='col-4'>
				<div class='form-check form-check-inline'>
					<input class='form-check-input' type='radio' name='sex' id='male' #{male_check}>
					<label class='form-check-label' for='male'>#{lp[2]}</label>
				</div>
				<div class='form-check form-check-inline'>
					<input class='form-check-input' type='radio' name='sex' id='female' #{female_check}>
					<label class='form-check-label' for='female'>#{lp[3]}</label>
				</div>
			</div>
		</div>
		<br>
    	<div class='row'>
	    	<div class='col-2'>#{lp[4]}</div>
			<div class='col-3'><input type="number" min="0" id="age" class="form-control login_input" value="#{age}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>#{lp[9]}</div>
			<div class='col-3'><input type="date" id='birth' class="form-control login_input" value="#{birth}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>#{lp[5]}</div>
			<div class='col-3'><input type="text" maxlength="5" id="height" class="form-control login_input" value="#{height}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>#{lp[6]}</div>
			<div class='col-3'><input type="text" maxlength="5" id="weight" class="form-control login_input" value="#{weight}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>#{lp[7]}</div>
			<div class='col-3'>
				<div class="form-check">
					<input class="form-check-input" type="checkbox" id="bio_kexow" #{bio_kexow_check} #{bio_kexow_disabled}>
				</div>
			</div>
		</div>
		<hr>

    	<div class='row'>
	    	<div class='col-2'></div>
			<div class='col-4'><button type="button" class="btn btn-outline-warning btn-sm nav_button" onclick="bio_cfg( 'change' )">#{lp[8]}</button></div>
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
	var sex = 0;
	var age = '';
	var height = '';
	var weight = '';
	var bio_kexow = 0;

	if( step == 'change' ){
		if( document.getElementById( "female" ).checked ){ sex = 1; }
		var age = document.getElementById( "age" ).value;
		var birth = document.getElementById( "birth" ).value;
		var height = document.getElementById( "height" ).value;
		var weight = document.getElementById( "weight" ).value;
		if( document.getElementById( "bio_kexow" ).checked ){ bio_kexow = 1; }
	}

	$.post( "config.cgi", { mod:'bio', step:step, sex:sex, age:age, birth:birth, height:height, weight:weight, bio_kexow:bio_kexow }, function( data ){ $( "#L1" ).html( data );});

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
	mlp = Hash.new
	mlp['jp'] = []
	mlp['jp'][1] = "代謝的性別"
	mlp['jp'][2] = "男性"
	mlp['jp'][3] = "女性"
	mlp['jp'][4] = "年齢（廃止予定）"
	mlp['jp'][5] = "身長(m)"
	mlp['jp'][6] = "体重(kg)"
	mlp['jp'][7] = "拡張こよみ上書き"
	mlp['jp'][8] = "保存"
	mlp['jp'][9] = "生年月日"

	return mlp[language]
end
