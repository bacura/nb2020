# Language pack for koyomi adding panel 0.12b (2022/12/05)

def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'koyomi' 	=> "こよみ:食事",\
		'sun' 		=> "日",\
		'mon' 		=> "月",\
		'tue' 		=> "火",\
		'wed' 		=> "水",\
		'thu' 		=> "木",\
		'fri' 		=> "金",\
		'sat' 		=> "土",\
		'year' 		=> "年",\
		'breakfast' => "朝食",\
		'lunch' 	=> "昼食",\
		'dinner' 	=> "夕食",\
		'supply'	=> "間食 / 補食",\
		'save' 		=> "登　録",\
		'volume' 	=> "量",\
		'time'		=> "分間",\
		'modify'	=> "変更",\
		'copy' 		=> "複製",\
		'inheritance'=> "時間継承",\
		'return' 	=> "<img src='bootstrap-dist/icons/signpost-r.svg' style='height:2em; width:2em;'>",\
		'joystick' 	=> "<img src='bootstrap-dist/icons/geo.svg' style='height:2em; width:2em;'>",\
		'clock'		=> "<img src='bootstrap-dist/icons/clock.svg' style='height:1.5em; width:1.5em;'>",\
		'calendar'	=> "<img src='bootstrap-dist/icons/calendar.svg' style='height:2em; width:2em;'>",\
		'return2'	=> "<img src='bootstrap-dist/icons/signpost.svg' style='height:2em; width:2em;'>"
	}

	return l[language]
end







