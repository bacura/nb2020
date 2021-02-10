# Nutorition browser 2020 Config module for Palette 0.00
#encoding: utf-8

#### displying palette
def listing( uname, lp )
	r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{uname}';", false, @debug )

	list_body = ''
	r.each do |e|
		list_body << "<tr><td>#{e['name']}</td><td>#{e['count']}</td>"
		list_body << "<td><button class='btn btn-outline-primary btn-sm' type='button' onclick='palette_cfg( \"edit_palette\", \"#{e['name']}\" )'>#{lp[41]}</button></td>"
		list_body << "<td>"
		list_body << "<input type='checkbox' id=\"#{e['name']}\">&nbsp;<button class='btn btn-outline-danger btn-sm' type='button' onclick='palette_cfg( \"delete_palette\", \"#{e['name']}\" )'>#{lp[42]}</button></td></tr>\n" unless e['name'] == '簡易表示用'
		list_body << "</td></tr>"
	end

	html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-8'><h5>#{lp[43]}</h5></div>
		<div class='col-2'><button class="btn btn-outline-primary btn-sm" type="button" onclick="palette_cfg( 'new_palette', '' )">#{lp[44]}</button></div>
		<div class='col-2'><button class="btn btn-outline-danger btn-sm" type="button" onclick="palette_cfg( 'reset_palette', '' )">#{lp[45]}</button></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
		<tr>
			<td>#{lp[46]}</td>
			<td>#{lp[47]}</td>
			<td>#{lp[48]}</td>
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
	module_js()

	step = cgi['step']
	html = ''

	case step
	when ''
		html = listing( user.name, lp )

	when 'new_palette', 'edit_palette'
		checked = []
		if step == 'edit_palette'
			r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}' AND name='#{cgi['palette_name']}';", false, @debug )
			palette = r.first['palette']
			palette.size.times do |c|
				if palette[c] == '1'
					checked << 'checked'
				else
					checked << ''
				end
			end
		end

		fc_table = ['', '', '', '', '', '', '']
		4.upto( 7 ) do |i| fc_table[0] << "<tr><td><input type='checkbox' id='#{@fct_item[i]}' #{checked[i]}>&nbsp;#{@fct_name[@fct_item[i]]}</td></tr>" end
		8.upto( 19 ) do |i| fc_table[1] << "<tr><td><input type='checkbox' id='#{@fct_item[i]}' #{checked[i]}>&nbsp;#{@fct_name[@fct_item[i]]}</td></tr>" end
		20.upto( 33 ) do |i| fc_table[2] << "<tr><td><input type='checkbox' id='#{@fct_item[i]}' #{checked[i]}>&nbsp;#{@fct_name[@fct_item[i]]}</td></tr>" end
		34.upto( 45 ) do |i| fc_table[3] << "<tr><td><input type='checkbox' id='#{@fct_item[i]}' #{checked[i]}>&nbsp;#{@fct_name[@fct_item[i]]}</td></tr>" end
		46.upto( 55 ) do |i| fc_table[4] << "<tr><td><input type='checkbox' id='#{@fct_item[i]}' #{checked[i]}>&nbsp;#{@fct_name[@fct_item[i]]}</td></tr>" end
		56.upto( 57 ) do |i| fc_table[5] << "<tr><td><input type='checkbox' id='#{@fct_item[i]}' #{checked[i]}>&nbsp;#{@fct_name[@fct_item[i]]}</td></tr>" end

		html = <<-"HTML"
	<div class="container-fluid">
		<div class="row">
			<div class="col-6">
				<div class="input-group mb-3">
  					<span class="input-group-text">#{lp[49]}</span>
  					<input type="text" class="form-control" id="palette_name" value="#{cgi['palette_name']}" maxlength="60">
  				</div>
			</div>
			<div class="col-5"></div>
			<div class="col-1"><button class="btn btn-outline-primary btn-sm" type="button" onclick="palette_cfg( 'regist' )">#{lp[50]}</button></div>
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
		fct_count = 0
		palette_name = cgi['palette_name']

		4.upto( 67 ) do |i|
			fct_bits << cgi[@fct_item[i]].to_i.to_s
			fct_count += 1 if cgi[@fct_item[i]] == '1'
		end

		r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE name='#{palette_name}' AND user='#{user.name}';", false, @debug )
		if r.first
			mdb( "UPDATE #{$MYSQL_TB_PALETTE} SET palette='#{fct_bits}', count='#{fct_count}' WHERE name='#{palette_name}' AND user='#{user.name}';", false, @debug )
		else
			mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET name='#{palette_name}', user='#{user.name}', palette='#{fct_bits}', count='#{fct_count}';", false, @debug )
		end

		html = listing( user.name, lp )

	when 'delete_palette'
		mdb( "DELETE FROM #{$MYSQL_TB_PALETTE} WHERE name='#{cgi['palette_name']}' AND user='#{user.name}';", false, @debug )

		html = listing( user.name, lp )

	when 'reset_palette'
		mdb( "DELETE FROM #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}';", false, @debug )
 		mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{user.name}', name='#{lp[51]}', count='5',  palette='0000001001001000001000000000000000000000000000000000000001';", false, @debug )
		mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{user.name}', name='#{lp[52]}', count='5',  palette='0000001001001000001000000000000000000000000000000000000001';", false, @debug )
		mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{user.name}', name='#{lp[53]}', count='14', palette='0000001001001000001001110110000000000001000000110000000001';", false, @debug )
		mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{user.name}', name='#{lp[54]}', count='54', palette='0000111111111111111111111111111111111111111111111111111111';", false, @debug )

		html = listing( user.name, lp )
	end

	return html
end


def module_js()
	js_fc_set = ''
	4.upto( 57 ) do |i| js_fc_set << "if( document.getElementById( '#{@fct_item[i]}' ).checked ){ var #{@fct_item[i]} = 1 }" end

	post_fc_set = ''
	4.upto( 57 ) do |i| post_fc_set << "#{@fct_item[i]}:#{@fct_item[i]}," end
	post_fc_set.chop!

	js = <<-"JS"
<script type='text/javascript'>

// Sending FC palette
var palette_cfg = function( step, id ){
	if( step == 'new_palette' ){
		$.post( "config.cgi", { mod:'palette', step:step }, function( data ){ $( "#L2" ).html( data );});
		document.getElementById( "L2" ).style.display = 'block';
	}

	switch( step ){
	case 'reset_palette':
		$.post( "config.cgi", { mod:'palette', step:step }, function( data ){ $( "#L1" ).html( data );});
		document.getElementById( "L1" ).style.display = 'block';
		displayVideo( 'Palette reset' );
		break;
	}

	if( step == 'regist' ){
		var palette_name = document.getElementById( "palette_name" ).value;

		if( palette_name != '' ){
			#{js_fc_set}

			$.post( "config.cgi", { mod:'palette', step:step, palette_name:palette_name,
			#{post_fc_set}
			}, function( data ){ $( "#L1" ).html( data );});
			displayVideo( palette_name + 'saved' );
		} else{
			displayVideo( 'Palette name!(>_<)' );
		}
	}

	// Edit FC palette
	if( step == 'edit_palette' ){
		$.post( "config.cgi", { mod:'palette', step:step, palette_name:id }, function( data ){ $( "#L2" ).html( data );});
		document.getElementById( "L2" ).style.display = 'block';
	}

	// Deleting FC palette
	if( step == 'delete_palette' ){
		if( document.getElementById( id ).checked ){
			$.post( "config.cgi", { mod:'palette', step:step, palette_name:id }, function( data ){ $( "#L1" ).html( data );});
			closeBroseWindows( 1 );
			displayLine( 'on' );
		} else{
			displayVideo( 'Check!(>_<)' );
		}
	}

};

</script>
JS
	puts js
end
