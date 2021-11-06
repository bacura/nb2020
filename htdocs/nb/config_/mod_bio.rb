# Nutorition browser 2020 Config module for bio 0.21b
#encoding: utf-8



def config_module( cgi, user, lp )
	lp = module_lp( user.language )
	module_js()

	step = cgi['step']
	r = mdb( "SELECT bio FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, false )
	if r.first
		if r.first['bio'] != nil && r.first['bio'] != ''
			bio = JSON.parse( r.first['bio'] )
			sex = bio['sex'].to_i
			age = bio['age'].to_i
			birth = bio['birth']
			height = bio['height'].to_f
			weight = bio['weight'].to_f
			kexow = bio['kexow'].to_i
			pgene = bio['pgene'].to_i
		end
	end

	if step ==  'change'
		sex = cgi['sex'].to_i
		age = cgi['age'].to_i
		birth = cgi['birth']
		height = cgi['height'].to_f
		weight = cgi['weight'].to_f
		kexow = cgi['kexow'].to_i
		pgene = cgi['pgene'].to_i

		# Updating bio information
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET sex='#{sex}', age='#{age}', birth='#{birth}', height='#{height}', weight='#{weight}' WHERE user='#{user.name}';", false, false )
		bio_ = JSON.generate( { "sex" => sex, "age" => age, "birth" => birth, "height" => height, "weight" => weight, "kexow" => kexow, "pgene" => pgene } )
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET bio='#{bio_}' WHERE user='#{user.name}';", false, false )
	end

	male_check = ''
	female_check = ''
	if sex == 0
		male_check = 'CHECKED'
	else
		female_check = 'CHECKED'
	end

	kexow_check = ''
	if user.status >= 2
		kexow_check = 'CHECKED' if kexow == 1
	else
		kexow_disabled = 'DISABLED'
	end

	pgene_check = ''
	if user.status >= 2
		pgene_check = 'CHECKED' if pgene == 1
	else
		pgene_disabled = 'DISABLED'
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
		<hr>

    	<div class='row'>
	    	<div class='col-2'></div>
			<div class='col-4'>
				<div class="form-check">
					<input class="form-check-input" type="checkbox" id="kexow" #{kexow_check} #{kexow_disabled}>#{lp[7]}
				</div>
			</div>
		</div>
    	<div class='row'>
	    	<div class='col-2'></div>
			<div class='col-4'>
				<div class="form-check">
					<input class="form-check-input" type="checkbox" id="pgene" #{pgene_check} #{pgene_disabled}>#{lp[10]}
				</div>
			</div>
		</div>
		<hr>

    	<div class='row'>
	    	<div class='col-2'></div>
			<div class='col-4'><button type="button" class="btn btn-outline-primary btn-sm nav_button" onclick="bio_cfg( 'change' )">#{lp[8]}</button></div>
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
	var kexow = 0;
	var pgene = 0;

	if( step == 'change' ){
		if( document.getElementById( "female" ).checked ){ sex = 1; }
		var age = document.getElementById( "age" ).value;
		var birth = document.getElementById( "birth" ).value;
		var height = document.getElementById( "height" ).value;
		var weight = document.getElementById( "weight" ).value;
		if( document.getElementById( "kexow" ).checked ){ kexow = 1; }
		if( document.getElementById( "pgene" ).checked ){ pgene = 1; }
	}
	$.post( "config.cgi", { mod:'bio', step:step, sex:sex, age:age, birth:birth, height:height, weight:weight, kexow:kexow, pgene:pgene }, function( data ){ $( "#L1" ).html( data );});

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
	mlp['jp'][10] = "ぽっちゃり（倹約）遺伝子が働いている気がする"

	return mlp[language]
end
