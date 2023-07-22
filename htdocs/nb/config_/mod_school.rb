# Nutorition browser 2020 Config module for school 0.10b (2023/07/19)
#encoding: utf-8


def config_module( cgi, db )
	l = module_lp( db.user.language )
	module_js()

	step = cgi['step']
	r = db.query( "SELECT school FROM #{$MYSQL_TB_CFG} WHERE user='#{db.user.name}';", false )
	if r.first
		if r.first['school'] != nil && r.first['school'] != ''
			school = JSON.parse( r.first['school'] )
			cs_name = school['name']
			cs_code = school['code']
			cs_url = school['url']
			cs_doc = school['doc']
			cs_format = school['format']
			week = 0
			week = 1 if cs_format == 'week'
		end
	end

	if step ==  'change'
		cs_name = cgi['cs_name']
		cs_code = cgi['cs_code']
		cs_url = cgi['cs_url']
		cs_doc = cgi['cs_doc']
		month = cgi['month'].to_i
		week = cgi['week'].to_i
		cs_format = 'week'
		cs_format = 'month' if week == 0


		# Updating bio information
		school_ = JSON.generate( { "name" => cs_name, "code" => cs_code, "url" => cs_url, "doc" => cs_doc, "format" => cs_format } )
		db.query( "UPDATE #{$MYSQL_TB_CFG} SET school='#{school_}' WHERE user='#{db.user.name}';", false )
	end


	week_check = 'CHECKED'
	month_check = ''
	cs_format = 'week'
	if week == 0
		month_check = 'CHECKED'
		week_check = ''
		cs_format = 'month'
	end


	html = <<-"HTML"
    <div class="container">
    	<div class='row'>
	    	<div class='col-2'>#{l['cs_name']}</div>
			<div class='col-3'><input type="text" id="cs_name" class="form-control login_input" value="#{cs_name}"></div>
		</div>
    	<div class='row'>
	    	<div class='col-2'>#{l['cs_code']}</div>
			<div class='col-3'><input type="text" id="cs_code" class="form-control login_input" value="#{cs_code}"></div>
		</div>
    	<div class='row'>
	    	<div class='col-2'>#{l['cs_url']}</div>
			<div class='col-10'><input type="text" id="cs_url" class="form-control login_input" value="#{cs_url}"></div>
		</div>
    	<div class='row'>
	    	<div class='col-2'>#{l['cs_doc']}</div>
			<div class='col-10'><input type="text" id="cs_doc" class="form-control login_input" value="#{cs_doc}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>#{l['format']}</div>
			<div class='col-4'>
				<div class='form-check form-check-inline'>
					<input class='form-check-input' type='radio' name='format' id='week' #{week_check}>
					<label class='form-check-label' for='female'>#{l['week']}</label>
				</div>
				<div class='form-check form-check-inline'>
					<input class='form-check-input' type='radio' name='format' id='month' #{month_check}>
					<label class='form-check-label' for='male'>#{l['month']}</label>
				</div>
			</div>
		</div>
		<hr>

    	<div class='row'>
	    	<div class='col-2'></div>
			<div class='col-4'><button type="button" class="btn btn-outline-primary btn-sm nav_button" onclick="school_cfg( 'change' )">#{l['save']}</button></div>
		</div>
	</div>
HTML
	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// Updating bio information
var school_cfg = function( step ){
	var cs_name = '';
	var cs_code = '';
	var cs_url = '';
	var cs_doc = '';
	var month = 0;
	var week = 0;

	if( step == 'change' ){
		cs_name = document.getElementById( "cs_name" ).value;
		cs_code = document.getElementById( "cs_code" ).value;
		cs_url = document.getElementById( "cs_url" ).value;
		cs_doc = document.getElementById( "cs_doc" ).value;
		if( document.getElementById( "week" ).checked ){ week = 1; }
		if( document.getElementById( "month" ).checked ){ month = 1; }
	}
	$.post( "config.cgi", { mod:'school', step:step, cs_name:cs_name, cs_code:cs_code, cs_url:cs_url, cs_doc:cs_doc, week:week, month:month }, function( data ){ $( "#L1" ).html( data );});

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
	l = Hash.new
	l['jp'] = {
		'cs_code' => "教室コード",\
		'cs_name' => "教室名",\
		'cs_url' => "教室URL",\
		'cs_doc' => "教室紹介",\
		'format' => "教室スタイル",\
		'month' => "月替り",\
		'week' => "週替り",\
		'enable' => "開校",\
		'save' => "保存"
	}

	return l[language]
end
