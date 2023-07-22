# Weight loss module for Physique 0.00b
#encoding: utf-8


@module = 'weight-gain'
@debug = false

def physique_module( cgi, db )
	l = module_lp( user.language )

end


def module_lp( language )
	l = Hash.new
	l['jp'] = {
		'mod_name' => "",\
	}

	return l[language]
end