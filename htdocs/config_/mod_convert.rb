# Nutorition browser 2020 Config module for food number converter 0.00b
#encoding: utf-8

def config_module( cgi, user, lp )
	lp = mlp( user.language )
	module_js()
	from_fn = cgi['from_fn'].to_s
	into_fn = cgi['into_fn'].to_s

	case cgi['step']
	when 'confirm'
	when 'exchange'
	end

	####

	html = <<-"HTML"

HTML
	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// Food number converter initialisation
var convert_cfg = function( mode ){

};

</script>
JS
	puts js
end


def module_jp( user )
	mlp = Hash.new
	mlp['jp'] = []


	return mlp[user.language]
end