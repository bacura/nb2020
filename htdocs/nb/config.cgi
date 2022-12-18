#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 config 0.24b (2022/12/17)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = File.basename( $0, '.cgi' )


#==============================================================================
#LIBRARY
#==============================================================================
require './soul'


#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'account' 	=> "アカウント情報",\
		'display' 	=> "表示",\
		'palette'	=> "成分パレット",\
		'history'	=> "履歴",\
		'rsum'		=> "まな板",\
		'convert'	=> "各種変換",\
		'bio'		=> "生体情報",\
		'allergen'	=> "アレルゲン",\
		'koyomi'	=> "こよみ",\
		'school'	=> "お教室",\
		'release' 	=> "登録解除"
	}

	return l[language]
end


#### 初期画面
def init( l, user )
	bio = ''
	bio = "<span class='badge rounded-pill ppill' onclick=\"configForm( 'bio' )\">#{l['bio']}</span>" if user.status >= 2
	koyomiex = ''
	koyomiex = "<span class='badge rounded-pill ppill' onclick=\"configForm( 'koyomi' )\">#{l['koyomi']}</span>" if user.status >= 2
	school = ''
	school = "<span class='badge rounded-pill ppill' onclick=\"configForm( 'school' )\">#{l['school']}</span>" if user.status >= 8 || user.status == 5

	html = <<-"HTML"
<span class="btn badge rounded-pill ppill" onclick="configForm( 'account' )">#{l['account']}</span>
<span class="btn badge rounded-pill ppill" onclick="configForm( 'display' )">#{l['display']}</span>
<span class="btn badge rounded-pill ppill" onclick="configForm( 'palette' )">#{l['palette']}</span>
<span class="btn badge rounded-pill ppill" onclick="configForm( 'history' )">#{l['history']}</span>
<span class="btn badge rounded-pill ppill" onclick="configForm( 'sum' )">#{l['sum']}</span>
<span class="btn badge rounded-pill ppill" onclick="configForm( 'convert' )">#{l['convert']}</span>
<span class="btn badge rounded-pill ppill" onclick="configForm( 'allergen' )">#{l['allergen']}</span>
#{bio}
#{koyomiex}
#{school}

<span class="badge rounded-pill bg-danger" onclick="configForm( 'release' )">#{l['release']}</span>
HTML

	return html
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
lp = user.load_lp( script )

#### Getting POST
mod = @cgi['mod']


#### Driver
html = ''
if mod == ''
	puts 'INIT<br>' if @debug
	html = init( l, user )
else
	require "#{$HTDOCS_PATH}/config_/mod_#{mod}.rb"

	puts "MOD (#{mod})<br>" if @debug
	html = config_module( @cgi, user, lp )
end


puts 'HTML<br>' if @debug
puts html
