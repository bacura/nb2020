# Nutorition browser 2020 Config module for Palette 0.20b
#encoding: utf-8

#### mod debug mode
@degug = true


#### displying palette
def listing( uname, l )
	r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{uname}';", false, @debug )
	list_body = ''
	r.each do |e|
		count = e['palette'].count( '1' )
		list_body << "<tr><td>#{e['name']}</td><td>#{count}</td>"
		list_body << "<td><button class='btn btn-outline-primary btn-sm' type='button' onclick='palette_cfg( \"edit_palette\", \"#{e['name']}\" )'>#{l['edit']}</button></td>"
		list_body << "<td>"
		list_body << "<input type='checkbox' id=\"#{e['name']}\">&nbsp;<button class='btn btn-outline-danger btn-sm' type='button' onclick='palette_cfg( \"delete_palette\", \"#{e['name']}\" )'>#{l['delete']}</button></td></tr>\n" unless e['name'] == '簡易表示用'
		list_body << "</td></tr>"
	end


	html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-8'><h5>#{l['palette_list']}</h5></div>
		<div class='col-2'><button class="btn btn-outline-primary btn-sm" type="button" onclick="palette_cfg( 'new_palette', '' )">#{l['new_palette']}</button></div>
		<div class='col-2'><button class="btn btn-outline-danger btn-sm" type="button" onclick="palette_cfg( 'reset_palette', '' )">#{l['reset']}</button></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
		<tr>
			<td>#{l['palette_name']}</td>
			<td>#{l['fc_num']}</td>
			<td>#{l['operation']}</td>
			<td></td>
		</tr>
	</thead>
	#{list_body}

	</table>
</div>
HTML

	return html
end


def config_module( cgi, user, lp )
	l = module_lp( user.language )
	module_js()

	step = cgi['step']
	html = ''

	case step
	when ''
		html = listing( user.name, l )
	when 'new_palette', 'edit_palette'
		checked = Hash.new
		if step == 'edit_palette'
			r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}' AND name='#{cgi['palette_name']}';", false, @debug )
			palette = r.first['palette']
			palette.size.times do |c|
				checked[@fct_item[c]] = 'checked' if palette[c] == '1'
			end
		end

		fc_table = ['', '', '', '', '', '', '']
		@fct_rew.each do |e| fc_table[0] << "<tr><td><input type='checkbox' id='#{e}' #{checked[e]}>&nbsp;#{@fct_name[e]}</td></tr>" end
		@fct_pf.each do |e| fc_table[1] << "<tr><td><input type='checkbox' id='#{e}' #{checked[e]}>&nbsp;#{@fct_name[e]}</td></tr>" end
		@fct_cho.each do |e| fc_table[2] << "<tr><td><input type='checkbox' id='#{e}' #{checked[e]}>&nbsp;#{@fct_name[e]}</td></tr>" end
		@fct_m.each do |e| fc_table[3] << "<tr><td><input type='checkbox' id='#{e}' #{checked[e]}>&nbsp;#{@fct_name[e]}</td></tr>" end
		@fct_fsv.each do |e| fc_table[4] << "<tr><td><input type='checkbox' id='#{e}' #{checked[e]}>&nbsp;#{@fct_name[e]}</td></tr>" end
		@fct_wsv.each do |e| fc_table[5] << "<tr><td><input type='checkbox' id='#{e}' #{checked[e]}>&nbsp;#{@fct_name[e]}</td></tr>" end
		fc_table[5] << "<tr><td><hr></td></tr>"
		@fct_as.each do |e| fc_table[5] << "<tr><td><input type='checkbox' id='#{e}' #{checked[e]}>&nbsp;#{@fct_name[e]}</td></tr>" end

		html = <<-"HTML"
	<div class="container-fluid">
		<div class="row">
			<div class="col-6">
				<div class="input-group mb-3">
  					<span class="input-group-text">#{l['palette_name']}</span>
  					<input type="text" class="form-control" id="palette_name" value="#{cgi['palette_name']}" maxlength="60">
  				</div>
			</div>
			<div class="col-5"></div>
			<div class="col-1"><button class="btn btn-outline-primary btn-sm" type="button" onclick="palette_cfg( 'regist' )">#{l['regist']}</button></div>
		</div>
		<br>
		<div class="row">
			<div class="col-4"><table class='table-sm table-striped' width='100%'>#{fc_table[0]}</table></div>
			<div class="col-4"><table class='table-sm table-striped' width='100%'>#{fc_table[1]}</table></div>
			<div class="col-4"><table class='table-sm table-striped' width='100%'>#{fc_table[2]}</table></div>
		<div class="row">
		<hr>
		</div>
			<div class="col-4"><table class='table-sm table-striped' width='100%'>#{fc_table[3]}</table></div>
			<div class="col-4"><table class='table-sm table-striped' width='100%'>#{fc_table[4]}</table></div>
			<div class="col-4"><table class='table-sm table-striped' width='100%'>#{fc_table[5]}</table></div>
		</div>
	</div>
HTML

	when 'regist'
		fct_bits = '0000'
		palette_name = cgi['palette_name']

		@fct_min.each do |e| fct_bits << cgi[e].to_i.to_s end
		r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE name='#{palette_name}' AND user='#{user.name}';", false, @debug )
		if r.first
			mdb( "UPDATE #{$MYSQL_TB_PALETTE} SET palette='#{fct_bits}' WHERE name='#{palette_name}' AND user='#{user.name}';", false, @debug )
		else
			mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET name='#{palette_name}', user='#{user.name}', palette='#{fct_bits}';", false, @debug )
		end

		html = listing( user.name, l )

	when 'delete_palette'
		mdb( "DELETE FROM #{$MYSQL_TB_PALETTE} WHERE name='#{cgi['palette_name']}' AND user='#{user.name}';", false, @debug )

		html = listing( user.name, l )

	when 'reset_palette'
		mdb( "DELETE FROM #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}';", false, @debug )
		0.upto( @palette_default.size - 1 ) do |c|
			mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{user.name}', name='#{$PALETTE_DEFAULT_NAME['jp'][c]}', palette='#{$PALETTE_DEFAULT['jp'][c]}';", false, @debug )
		end
		html = listing( user.name, l )
	end

	return html
end


def module_js()
	js_fc_set = ''
	post_fc_set = ''

	@fct_min.each do |e|
		js_fc_set << "if( document.getElementById( '#{e}' ).checked ){ var #{e} = 1 }"
		post_fc_set << "#{e}:#{e},"
	end
	post_fc_set.chop!

	js = <<-"JS"
<script type='text/javascript'>

// Sending FC palette
var palette_cfg = function( step, id ){
	flashBW();
	if( step == 'new_palette' ){
		$.post( "config.cgi", { mod:'palette', step:step }, function( data ){
			$( "#L2" ).html( data );
		});

			dl2 = true;
	}

	if( step == 'reset_palette' ){
		$.post( "config.cgi", { mod:'palette', step:step }, function( data ){
			$( "#L1" ).html( data );
			displayVIDEO( 'Reset' );
		});
	}

	if( step == 'regist' ){
		var palette_name = document.getElementById( "palette_name" ).value;

		if( palette_name != '' ){
			#{js_fc_set}

			$.post( "config.cgi", { mod:'palette', step:step, palette_name:palette_name, #{post_fc_set} }, function( data ){
				$( "#L1" ).html( data );
				displayVIDEO( palette_name );
			});
		} else{
			displayVIDEO( 'Palette name!(>_<)' );
		}
	}

	// Edit FC palette
	if( step == 'edit_palette' ){
		$.post( "config.cgi", { mod:'palette', step:step, palette_name:id }, function( data ){
			$( "#L2" ).html( data );
		});
			dl2 = true;
	}

	// Deleting FC palette
	if( step == 'delete_palette' ){
		if( document.getElementById( id ).checked ){
			$.post( "config.cgi", { mod:'palette', step:step, palette_name:id }, function( data ){
				$( "#L1" ).html( data );
			});
		} else{
			displayVIDEO( 'Check!(>_<)' );
		}
	}
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
		'edit' => "編集",\
		'delete' => "削除",\
		'palette_list' => "カスタム成分パレット一覧",\
		'new_palette' => "新規登録",\
		'reset' => "リセット",\
		'palette_name' => "パレット名",\
		'fc_num' => "成分数",\
		'operation' => "操作",\
		'regist' => "登録"
	}

	return l[language]
end
