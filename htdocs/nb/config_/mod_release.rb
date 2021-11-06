# Nutorition browser 2020 Config module for release 0.01b
#encoding: utf-8

#mod debug
@debug = false

def config_module( cgi, user, lp )
	module_js()

	step = cgi['step']
	password = cgi['password']
	puts "#{step}<br>" if @debug
	puts "#{password}<br>" if @debug

	html =''

	if step ==  ''
		puts 'form step<br>' if @debug
		html = <<-"HTML"
      	<div class="container">
      		<div class='row'>
	    		#{lp[34]}<br>
    			#{lp[35]}<br>
				#{lp[36]}<br>
			</div><br>
      		<div class='row'>
				<div class='col-4'><input type="password" id="password" class="form-control login_input" placeholder="#{lp[37]}" required></div>
				<div class='col-4'><button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="release_cfg()">#{lp[38]}</button></div>
			</div>
		</div>
HTML
	else
		if user.status != 3 || user.status != 9
			puts 'release step general<br>' if @debug
			html = <<-"HTML"
      		<div class="container">
      			<div class='row'>
	    			#{lp[39]}
				</div>
			</div>
HTML

			# Updating user table
			mdb( "UPDATE #{$MYSQL_TB_USER} SET status='0' WHERE user='#{user.name}' AND cookie='#{user.uid}';", false, false )

			# Deleting indivisual data
			mdb( "DELETE FROM #{$MYSQL_TB_HIS} WHERE user='#{user.name}';", false, false )
			mdb( "DELETE FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, false )
			mdb( "DELETE FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, false )
			mdb( "DELETE FROM #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';", false, false )
			mdb( "DELETE FROM #{$MYSQL_TB_PRICEM} WHERE user='#{user.name}';", false, false )
			mdb( "DELETE FROM #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}';", false, false )
		else
			puts 'release step ROM<br>' if @debug
			html = <<-"HTML"
      		<div class="container">
      			<div class='row'>
	    			#{lp[40]}
				</div>
			</div>
HTML
		end

		return html
	end
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

var release_cfg = function(){
	var password = document.getElementById( "password" ).value;
	closeBroseWindows( 1 );
	displayLINE( 'on' );

	$.post( "config.cgi", { mod:'release', step:'release', password:password }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
};

</script>
JS
	puts js
end
